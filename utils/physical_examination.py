import streamlit as st
import os
import glob

# Load physical examination text from a file
def load_phys_exam_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"File not found: {file_path}. Please check the file path.")
        return ""

# Function to get examination components from the loaded text
def get_components(text):
    if text:
        component_texts = text.split('\n\n')  # Assuming sections are separated by double newlines
        components = []
        for component_text in component_texts:
            if ':' in component_text:  # Check if the component has a description
                component_name = component_text.split(':', 1)[0].strip()
                components.append(component_name)
        return components
    return []

# Function to display selected examination component text
def display_selected_component(selected_component, text):
    if selected_component:
        component_texts = text.split('\n\n')
        for component_text in component_texts:
            if selected_component.lower() in component_text.lower():
                # Extract text after the first colon
                if ':' in component_text:
                    # Get content after the first colon and remove leading/trailing whitespace
                    content = component_text.split(':', 1)[-1].strip()  
                    st.markdown(content)  # Display only the content, not the title
                break  # Exit after displaying the selected component's content
    else:
        st.write("No component selected.")

# Function to check and display an image if present

def display_image(base_image_name):
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', 
                        '.PNG', '.JPG', '.JPEG', '.GIF', '.BMP', '.TIFF']
    image_found = False

    # Add custom CSS for image container
    st.markdown(
        """
        <style>
        .image-container {
            max-width: 600px; /* Set the max width you desire */
            margin: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Construct a search pattern to find files that contain base_image_name
    for ext in image_extensions:
        pattern = f"*{base_image_name}*{ext}"  # Wildcards before and after the base name
        matching_files = glob.glob(pattern)  # Get a list of matching files

        if matching_files:
            # Wrap your image in a div with the CSS class
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image(matching_files[0], caption="Image interpretation required.")
            st.markdown('</div>', unsafe_allow_html=True)  # Close the div
            image_found = True
            break  # Exit the loop after finding the first matching image

    if not image_found:
        st.write("No images are available.")


# Function to check and display audio if present
def display_audio(base_audio_name):
    audio_extensions = ['.mp3', '.wav', '.ogg', '.flac', '.MP3', '.WAV', '.OGG', '.FLAC']
    audio_found = False

    for ext in audio_extensions:
        audio_path = f"{base_audio_name}{ext}"
        if os.path.isfile(audio_path):
            st.audio(audio_path)
            audio_found = True
            break  # Exit loop if an audio file is found

    if not audio_found:
        st.write("No audio is available.")

# Function to check and display video if present
def display_video(base_video_name):
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.MP4', '.MOV', '.AVI', '.MKV']
    video_found = False

    for ext in video_extensions:
        video_path = f"{base_video_name}{ext}"
        if os.path.isfile(video_path):
            st.video(video_path)
            video_found = True
            break  # Exit loop if a video file is found

    if not video_found:
        st.write("No video is available.")

# Main Streamlit app function
def main():
    st.title("Physical Examination Components")

    st.markdown("""
    Please select and review the physical examination components to help develop your differential diagnosis.
    Please note that any image provided requires interpretation.
    """)

    # Load physical examination text
    text = load_phys_exam_data("phys_exam.txt")

    # Get available components
    components = get_components(text)

    # Only display dropdown if there are components available
    if components:
        # User selection
        selected_component = st.selectbox("Select a physical examination component:", components)

        # Display selected component text
        display_selected_component(selected_component, text)

        # Check for media files based on selected component
        if selected_component == "Image":
            display_image("_peimage_1")  # Check for various formats of image_1
        elif selected_component == "Audio":
            display_audio("_peaudio_1")  # Check for various formats of audio_1
        elif selected_component == "Video":
            display_video("_pevideo_1")  # Check for various formats of video_1

        # Add a submit button to go to the next page
        if st.button("Next", key="pe_submit_button"):
            st.session_state.page = "History Illness Script"  # Change to your actual next page
            st.rerun()  # Rerun the app to reflect the changes
    else:
        st.write("No physical examination components available.")

if __name__ == '__main__':
    main()

