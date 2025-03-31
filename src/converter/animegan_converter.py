import io  # Required for handling byte streams

import streamlit as st
from PIL import Image

# --- Assuming these imports work and contain the necessary definitions ---
# Assuming converter is installed or in PYTHONPATH
from converter._path_parser import PathParser
from converter._typing import ModelName, Resolution, Scale
from converter.api import (
    animegan_picture_transfer,  # Keep save_image if needed elsewhere, but it's called internally now
)
from converter._dataclss import ConverterSetting
from converter.utils.config import load_settings_file
# Initialize PathParser (ensure paths are valid in the execution environment)
path_parser = PathParser()

# Get choices (handle potential errors if typing is complex)
# model_choice = list(ModelName.__args__) # type: ignore # This isn't used in the UI yet

converter_settings: ConverterSetting = load_settings_file("converter.toml", ConverterSetting)


# --- Streamlit App ---
if not converter_settings.as_package:
    st.set_page_config(layout="wide")
    st.title("🖼️ Image Style Transfer and Tools")

# --- Session State Initialization ---
if "output_image" not in st.session_state:
    st.session_state.output_image = None
if "status_text" not in st.session_state:
    st.session_state.status_text = ""
if "input_image_display" not in st.session_state:
    st.session_state.input_image_display = None

# --- UI Layout ---
tab1, tab2, tab3 = st.tabs(
    [
        "🎨 Image-to-Image",
        "🎬 Video-to-Video (Placeholder)",
        "🔍 RealESRGAN (Placeholder)",
    ]
)

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.header("Input & Settings")
        uploaded_file = st.file_uploader(
            "Choose an image...", type=["png", "jpg", "jpeg", "webp"]
        )

        input_image = None  # Initialize input_image before the conditional block

        if uploaded_file is not None:
            try:
                # Read the image using PIL
                input_image = Image.open(uploaded_file)
                # Ensure image is in RGB or RGBA format that PIL can handle well
                # Convert palette images (like some GIFs) or grayscale to RGB
                if input_image.mode == "P" or input_image.mode == "L":
                    input_image = input_image.convert("RGB")
                # Keep alpha if present, otherwise convert potentially odd modes to RGB
                elif input_image.mode not in ("RGB", "RGBA"):
                    input_image = input_image.convert("RGB")

                st.session_state.input_image_display = input_image  # Store for display

                # Display the uploaded image
                st.image(
                    input_image, caption="Uploaded Image", use_container_width=True
                )

                # --- Settings ---
                resolution = st.slider(
                    label="Select Output Resolution (Longest Side):",
                    min_value=128,  # Lower min might be useful
                    max_value=2048,  # Higher max might be desired
                    value=720,
                    step=64,  # Steps powers of 2 or divisible by common factors
                    help="Adjust the desired output resolution (longest side). Aspect ratio is preserved.",
                )
                st.write(f"Selected Resolution: `{int(resolution)}` px")

                upscale = st.checkbox(
                    "Enable 4x Upscaling (RealESRGAN)?",
                    value=False,
                    help="Check this box to apply 4x upscaling after style transfer.",
                )

                # --- Action Buttons ---
                transfer_button = st.button(
                    "✨ Start Style Transfer",
                    type="primary",
                    use_container_width=True,
                    key="transfer_btn",
                )

                # --- Process Actions ---
                if transfer_button and input_image:  # Ensure input_image is valid
                    with st.spinner("🎨 Applying style transfer... Please wait."):
                        try:
                            # Call the API function with the PIL image, resolution, and upscale flag
                            processed_image = animegan_picture_transfer(
                                input_image, int(resolution), upscale
                            )

                            # Store result in session state
                            st.session_state.output_image = processed_image
                            st.session_state.status_text = (
                                "✅ Style transfer successful!"
                            )
                            st.success(
                                st.session_state.status_text
                            )  # Show success message immediately

                        except Exception as e:
                            st.session_state.output_image = None
                            st.session_state.status_text = (
                                f"❌ Error during style transfer: {e}"
                            )
                            # Log the full error for debugging if needed
                            # import traceback
                            # st.error(f"{st.session_state.status_text}\n```\n{traceback.format_exc()}\n```")
                            st.error(
                                st.session_state.status_text
                            )  # Show error immediately

            except Exception as e:
                st.error(f"Error loading or preparing image: {e}")
                # Reset states if image loading failed
                st.session_state.input_image_display = None
                st.session_state.output_image = None
                st.session_state.status_text = "Failed to load image."
                input_image = None  # Ensure input_image is None if loading failed

        else:
            # If no file is uploaded, show a message
            st.info("Please upload an image to begin.")
            # Option to clear previous results when file is removed (can be complex to detect removal vs. initial state)
            # A simple approach is to clear output if input_image_display is None AFTER a file was potentially there.
            # For now, relying on user uploading a new file to trigger processing.
            # st.session_state.output_image = None # Uncomment if you want output cleared when no file is present

    with col2:
        st.header("Output")

        # --- Display Output ---
        if st.session_state.output_image:
            st.image(
                st.session_state.output_image,
                caption="Processed Image",
                use_container_width=True,
            )
            try:
                buf = io.BytesIO()
                # Handle potential RGBA images from processing, save as PNG
                img_to_save = st.session_state.output_image
                output_format = "PNG"  # Default to PNG for broader compatibility (handles transparency)
                mime_type = "image/png"

                # Try to infer original format if not RGBA, but default to PNG is safer
                # Use PNG if alpha channel exists, otherwise try original or fallback to JPEG/PNG
                if img_to_save.mode == "RGBA":
                    output_format = "PNG"
                    mime_type = "image/png"
                else:
                    # If original format known and not GIF (PIL save issues sometimes) use it, else PNG
                    # uploaded_file might be None if app reloads, so safer to stick to PNG/JPEG
                    # input_format = input_image.format if input_image else 'PNG'
                    # if input_format and input_format.upper() in ['JPEG', 'JPG']:
                    #     output_format = 'JPEG'
                    #     mime_type = 'image/jpeg'
                    #     img_to_save = img_to_save.convert('RGB') # Ensure RGB for JPEG
                    # else:
                    output_format = "PNG"  # Safer default
                    mime_type = "image/png"

                img_to_save.save(buf, format=output_format)
                byte_im = buf.getvalue()

                st.download_button(
                    label=f"⬇️ Download Processed Image ({output_format})",
                    data=byte_im,
                    file_name=f"processed_image.{output_format.lower()}",
                    mime=mime_type,
                )
            except Exception as e:
                st.warning(f"Could not create download button: {e}")

        elif st.session_state.input_image_display:  # If no output yet, but input exists
            st.info("🖼️ Processed image will appear here after style transfer.")
        else:
            st.info("🖼️ Upload an image and click 'Start Style Transfer'.")

        # Display status message (updated by actions in col1)
        # Use a key to prevent widget duplication errors if logic reruns
        st.text_area(
            "Status Information",
            value=st.session_state.status_text,
            height=100,
            disabled=True,
            key="status_info_area",
        )

# --- Placeholder Tabs ---
with tab2:
    st.header("🎬 Video Style Transfer")
    st.info("This feature is under development.")

with tab3:
    st.header("🔍 Real-ESRGAN Upscaling (Standalone)")
    st.info("This feature is under development.")

# To run: streamlit run main.py (or your script name)
