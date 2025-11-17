import streamlit as st
import os
from dotenv import load_dotenv
from app.agents.syllabus_agent import generate_syllabus
from app.utils.file_exporter import export_to_docx

load_dotenv()

def render():
    st.markdown("## 📘 Syllabus Generator")
    st.markdown("Craft a comprehensive 15-week structured syllabus with ease. Define your course goals, and let AI handle the structure! ✨")

    with st.container(border=True): # Use a container for the form to give it a card-like appearance
        # Using a proper form for better control over inputs
        with st.form("syllabus_form_inner", clear_on_submit=False): 
            st.markdown("### Course Details")
            col1, col2 = st.columns(2)
            with col1:
                course_name = st.text_input("📚 Course Title", placeholder="e.g., Fundamentals of Data Analytics", help="Provide the full title of your course.")
            with col2:
                duration_weeks = st.slider("🗓️ Course Duration (weeks)", min_value=4, max_value=20, value=15, help="Select the total number of weeks for your course.")
            
            st.markdown("### Learning Objectives")
            objectives = st.text_area("🎯 What should students achieve by the end of the course?", 
                                      placeholder="e.g., Students will be able to perform data cleaning, statistical analysis, and data visualization using Python.", 
                                      height=150, help="List the key learning outcomes for your students.")
            
            st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True) # Spacer
            submitted = st.form_submit_button("✨ Generate Syllabus")

    if submitted: # This `if submitted` block is executed only after the form is submitted
        if not course_name or not objectives:
            st.error("🚨 Please fill all required fields: Course Title and Learning Objectives.")
            return

        with st.spinner("🧠 Generating your detailed syllabus using Gemini... This might take a moment!"):
            try:
                syllabus_text = generate_syllabus(course_name, objectives, duration_weeks)
                st.success("✅ Syllabus Generated Successfully!")
                
                st.markdown(f"### 📖 {course_name} – Weekly Plan")
                st.markdown("<hr style='border: 1px dashed var(--light-blue);'>", unsafe_allow_html=True) # Consistent dashed line
                st.text(syllabus_text)

                st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True) # Spacer
                st.download_button(
                    label="📥 Download Syllabus (.docx)",
                    data=export_to_docx(
                        title=f"{course_name} – Syllabus",
                        content=syllabus_text,
                        filename=f"{course_name.replace(' ', '_')}_syllabus.docx"
                    ),
                    file_name=f"{course_name.replace(' ', '_')}_syllabus.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    help="Click to download your generated syllabus as a Word document."
                )
            except Exception as e:
                st.error(f"❌ An error occurred during syllabus generation: {e}. Please try again.")