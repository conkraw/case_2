# utils.py

import streamlit as st
import os
import requests

def read_results_from_file():
    try:
        with open('results.txt', 'r') as file:
            diagnoses = [line.strip() for line in file.readlines() if line.strip()]
        return diagnoses
    except Exception as e:
        st.error(f"Error reading dx_list.txt: {e}")
        return []

import streamlit as st
import os
import glob

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
    radiological_images = glob.glob("*_image_*.jpg") + glob.glob("*_image_*.jpeg") + \
                          glob.glob("*_image_*.png") + glob.glob("*_image_*.gif")

    # Create a dropdown for radiological images if any are found
    if radiological_images:
        radiological_options = [os.path.basename(img) for img in radiological_images]
        selected_radiological_image = st.selectbox("Select a radiological image:", [""] + radiological_options)

        # Display the selected radiological image
        if selected_radiological_image:
            st.image(selected_radiological_image, caption=selected_radiological_image, use_column_width=True)

    # Add a button to go to the next page
    if st.button("Next Page", key="results_next_button"):
        st.session_state.page = "Laboratory Features"  # Change to the Simple Success page
        st.rerun()  # Rerun to update the app

