# In converter/api.py

import os
import shutil
import subprocess
from pathlib import Path

from PIL import Image  # Make sure PIL Image is imported
from tqdm import tqdm

from converter._dataclss import ConverterSetting, WorkspaceSetting
from converter._path_parser import PathParser
from converter._typing import Resolution, Scale
from converter.core.onnx_infer import image_enforce
from converter.utils.config import load_settings_file, write_settings_file
from converter.workflow.common_config import *

# --- Load settings (assuming these are correct) ---
try:
    converter_settings: ConverterSetting = load_settings_file(
        "converter.toml", ConverterSetting
    )
    workspace_settings: WorkspaceSetting = load_settings_file(
        "workspace.toml", WorkspaceSetting
    )
    path_parser = PathParser()
    scale_list = list(Scale.__args__)
except Exception as e:
    # Handle exceptions during setup if necessary
    print(f"[ERROR] Failed to load settings or initialize PathParser: {e}")
    # Depending on your structure, you might want to raise this or exit.
    raise  # Re-raise to make the issue apparent

# --- Function Definitions ---


def save_image(image: Image.Image, resolution: int):  # <-- Add type hint for clarity
    """
    Saves the input PIL Image to the workspace input path after resizing it.

    Args:
        image: The input PIL Image object.
        resolution: The target resolution for the longest side.
    """
    print(f"[INFO] Received image of type: {type(image)}")  # Debug print

    # --- *** THE FIX IS HERE *** ---
    # The input 'image' is ALREADY a PIL Image object.
    # DO NOT try to convert it from a numpy array.
    # pil_img = Image.fromarray(image.astype("uint8")) # type:ignore  <--- REMOVE THIS LINE
    pil_img = image  # Use the passed PIL image directly
    # --- *** END FIX *** ---

    # Get image dimensions
    original_width, original_height = pil_img.size
    print(f"[INFO] Original image size: {original_width}x{original_height}")

    # Calculate new dimensions preserving aspect ratio based on the longest side
    if original_width == 0 or original_height == 0:
        print("[ERROR] Invalid image dimensions (0). Cannot resize.")
        raise ValueError("Invalid input image dimensions")

    aspect_ratio = original_width / original_height

    if original_width >= original_height:
        # Width is longest or image is square
        new_width = resolution
        new_height = max(
            1, int(new_width / aspect_ratio)
        )  # Ensure height is at least 1
    else:
        # Height is longest
        new_height = resolution
        new_width = max(1, int(new_height * aspect_ratio))  # Ensure width is at least 1

    print(f"[INFO] Resizing image to: {new_width}x{new_height}")

    # Resize the image using Pillow's resize method
    try:
        # Use LANCZOS (a.k.a. ANTIALIAS in newer Pillow) for high-quality downscaling/upscaling
        resampling_filter = (
            Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
        )
        resized_img = pil_img.resize((new_width, new_height), resampling_filter)
    except Exception as e:
        print(f"[ERROR] Failed to resize image: {e}")
        raise  # Re-raise the exception to be caught by the main script

    # Prepare workspace and input directories (ensure paths are Path objects)
    workspace_dir = path_parser.workspace
    input_dir = path_parser.input

    # Clean and create directories (use Path object methods)
    try:
        if workspace_dir.exists():
            print(f"[INFO] Removing existing workspace directory: {workspace_dir}")
            shutil.rmtree(workspace_dir)
        os.makedirs(workspace_dir)
        print(f"[INFO] Created workspace directory: {workspace_dir}")

        # Input dir is usually inside workspace, create it too
        # No need to remove separately if workspace is removed above
        os.makedirs(input_dir)
        print(f"[INFO] Created input directory: {input_dir}")

    except OSError as e:
        print(f"[ERROR] Failed to prepare directories: {e}")
        raise

    # Define the save path using PathParser (should return a Path object)
    save_file_path = path_parser.input_image
    print(f"[INFO] Target save path: {save_file_path}")

    # Save the resized image
    try:
        # Ensure the image is in a saveable mode (e.g., convert RGBA to RGB if saving as JPEG)
        # Infer format from suffix, default to PNG if unknown
        file_suffix = save_file_path.suffix.lower()
        save_format = "JPEG" if file_suffix in [".jpg", ".jpeg"] else "PNG"

        img_to_save = resized_img
        if save_format == "JPEG":
            if (
                img_to_save.mode == "RGBA" or img_to_save.mode == "P"
            ):  # Handle RGBA and Palette modes for JPEG
                print("[INFO] Converting image to RGB for JPEG saving.")
                img_to_save = img_to_save.convert("RGB")
            save_params = {"quality": 95}  # Example: Set JPEG quality
        else:  # Defaulting to PNG
            save_format = "PNG"  # Explicitly set format name for save()
            save_params = {"compress_level": 6}  # Example: Set PNG compression

        # Convert Path object to string for Pillow's save function
        img_to_save.save(str(save_file_path), format=save_format, **save_params)
        print(f"[INFO] Image successfully saved to {save_file_path}")
        return f"Image saved as {save_file_path}"
    except Exception as e:
        print(f"[ERROR] Failed to save image to {save_file_path}: {e}")
        raise  # Re-raise the exception


def animegan_picture_transfer(
    image: Image.Image, resolution: int, upscale: bool
):  # Hint input type
    """
    Performs style transfer on a single image.

    Args:
        image: The input PIL Image object.
        resolution: Target resolution for the longest side before style transfer.
        upscale: Whether to upscale the result using RealESRGAN.

    Returns:
        A PIL Image object containing the processed image.
    """
    print("[INFO] Starting animegan_picture_transfer...")
    # 1. Save the input image (resized) to the expected location
    try:
        save_status = save_image(image, resolution)  # Pass the PIL image directly
        print(f"[INFO] {save_status}")
    except Exception as e:
        print(f"[ERROR] Failed during save_image step: {e}")
        raise  # Propagate the error

    # 2. Prepare output directory (optional: clean before processing)
    output_dir = path_parser.output
    if output_dir.exists():
        print(f"[INFO] Removing existing output directory: {output_dir}")
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    print(f"[INFO] Created output directory: {output_dir}")

    # 3. Define input/output paths for the model using PathParser
    input_image_path = str(
        path_parser.input_image
    )  # Path where save_image saved the file
    output_image_path = str(
        path_parser.output_image
    )  # Path where the model should save its output
    model_path = str(path_parser.model_path)  # Path to the ONNX model

    print(f"[INFO] Input to image_enforce: {input_image_path}")
    print(f"[INFO] Model for image_enforce: {model_path}")
    print(f"[INFO] Output from image_enforce: {output_image_path}")

    # 4. Run the style transfer model
    try:
        image_enforce(
            input=input_image_path,
            model_path=model_path,
            output=output_image_path,  # Pass the DIRECT output file path
        )
        print("[INFO] image_enforce completed.")
    except Exception as e:
        print(f"[ERROR] Failed during image_enforce step: {e}")
        # Check if output file exists even if enforce failed partially
        if not Path(output_image_path).exists():
            print("[ERROR] Output image file not found after image_enforce error.")
            raise RuntimeError(
                f"image_enforce failed and produced no output: {e}"
            ) from e
        else:
            print(
                "[WARNING] image_enforce raised an error, but an output file exists. Trying to proceed."
            )
            # Decide if you want to continue or raise the error. Raising is safer.
            raise  # Re-raise the error from image_enforce

    # 5. Load the processed image
    try:
        # Ensure the output path exists before trying to open
        if not Path(output_image_path).is_file():
            raise FileNotFoundError(
                f"Processed image not found at expected path: {output_image_path}"
            )
        processed_image_pil = Image.open(output_image_path)
        print(f"[INFO] Successfully loaded processed image from {output_image_path}")
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        raise  # Cannot continue without the processed image
    except Exception as e:
        print(f"[ERROR] Failed to open processed image file {output_image_path}: {e}")
        raise  # Re-raise other potential PIL errors

    # 6. Apply upscaling if requested
    final_image = processed_image_pil
    if upscale:
        print("[INFO] Upscaling requested.")
        try:
            # Assuming upscale_image saves the upscaled file and returns the PIL image
            # Important: upscale_image needs the *path* to the image it should upscale
            # It currently seems designed to upscale path_parser.output_image and save to path_parser.upscale_image
            final_image = upscale_image(
                output_image_path, "4x"
            )  # Pass the path to upscale
            print("[INFO] Upscaling completed.")
        except Exception as e:
            print(f"[ERROR] Failed during upscale_image step: {e}")
            # Decide if you want to return the non-upscaled image or raise an error
            # Returning non-upscaled might be acceptable, but signal it.
            print("[WARNING] Upscaling failed. Returning non-upscaled image.")
            # Optionally raise e if upscaling must succeed
            # raise
    else:
        print("[INFO] Upscaling not requested.")

    print("[INFO] animegan_picture_transfer finished.")
    return final_image  # Return the final PIL image (either processed or processed+upscaled)


# Modify upscale_image to accept input path and handle PIL Image return
def upscale_image(input_image_path: str, scale: Scale) -> Image.Image:
    """
    Upscales the image at the given path using RealESRGAN.

    Args:
        input_image_path: Path to the image file to upscale.
        scale: The upscale factor (e.g., "4x").

    Returns:
        A PIL Image object of the upscaled image.
    """
    print(f"[INFO] Starting upscale_image for: {input_image_path}")
    if scale not in ["2x", "4x", "8x"]:
        raise ValueError("Unsupported scale. Choose '2x', '4x', or '8x'.")

    # Define paths using PathParser
    execu_path = str(path_parser.realesr_excu)
    upscaled_output_path = str(
        path_parser.upscale_image
    )  # Where RealESRGAN saves the output
    model_name = converter_settings.realesr_model

    # Ensure the input path exists
    if not Path(input_image_path).is_file():
        raise FileNotFoundError(
            f"Input image for upscaling not found: {input_image_path}"
        )

    # Ensure the output directory exists (RealESRGAN might not create it)
    Path(upscaled_output_path).parent.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] RealESRGAN Executable: {execu_path}")
    print(f"[INFO] RealESRGAN Input: {input_image_path}")
    print(f"[INFO] RealESRGAN Output: {upscaled_output_path}")
    print(f"[INFO] RealESRGAN Model: {model_name}")

    # Run RealESRGAN
    try:
        # Use subprocess.run for better control and error checking
        process = subprocess.run(
            [
                execu_path,
                "-i",
                input_image_path,
                "-o",
                upscaled_output_path,
                "-n",
                model_name,
                "-s",
                scale.replace("x", ""),  # Pass scale factor if needed, e.g. -s 4
                # Add any other necessary flags, e.g., -g for GPU index
            ],
            check=True,  # Raise exception on non-zero exit code
            capture_output=True,  # Capture stdout/stderr
            text=True,  # Decode output as text
        )
        print(f"[INFO] RealESRGAN stdout:\n{process.stdout}")
        print(
            f"[INFO] RealESRGAN stderr:\n{process.stderr}"
        )  # Check stderr for warnings/errors too
        print("[INFO] RealESRGAN process completed successfully.")

    except FileNotFoundError:
        print(f"[ERROR] RealESRGAN executable not found at: {execu_path}")
        raise RuntimeError(f"RealESRGAN executable not found at: {execu_path}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] RealESRGAN failed with exit code {e.returncode}")
        print(f"[ERROR] RealESRGAN stdout:\n{e.stdout}")
        print(f"[ERROR] RealESRGAN stderr:\n{e.stderr}")
        # Check if output file was created despite error
        if not Path(upscaled_output_path).exists():
            print("[ERROR] Upscaled image file not found after RealESRGAN error.")
        raise RuntimeError(f"RealESRGAN execution failed: {e.stderr}") from e
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred during RealESRGAN execution: {e}")
        raise  # Re-raise other errors

    # Load and return the upscaled image as a PIL object
    try:
        if not Path(upscaled_output_path).is_file():
            raise FileNotFoundError(
                f"Upscaled image not found at expected path: {upscaled_output_path}"
            )
        upscaled_image_pil = Image.open(upscaled_output_path)
        print(f"[INFO] Successfully loaded upscaled image from {upscaled_output_path}")
        return upscaled_image_pil
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        raise
    except Exception as e:
        print(f"[ERROR] Failed to open upscaled image file {upscaled_output_path}: {e}")
        raise


# --- Other functions (animegan_video_transfer, etc.) remain the same ---
# def animegan_video_transfer(): ...
