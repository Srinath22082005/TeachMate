import streamlit as st
import os
from dotenv import load_dotenv
from app.agents.resource_agent import generate_resources
from app.utils.file_exporter import export_to_docx

load_dotenv()

def render():
    st.markdown("## 🔍 Resource Recommender")
    st.markdown("Get curated academic resources like videos, blogs, papers, and more, based on your topic and learning level. Enhance your teaching materials with relevant content! 🌟")

    with st.container(border=True): # Use a container for the form
        # Using a proper form for better control over inputs
        with st.form("resource_form_inner", clear_on_submit=False): 
            st.markdown("### Resource Search Criteria")
            col1, col2 = st.columns(2)
            with col1:
                subject = st.text_input("💡 Topic / Concept", placeholder="e.g., Natural Language Processing", help="Enter the specific topic or concept you need resources for.")
            with col2:
                difficulty = st.selectbox("🎓 Student Level", ["Beginner", "Intermediate", "Advanced"], help="Select the appropriate difficulty level for the resources.")
            
            st.markdown("### Preferred Resource Types")
            format_types = st.multiselect(
                "📄 Choose Resource Formats",
                ["YouTube Videos", "Blogs", "Slides (PPT)", "PDFs", "Research Papers", "Lab Assignments", "Case Studies"],
                default=["YouTube Videos", "PDFs"],
                help="Select one or more types of resources you'd like to receive."
            )
            
            st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True) # Spacer
            submitted = st.form_submit_button("✨ Generate Resources")

    if submitted:
        if not subject or not format_types:
            st.error("🚨 Please fill the Topic and choose at least one Preferred Resource Type.")
            return

        with st.spinner("🧠 Generating suggestions using Gemini... This might take a moment to find the best resources!"):
            try:
                resources_text = generate_resources(subject, difficulty, format_types)
                st.success("✅ Resources Generated Successfully!")
                
                st.markdown("### 📚 Suggested Resources")
                st.info(f"Here are some recommended resources for '{subject}' at '{difficulty}' level:")
                st.text(resources_text)

                st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True) # Spacer
                st.download_button(
                    label="📥 Download Resources (.docx)",
                    data=export_to_docx(
                        title=f"{subject} – Suggested Resources",
                        content=resources_text,
                        filename=f"{subject.replace(' ', '_')}_resources.docx"
                    ),
                    file_name=f"{subject.replace(' ', '_')}_resources.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    help="Download the list of suggested resources as a Word document."
                )
            except Exception as e:
                st.error(f"❌ An error occurred during resource generation: {e}. Please check your inputs.")