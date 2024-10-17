# utils.py

import streamlit as st
import os
import requests
import glob

def read_results_from_file():
    try:
        with open('results.txt', 'r') as file:
            diagnoses = [line.strip() for line in file.readlines() if line.strip()]
        return diagnoses
    except Exception as e:
        st.error(f"Error reading dx_list.txt: {e}")
        return []

def display_results_image():
    st.title("Results")
    results = read_results_from_file()
    
    # Insert a blank option at the start of the results list
    results.insert(0, "")  # Add a blank option

    # Create a dropdown in Streamlit for the user to select a result
    selected_result = st.selectbox("Select a result", results)

    # Prepare the corresponding image file name
    image_filename = selected_result.replace(" ", "_") if selected_result else ""
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', 
                       '.JPG', '.JPEG', '.PNG', '.GIF']

    # Look for the image file in the same directory
    image_path = None
    for ext in image_extensions:
        potential_path = f"{image_filename}{ext}"
        if os.path.exists(potential_path):
            image_path = potential_path
            break

    # Display the selected result and the image
    if selected_result and image_path:  # Only show image if a valid result is selected
        st.image(image_path, caption=selected_result, use_column_width=True)

    # Look for radiological images with any prefix
    radiological_images = []
    for ext in image_extensions:
        radiological_images.extend(glob.glob(f"*image_*{ext}"))  # Match any prefix followed by 'image_'

    # Add custom CSS for image container
    st.markdown(
        """
        <style>
        .image-container {
            max-width: 100px; /* Set the max width you desire */
            margin: 10px auto; /* Center the container */
            display: inline-block; /* Align images next to each other */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create options for the dropdown to show "Image 1", "Image 2", etc.
    if radiological_images:
        radiological_options = [f"Image {i + 1}" for i in range(len(radiological_images))]
        selected_radiological_image_index = st.selectbox("Select a radiological image:", [""] + radiological_options)

        # Get the corresponding file path based on the selected index
        if selected_radiological_image_index:
            selected_index = radiological_options.index(selected_radiological_image_index)
            selected_radiological_image = radiological_images[selected_index]

            # Display the selected radiological image with the custom container
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image(selected_radiological_image, caption=selected_radiological_image, use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)  # Close the div

    # Add a button to go to the next page
    if st.button("Next Page", key="results_next_button"):
        st.session_state.page = "Laboratory Features"  # Change to the Simple Success page
        st.rerun()  # Rerun to update the app

# Assuming this is called in your main function
if __name__ == '__main__':
    display_results_image()


