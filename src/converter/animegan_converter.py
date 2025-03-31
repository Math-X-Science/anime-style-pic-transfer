import streamlit as st
from PIL import Image
import io  # Required for handling byte streams if needed

# Assuming these imports work and contain the necessary definitions
try:
    from converter._typing import ModelName, Resolution, Scale
    from converter.api import animegan_picture_transfer, save_image
    # Get choices (handle potential errors if typing is complex)
    try:
        model_choice = list(ModelName.__args__) # type: ignore
    except AttributeError:
        st.warning("Could not dynamically get ModelName choices. Using placeholders.")
        model_choice = ["ModelA", "ModelB", "ModelC"] # Placeholder
    # resolution_choice seems unused in active Gradio code, using Slider instead
    # scale_choice seems unused in active Gradio code
except ImportError:
    st.error("Failed to import converter modules. Please ensure the 'converter' package is installed and accessible.")
    # Define dummy functions and choices for UI layout preview
    def animegan_picture_transfer(image, upscale):
        st.warning("`animegan_picture_transfer` not found. Displaying input image.")
        if image:
             return image.copy() # Return a copy to avoid modifying original
        return None
    def save_image(image, resolution):
        st.warning("`save_image` not found.")
        if image:
            return f"Save action simulated for image with resolution {resolution}."
        return "Save action requires an image."
    model_choice = ["ModelA", "ModelB", "ModelC"] # Placeholder
    # resolution_choice = [240, 480, 720, 1080] # Placeholder
    # scale_choice = [2, 4, 8] # Placeholder

# --- Streamlit App ---

st.set_page_config(layout="wide")
st.title("🖼️ Image Style Transfer and Tools")

# --- Session State Initialization ---
if 'output_image' not in st.session_state:
    st.session_state.output_image = None
if 'status_text' not in st.session_state:
    st.session_state.status_text = ""
if 'input_image_display' not in st.session_state:
    st.session_state.input_image_display = None

# --- UI Layout ---

tab1, tab2, tab3 = st.tabs(["🎨 Image-to-Image", "🎬 Video-to-Video (Placeholder)", "🔍 RealESRGAN (Placeholder)"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.header("Input & Settings")
        uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg", "webp"])

        input_image = None # Initialize input_image before the conditional block

        if uploaded_file is not None:
            try:
                # Read the image using PIL
                input_image = Image.open(uploaded_file)
                st.session_state.input_image_display = input_image # Store for display
                # Display the uploaded image
                st.image(input_image, caption="Uploaded Image", use_column_width=True)

                # --- Settings ---
                resolution = st.slider(
                    label="Select Output Resolution (Longest Side):",
                    min_value=120,
                    max_value=1080,
                    value=720,
                    step=30,
                    help="Adjust the desired output resolution."
                )
                st.write(f"Selected Resolution: `{int(resolution)}`")

                upscale = st.checkbox("Enable Upscaling?", value=False, help="Check this box to perform upscaling during transfer.")

                # --- Action Buttons ---
                button_col1, button_col2 = st.columns(2)
                with button_col1:
                    transfer_button = st.button("✨ Start Style Transfer", type="primary", use_column_width=True)
                with button_col2:
                    save_button = st.button("💾 Save Action (Example)", use_column_width=True, help="Calls the save function with the *input* image and resolution setting.")

                # --- Process Actions (Moved Here) ---
                # Process clicks only if the buttons exist (i.e., file uploaded)
                if transfer_button: # No need to check input_image again, it must exist here
                    with st.spinner("🎨 Applying style transfer... Please wait."):
                        try:
                            processed_image = animegan_picture_transfer(input_image, upscale)
                            st.session_state.output_image = processed_image
                            st.session_state.status_text = "✅ Style transfer successful!"
                        except Exception as e:
                            st.session_state.output_image = None
                            st.session_state.status_text = f"❌ Error during style transfer: {e}"
                            st.error(st.session_state.status_text) # Show error immediately

                if save_button: # No need to check input_image again
                    with st.spinner("💾 Processing Save Action..."):
                        try:
                            status = save_image(input_image, int(resolution))
                            # Update status text, don't clear the output image from a previous transfer
                            st.session_state.status_text = f"ℹ️ Save Status: {status}"
                        except Exception as e:
                            # Update status text, don't clear the output image
                            st.session_state.status_text = f"❌ Error during save action: {e}"
                            st.error(st.session_state.status_text) # Show error immediately

            except Exception as e:
                st.error(f"Error loading image: {e}")
                # Reset states if image loading failed
                st.session_state.input_image_display = None
                st.session_state.output_image = None
                st.session_state.status_text = "Failed to load image."
                input_image = None # Ensure input_image is None if loading failed

        else:
            # If no file is uploaded, ensure states reflect that.
            # (input_image is already None from initialization)
            if 'uploader_key' not in st.session_state: st.session_state.uploader_key = 0 # Hack to help reset if needed
            # Optional: Clear previous results when the file is removed by the user
            # This requires a bit more state management or observing the uploader state.
            # For simplicity now, we just show a message.
            st.info("Please upload an image to begin.")
            # Clear previous output if desired when no file is present
            # st.session_state.output_image = None
            # st.session_state.status_text = "Please upload an image."


    with col2:
        st.header("Output")

        # --- Display Output (Remains in col2) ---
        # Always check session state here for what to display
        if st.session_state.output_image:
            st.image(st.session_state.output_image, caption="Processed Image", use_column_width=True)
            try:
                buf = io.BytesIO()
                # Handle potential RGBA images from processing, save as PNG
                img_to_save = st.session_state.output_image
                if img_to_save.mode == 'RGBA':
                     output_format = 'PNG'
                     # Optional: Convert to RGB if PNG transparency is not desired
                     # img_to_save = img_to_save.convert('RGB')
                     # output_format = 'JPEG' # Or keep PNG
                else:
                    output_format = img_to_save.format or 'PNG'

                img_to_save.save(buf, format=output_format)
                byte_im = buf.getvalue()
                st.download_button(
                    label=f"⬇️ Download Processed Image ({output_format})",
                    data=byte_im,
                    file_name=f"processed_image.{output_format.lower()}",
                    mime=f"image/{output_format.lower()}"
                )
            except Exception as e:
                st.warning(f"Could not create download button: {e}")
        elif st.session_state.input_image_display: # If no output yet, but input exists
             st.info("Processed image will appear here after style transfer.")


        # Display status message (updated by actions in col1)
        st.text_area("Status Information", value=st.session_state.status_text, height=100, disabled=True, key="status_area")


# --- Placeholder Tabs ---
with tab2:
    st.header("Video Style Transfer")
    st.info("This feature is not yet implemented.")

with tab3:
    st.header("Real-ESRGAN Upscaling (Testing)")
    st.info("This feature is not yet implemented.")

# To run: streamlit run your_script_name.py