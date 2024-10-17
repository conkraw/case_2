import streamlit as st
from utils.session_management import collect_session_data
from utils.firebase_operations import upload_to_firebase

def load_existing_examination(db, document_id):
    collection_name = st.secrets["FIREBASE_COLLECTION_NAME"]
    user_data = db.collection(collection_name).document(document_id).get()
    
    if user_data.exists:
        return user_data.to_dict().get("excluded_exams", []), user_data.to_dict().get("confirmed_exams", [])
    return [], []

def display_focused_physical_examination(db, document_id):
    st.title("Focused Physical Examination Selection")

    if 'excluded_exams' not in st.session_state or 'confirmed_exams' not in st.session_state:
        excluded_exams, confirmed_exams = load_existing_examination(db, document_id)
        st.session_state.excluded_exams = excluded_exams
        st.session_state.confirmed_exams = confirmed_exams

    options1 = [
        "General Appearance", "Eyes", "Ears, Neck, Throat",
        "Lymph Nodes", "Cardiovascular", "Lungs",
        "Skin", "Abdomen", "Extremities",
        "Musculoskeletal", "Neurological", "Psychiatry", "Genitourinary"
    ]

    st.markdown("<h5>Please select the parts of physical examination required:</h5>", unsafe_allow_html=True)
    selected_exams1 = st.multiselect("Select options to exclude:", options1, default=st.session_state.excluded_exams, key="exclude_exams")

    st.markdown("<h5>Please select examinations necessary to confirm the most likely hypothesis:</h5>", unsafe_allow_html=True)
    selected_exams2 = st.multiselect("Select options to confirm:", options1, default=st.session_state.confirmed_exams, key="confirm_exams")

    if st.button("Submit", key="focused_pe_submit_button"):
        if not selected_exams1:
            st.error("Select at least one examination to exclude.")
        elif not selected_exams2:
            st.error("Select at least one examination to confirm.")
        else:
            st.session_state.excluded_exams = selected_exams1
            st.session_state.confirmed_exams = selected_exams2
            
            entry = {
                'excluded_exams': st.session_state.excluded_exams,
                'confirmed_exams': st.session_state.confirmed_exams,
            }

            session_data = collect_session_data()
            upload_message = upload_to_firebase(db, document_id, entry)
            
            st.success("Your selections have been saved successfully.")
            st.session_state.page = "Physical Examination Components"
            st.rerun()

