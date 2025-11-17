import streamlit as st

# Import all tab modules
from app.ui import (
    
  
    syllabus_generator,
    lesson_plan_creator,
    assessment_builder,
    resource_recommender,
    feedback_tracker,
    ai_copilot,
    rag_uploader,
    rag_qa
)

# Page configuration
st.set_page_config(
    page_title="TeachMate AI Agent 🎓",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ Global CSS – Light Blue & White Theme
st.markdown(
    """
    <style>
    :root {
        --primary-blue: #007BFF;
        --light-blue: #B0D7EB;
        --very-light-blue: #E6F3F9;
        --white: #FFFFFF;
        --dark-text: #000000; /* Pure black for all text */
        --medium-text: #000000;
        --success-green: #28A745;
        --error-red: #DC3545;
        --warning-orange: #FFC107;
        --info-blue: #2196F3;
        --dark-background-text: #FFFFFF;
    }

    html, body {
        height: 100%;
        color: var(--dark-text) !important;
        margin: 0;
        padding: 0;
    }

    .stApp {
        background-color: var(--very-light-blue);
        color: var(--dark-text) !important;
        font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    }

    /* ✅ Header */
    header {
        background-color: var(--white) !important;
        border-bottom: 1px solid var(--light-blue);
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        color: var(--dark-text) !important;
    }

    /* ✅ Sidebar */
    .stSidebar {
        color: var(--dark-text) !important;
        background-color: var(--white);
        border-right: 1px solid var(--light-blue);
        padding-top: 2rem;
        box-shadow: 2px 0 8px rgba(0, 0, 0, 0.08);
    }
    .stSidebar .st-emotion-cache-1pxazr7 > div {
        font-weight: bold;
        color: var(--dark-text) !important;
    }

    /* ✅ Headings */
    h1, h2, h3, h4, h5, h6 {
        color: var(--dark-text) !important;
        margin-bottom: 1rem;
        font-weight: 600;
    }

    /* ✅ General Text */
    p, .stMarkdown, .stText, .stChatMessage, label , p ,div {
        color: #000000 !important;
    #    background-color : white;
        line-height: 1.6;
    }
    

    /* ✅ Primary Buttons – White Theme */
    .stButton > button {
        background-color: var(--white) !important;
        color: var(--dark-text) !important;
        border: 1px solid var(--light-blue) !important;
        padding: 0.7rem 1.4rem;
        border-radius: 0.5rem;
        font-weight: 600;
        cursor: pointer;
        transition: background-color 0.3s ease-in-out, transform 0.2s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .stButton > button:hover {
        background-color: var(--very-light-blue) !important;
        transform: translateY(-2px);
    }

    /* ✅ Sidebar Logout Button – Light Red */
    .stSidebar .stButton > button {
        background-color: #FFE5E5 !important;
        color: var(--dark-text) !important;
        border: 1px solid #FFB3B3 !important;
    }
    .stSidebar .stButton > button:hover {
        background-color: #FFCCCC !important;
    }

    /* ✅ Form Submit Buttons – Light Blue */
    .stForm button {
        background-color: var(--white) !important;
        color: var(--dark-text) !important;
        border: 1px solid var(--light-blue) !important;
        font-weight: 600;
    }
    .stForm button:hover {
        background-color: var(--very-light-blue) !important;
    }

    /* ✅ Download Button – Light Green */
    .stDownloadButton > button {
        background-color: #E8F5E9 !important;
        color: var(--dark-text) !important;
        border: 1px solid #B2DFDB !important;
        font-weight: 600;
    }
    .stDownloadButton > button:hover {
        background-color: #D0F0D0 !important;
    }

    /* ✅ Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > button,
    .stMultiSelect > div > div > div {
        border-radius: 0.5rem;
        border: 1px solid var(--light-blue);
        padding: 0.75rem;
        color: var(--dark-text) !important;
        background-color: var(--white);
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    /* ✅ Alerts */
    .stAlert {
        border-radius: 0.5rem;
        color: var(--dark-text) !important;
        width: 100% !important;
        padding: 1rem 1.2rem !important;
        margin-bottom: 1rem;
        border-left: 5px solid;
        line-height: 1.6 !important;
        font-size: 0.95rem !important;
        box-sizing: border-box !important;
        word-wrap: break-word !important;
    }
    .stInfo { background-color: #E0F7FA; border-color: var(--info-blue); }
    .stSuccess { background-color: #E8F5E9; border-color: var(--success-green); }
    .stWarning { background-color: #FFF3E0; border-color: var(--warning-orange); }
    .stError { background-color: #FFEBEE; border-color: var(--error-red); }

    /* ✅ Expander */
    .stExpander {
        border: 1px solid var(--light-blue);
        border-radius: 0.5rem;
        background-color: var(--white);
        padding: 0.5rem;
        color: var(--dark-text) !important;
    }
    .stExpander div[role="button"] p {
        color: var(--dark-text) !important;
    }

    /* ✅ Slider */
    .stSlider .st-emotion-cache-1pxazr7.e1y0inbl0 > div {
        color: var(--dark-text) !important;
        font-weight: 600;
    }

    /* ✅ Login Card */
    .login-card {
        background-color: var(--white);
        padding: 3rem;
        border-radius: 1rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        color: var(--dark-text) !important;
    }
    .login-card h1 {
        color: var(--dark-text) !important;
    }
    .login-card p {
        color: var(--dark-text) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)




# 🔐 Hardcoded user credentials (You can replace with DB later)
USERS = {
    "teacher1": "pass123",
    "admin": "adminpass"
}

# 🔐 Login function
def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        # Centering the login card vertically and horizontally
        st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center; min-height: 100vh;">
                <div class="login-card">
                    <h1 style='text-align: center;'>🔐 Welcome to TeachMate AI</h1>
                    <p style='text-align: center; margin-bottom: 2rem;'>Your AI-powered assistant for educators. Please log in to continue.</p>
            """,
            unsafe_allow_html=True
        )

        # Using st.form to group login elements for better submission handling
        with st.form("login_form"):
            username = st.text_input("👤 Username", key="login_username")
            password = st.text_input("🔑 Password", type="password", key="login_password")

            # Using columns for the button to maintain centering within the form
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                submitted = st.form_submit_button("Login", use_container_width=True)

            if submitted:
                if username in USERS and USERS[username] == password:
                    st.success(f"✅ Welcome, {username}! Redirecting to dashboard...")
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
        
        st.markdown('</div></div>', unsafe_allow_html=True) # Close login-card and centering div
    

# New Feature: Dashboard/Welcome Screen
def render_dashboard():
    st.markdown("## 👋 Welcome to TeachMate AI, **" + st.session_state.username + "**!")
    st.markdown("Your personalized AI assistant is ready to help you streamline your teaching tasks. Select a module from the sidebar to get started. 🚀")
    st.markdown("<hr style='border: 1px dashed var(--light-blue);'>", unsafe_allow_html=True)

    st.markdown("### 📊 Quick Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📝 **Syllabus & Lesson Plans**\n\n_Generate structured course outlines and detailed weekly plans._")
    with col2:
        st.success("📚 **Assessments & Resources**\n\n_Build question banks and find relevant learning materials._")
    with col3:
        st.warning("💬 **AI Co-Pilot & RAG**\n\n_Chat with AI or ask questions from your uploaded documents._")
    
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("### ❓ Need Help?")
    st.info("Check out the 'About TeachMate' section in the sidebar for FAQs and usage tips, or chat with the AI Co-Pilot for instant assistance!")


# 🔁 TeachMate Main App UI (only if logged in)
def main_app():
    # Sidebar header
    st.sidebar.title("📘 TeachMate AI Agent")
    st.sidebar.markdown("Empowering educators with AI-powered productivity tools. Your personal teaching assistant! 🚀")
    
    # All available tabs
    TABS = {
        
        "Dashboard 🏠": render_dashboard, # New dashboard tab
        "Syllabus Generator 📝": syllabus_generator.render,
        "Lesson Plan Creator 🗓️": lesson_plan_creator.render,
        "Assessment Builder 📊": assessment_builder.render,
        "Resource Recommender 📚": resource_recommender.render,
        "Feedback Tracker 📈": feedback_tracker.render,
        "Chat with AI Co-Pilot 🤖": ai_copilot.render,
        "RAG Document Uploader 📂": rag_uploader.render,
        "RAG-Powered Q&A ❓": rag_qa.render
    }

    # Sidebar navigation
    st.sidebar.header("🧭 Navigation")
    selected_tab = st.sidebar.radio("Choose a Module:", list(TABS.keys()))
    
    # User info and Logout
    st.sidebar.markdown("---")
    st.sidebar.info(f"👋 Logged in as: **{st.session_state.username}**")
    if st.sidebar.button("🔒 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    # Header title for the main content area
    st.title(f"📚 TeachMate AI Agent – {selected_tab.replace(' 🏠', '').replace(' 📝', '').replace(' 🗓️', '').replace(' 📊', '').replace(' 📚', '').replace(' 📈', '').replace(' 🤖', '').replace(' 📂', '').replace(' ❓', '')} Module")
    st.markdown(f"<hr style='border: 1px solid var(--light-blue);'>", unsafe_allow_html=True) # Light blue separator

    # Render selected tab content
    TABS[selected_tab]()

# 🚀 Run app
if __name__ == "__main__":
    if "logged_in" in st.session_state and st.session_state.logged_in:
        main_app()
    else:
        login()