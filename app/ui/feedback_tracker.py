import streamlit as st
import os
import datetime
import json
from dotenv import load_dotenv
from app.agents.feedback_agent import generate_feedback_suggestions
from app.utils.file_exporter import export_to_docx

load_dotenv()
feedback_log_path = "app/memory/feedback_log.json"

def save_feedback(course_name, positive, negative, suggestions, rating=None):
    entry = {
        "course": course_name,
        "timestamp": datetime.datetime.now().isoformat(),
        "what_worked": positive,
        "what_did_not": negative,
        "gemini_suggestion": suggestions,
        "rating": rating
    }

    if os.path.exists(feedback_log_path):
        with open(feedback_log_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = [] # Handle empty or malformed JSON
    else:
        data = []

    data.append(entry)
    with open(feedback_log_path, "w") as f:
        json.dump(data, f, indent=2)

def load_feedback_history():
    if os.path.exists(feedback_log_path):
        with open(feedback_log_path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def render():
    st.markdown("## 📊 Feedback Tracker")
    st.markdown("Log your weekly reflections on course delivery and get smart, actionable suggestions from AI. You can also rate your teaching experience for quick insights! 🚀")

    with st.container(border=True): # Use a container for the form
        st.markdown("### Weekly Reflection")
        with st.form("feedback_form_inner", clear_on_submit=True): # Inner form, clear on submit
            course_name = st.text_input("📚 Course Name", placeholder="e.g., Machine Learning", help="Enter the name of the course you are reflecting on.")
            
            st.markdown("### How was the week overall? (Optional)")
            rating = st.slider("🌟 Rate your week (1-5 stars)", 1, 5, 3, help="Give a quick rating of your overall teaching experience this week.")
            
            st.markdown("### Detailed Feedback")
            positive = st.text_area("✅ What went well this week? (e.g., Student engagement was high during labs)", height=150, help="Describe the positive aspects of your teaching this week.")
            negative = st.text_area("❌ What needs improvement? (e.g., Some students struggled with the advanced topics)", height=150, help="Identify areas where you faced challenges or could do better.")
            
            st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True) # Spacer
            submitted = st.form_submit_button("✨ Generate Suggestions & Log Feedback")

    if submitted:
        if not course_name or not positive or not negative:
            st.error("🚨 All fields (Course Name, What went well, What needs improvement) are required to generate suggestions and log your feedback.")
            return

        with st.spinner("🧠 Analyzing your feedback with Gemini and generating personalized suggestions..."):
            try:
                suggestions = generate_feedback_suggestions(course_name, positive, negative)
                st.success("✅ Suggestions Ready and Feedback Logged!")
                
                st.markdown("### 💡 Gemini's Actionable Suggestions")
                st.info("Based on your reflection, here's what Gemini recommends:")
                st.markdown(suggestions) # Use markdown for potentially richer text output from Gemini

                save_feedback(course_name, positive, negative, suggestions, rating)

                st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True) # Spacer
                st.download_button(
                    label="📥 Download Feedback Summary (.docx)",
                    data=export_to_docx(
                        title=f"{course_name} – Weekly Feedback Summary",
                        content=suggestions,
                        filename=f"{course_name.replace(' ', '_')}_feedback_summary.docx"
                    ),
                    file_name=f"{course_name.replace(' ', '_')}_feedback_summary.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    help="Download the AI-generated suggestions as a Word document."
                )
            except Exception as e:
                st.error(f"❌ An error occurred during feedback analysis: {e}. Please try again later.")
    
    st.markdown("---")
    st.markdown("### 📜 Feedback History")
    feedback_history = load_feedback_history()
    if feedback_history:
        # Display latest feedback first
        for entry in reversed(feedback_history):
            rating_str = "⭐" * entry.get("rating", 0) + " (Not rated)" if entry.get("rating") == 0 else ""
            if entry.get("rating"):
                rating_str = "⭐" * entry["rating"] + f" ({entry['rating']}/5)"
            else:
                rating_str = "_Not rated_"

            with st.expander(f"**{entry['course']}** – {rating_str} – Logged on: {datetime.datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}"):
                st.markdown(f"**✅ What Went Well:** \n{entry['what_worked']}")
                st.markdown(f"**❌ What Needs Improvement:** \n{entry['what_did_not']}")
                st.markdown(f"**💡 Gemini's Suggestions:** \n{entry['gemini_suggestion']}")
                st.markdown("<hr style='border: 0.5px solid var(--light-blue);'>", unsafe_allow_html=True) # Lighter separator
    else:
        st.info("No feedback entries yet. Submit your first reflection above!")