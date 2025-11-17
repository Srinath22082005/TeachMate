import streamlit as st
import os
import json

# Define a simple path to store user data (for demonstration)
# Ensure this directory exists in your project structure: app/memory/
USER_DATA_DIR = "app/memory"
USER_DATA_FILE = os.path.join(USER_DATA_DIR, "user_profiles.json")

# Ensure the directory exists
os.makedirs(USER_DATA_DIR, exist_ok=True)


def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # If file is empty or corrupted, return empty dict and re-initialize
                return {}
    return {}

def save_user_data(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def render():
    st.markdown("## 👤 User Profile")
    st.markdown("Manage your basic profile information here. Your details help personalize your TeachMate AI experience. ✨")

    user_data = load_user_data()
    
    # Get current user's profile, create if not exists
    current_username = st.session_state.get("username", "guest")
    if current_username not in user_data:
        user_data[current_username] = {
            "full_name": "",
            "email": "",
            "role": "",
            "institution": ""
        }
        save_user_data(user_data) # Save new empty profile to file

    user_profile = user_data[current_username]

    st.markdown("<hr style='border: 1px dashed var(--light-blue);'>", unsafe_allow_html=True)
    st.markdown("### My Details")

    with st.container(border=True): # Use a container for the form
        with st.form("user_profile_form"):
            # Prefill values from loaded profile
            full_name = st.text_input("📝 Full Name", value=user_profile.get("full_name", ""), placeholder="e.g., Dr. Jane Doe")
            email = st.text_input("📧 Email Address", value=user_profile.get("email", ""), placeholder="e.g., jane.doe@university.edu")
            # Ensure index is valid for selectbox if value not found
            default_role_index = ["", "Professor", "Lecturer", "Teaching Assistant", "Researcher", "Other"].index(user_profile.get("role", "") if user_profile.get("role", "") in ["", "Professor", "Lecturer", "Teaching Assistant", "Researcher", "Other"] else "")
            role = st.selectbox("🎓 Role", ["", "Professor", "Lecturer", "Teaching Assistant", "Researcher", "Other"], index=default_role_index)
            institution = st.text_input("🏫 Institution / Organization", value=user_profile.get("institution", ""), placeholder="e.g., State University")

            st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True) # Spacer
            submitted = st.form_submit_button("💾 Save Profile")

        if submitted:
            user_profile["full_name"] = full_name
            user_profile["email"] = email
            user_profile["role"] = role
            user_profile["institution"] = institution
            save_user_data(user_data) # Save updated profile back to file
            st.success("✅ Profile updated successfully!")
            st.rerun() # Rerun to display updated data

    st.markdown("---")
    st.markdown("### Current Profile Information")
    # Display current profile info in an attractive box
    if any(user_profile.values()): # Check if any value is set
        st.info(f"""
        **Name:** {user_profile.get("full_name", "_Not set_")}  
        **Email:** {user_profile.get("email", "_Not set_")}  
        **Role:** {user_profile.get("role", "_Not set_")}  
        **Institution:** {user_profile.get("institution", "_Not set_")}
        """)
    else:
        st.warning("Your profile is empty. Please fill in your details above to personalize your experience!", icon="⚠️")