import streamlit as st
import os
from dotenv import load_dotenv
from app.agents.assessment_agent import generate_assessment
from app.utils.file_exporter import export_to_docx

load_dotenv()

def render():
    st.markdown("## 📝 Assessment Builder")
    st.markdown("Generate diverse assessment questions including MCQs, short/long answers, and case scenarios, tailored to your course and Bloom's Taxonomy level. Create effective evaluations quickly! 🚀")

    with st.container(border=True): # Use a container for the form
        # Using a proper form for better control over inputs
        with st.form("assessment_form_inner", clear_on_submit=False): 
            st.markdown("### Assessment Criteria")
            col1, col2 = st.columns(2)
            with col1:
                course_name = st.text_input("📚 Course Title", placeholder="e.g., Data Structures", help="Enter the title of the course for this assessment.")
            with col2:
                unit_name = st.text_input("📖 Unit / Module Name", placeholder="e.g., Trees and Graphs", help="Specify the particular unit or module the assessment covers.")
            
            col3, col4 = st.columns(2)
            with col3:
                num_questions = st.slider("🔢 Number of Questions", min_value=5, max_value=20, value=10, help="Choose the desired number of questions to generate.")
            with col4:
                question_type = st.selectbox("❓ Type of Questions", ["MCQs", "Short Answer", "Long Answer", "Case Scenario"], help="Select the format for the questions.")
            
            st.markdown("---") # Simple line for Bloom's level separation
            bloom_level = st.selectbox("🧠 Bloom’s Taxonomy Level", ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"], help="Target a specific cognitive level for the questions.")
            
            st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True) # Spacer
            submitted = st.form_submit_button("✨ Generate Questions")

    if submitted:
        if not course_name or not unit_name:
            st.error("🚨 Please complete both Course Title and Unit / Module Name.")
            return

        with st.spinner("🧠 Generating questions using Gemini... This might take a moment!"):
            try:
                questions_text = generate_assessment(course_name, unit_name, num_questions, question_type, bloom_level)
                st.success("✅ Assessment Questions Generated Successfully!")
                
                st.markdown("### 🧾 Sample Output")
                st.info("Here are your generated assessment questions:")
                st.text(questions_text) # This will adapt to the container width

                st.markdown("<div style='margin-top: 1.5rem;color : white'></div>", unsafe_allow_html=True) # Spacer
                st.download_button( 
                    label="📥 Download Assessment (.docx)",
                    data=export_to_docx(
                        title=f"{course_name} – Assessment Bank ({unit_name})",
                        content=questions_text,
                        filename=f"{course_name.replace(' ', '_')}_{unit_name.replace(' ', '_')}_assessment.docx"
                    ),
                    file_name=f"{course_name.replace(' ', '_')}_{unit_name.replace(' ', '_')}_assessment.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    help="Download your assessment questions as a Word document."
                )
            except Exception as e:
                st.error(f"❌ An error occurred during question generation: {e}. Please check your inputs and try again.")