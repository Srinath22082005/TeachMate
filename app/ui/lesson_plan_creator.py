import streamlit as st
import os
from dotenv import load_dotenv
from app.agents.lesson_plan_agent import generate_lesson_plan
from app.utils.file_exporter import export_to_docx

load_dotenv()

def render():
    st.markdown("## 🧾 Lesson Plan Creator")
    st.markdown("Generate a detailed weekly lesson plan with specified class time, student level, and learning outcomes. Plan your classes effortlessly! 💡")

    with st.container(border=True): # Use a container for the form
        # Using a proper form for better control over inputs
        with st.form("lesson_plan_form_inner", clear_on_submit=False): 
            st.markdown("### Lesson Plan Details")
            col1, col2 = st.columns(2)
            with col1:
                course_name = st.text_input("📚 Course Title", placeholder="e.g., Fundamentals of AI", help="Enter the main title of your course.")
            with col2:
                num_weeks = st.slider("🗓️ Number of Weeks", min_value=4, max_value=20, value=12, help="Specify how many weeks your lesson plan should cover.")
            
            col3, col4 = st.columns(2)
            with col3:
                class_duration = st.selectbox("⏳ Class Duration per Week", ["1 hour", "2 hours", "3 hours", "4 hours", "5 hours"], help="Choose the total class time per week.")
            with col4:
                difficulty = st.selectbox("🎓 Student Level", ["Beginner", "Intermediate", "Advanced"], help="Select the target audience's proficiency level.")
            
            st.markdown("### Target Learning Outcomes")
            target_outcomes = st.text_area("🎯 Key Learning Outcomes", 
                                            placeholder="e.g., Students will understand neural networks, implement a simple CNN, and evaluate model performance.", 
                                            height=150, help="Outline what students should be able to do by the end of the course/unit.")
            
            st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True) # Spacer
            submitted = st.form_submit_button("✨ Generate Lesson Plan")

    if submitted:
        if not course_name or not target_outcomes:
            st.error("🚨 All fields are required: Course Title and Target Learning Outcomes are mandatory.")
            return

        with st.spinner("🧠 Generating your comprehensive weekly lesson plan using Gemini... This may take a few moments!"):
            try:
                lesson_text = generate_lesson_plan(course_name, class_duration, difficulty, target_outcomes, num_weeks)
                st.success("✅ Lesson Plan Ready!")
                
                st.markdown(f"### 📅 Weekly Lesson Breakdown for {course_name}")
                st.markdown("<hr style='border: 1px dashed var(--light-blue);'>", unsafe_allow_html=True)
                st.text(lesson_text)

                st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True) # Spacer
                st.download_button(
                    label="📥 Download Lesson Plan (.docx)",
                    data=export_to_docx(
                        title=f"{course_name} – Lesson Plan",
                        content=lesson_text,
                        filename=f"{course_name.replace(' ', '_')}_lesson_plan.docx"
                    ),
                    file_name=f"{course_name.replace(' ', '_')}_lesson_plan.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    help="Download your generated lesson plan as a Word document."
                )
            except Exception as e:
                st.error(f"❌ An error occurred during lesson plan generation: {e}. Please ensure all details are correct.")