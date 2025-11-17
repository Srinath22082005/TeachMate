import streamlit as st
import os
import datetime
from dotenv import load_dotenv

# Import copilot agent
from app.agents.copilot_agent import get_copilot_response

# Load env
load_dotenv()

# Streamlit Co-Pilot UI
def render():
    st.markdown("## 🤖 AI Co-Pilot")
    st.markdown("Your intelligent assistant for all teaching-related queries! Ask anything about course planning, content delivery, classroom management, and more. 🚀")

    st.markdown("<hr style='border: 1px dashed var(--light-blue);'>", unsafe_allow_html=True)

    # Chat history display area
    st.markdown("""
    <div class="chat-container">
        <div id="chat-history-scroll-area" class="chat-history-scroll-area">
    """, unsafe_allow_html=True) # Renamed class for clarity
    
    # --- Initialize session state for copilot_history if it doesn't exist ---
    if "copilot_history" not in st.session_state:
        st.session_state["copilot_history"] = []

    # Display chat history within the scrollable area
    # Use st.session_state["copilot_history"] which is initialized in streamlit_app.py
    for chat in st.session_state["copilot_history"]:
        if chat["user"]:
            st.markdown(f"""
            <div class="chat-message user-message">
                {chat['user']}
            </div>
            <div class="message-timestamp user-timestamp">{datetime.datetime.fromisoformat(chat['time']).strftime('%I:%M %p')}</div>
            """, unsafe_allow_html=True)
        if chat["ai"]:
            st.markdown(f"""
            <div class="chat-message ai-message">
                {chat['ai']}
            </div>
            <div class="message-timestamp ai-timestamp">{datetime.datetime.fromisoformat(chat['time']).strftime('%I:%M %p')}</div>
            """, unsafe_allow_html=True)

    # JavaScript to scroll to the bottom of the chat history
    st.markdown("""
    <script>
        var objDiv = document.getElementById("chat-history-scroll-area");
        if (objDiv) {
            objDiv.scrollTop = objDiv.scrollHeight;
        }
    </script>
    """, unsafe_allow_html=True)


    # Close chat history scrollable area
    st.markdown("</div>", unsafe_allow_html=True) # Closing chat-history-scroll-area div
    st.markdown("</div>", unsafe_allow_html=True) # Closing chat-container div

    # Chat input area fixed at the bottom of the visible screen portion
    st.markdown("""
    <div class="chat-input-area-fixed">
    """, unsafe_allow_html=True)

    # Use a form for the input and buttons to allow clearing input easily
    with st.form("copilot_chat_form", clear_on_submit=True):
        user_input = st.text_input("✍️ Type your message here...", placeholder="e.g., How to teach recursion visually?", key="copilot_input_form", label_visibility="collapsed")
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            submitted = st.form_submit_button("🚀 Send", use_container_width=True)
        with col_btn2:
            clear_chat = st.form_submit_button("🔄 Clear Chat", use_container_width=True)

        if submitted:
            if not user_input.strip(): # Check for empty string after stripping whitespace
                st.warning("Please type a message before sending.")
                return

            # Append user message immediately for responsiveness
            st.session_state["copilot_history"].append({
                "user": user_input,
                "ai": "", # AI response will be filled later
                "time": datetime.datetime.now().isoformat()
            })
            # To ensure the latest user message appears before AI starts thinking
            st.rerun()

        if clear_chat:
            st.session_state["copilot_history"] = []
            st.success("Chat history cleared!")
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True) # Close chat-input-area-fixed div

    # Logic to generate AI response (placed after the form submission logic)
    # Check if there's a new user message that hasn't received an AI response yet
    if st.session_state["copilot_history"] and not st.session_state["copilot_history"][-1]["ai"]:
        latest_user_message = st.session_state["copilot_history"][-1]["user"]
        with st.spinner("🧠 AI Co-Pilot is thinking..."):
            try:
                reply = get_copilot_response(latest_user_message)
                st.session_state["copilot_history"][-1]["ai"] = reply
                # No need to update timestamp again, user message already has it
                st.rerun() # Rerun to display AI response
            except Exception as e:
                st.error(f"❌ An error occurred while getting a response: {e}. Please try again.")
                # Optionally, mark the last user message as failed or remove it
                if st.session_state["copilot_history"][-1]["user"] == latest_user_message: # Prevent removing if user sent new message
                     st.session_state["copilot_history"][-1]["ai"] = f"Error: {e}" # Indicate error in UI
                     st.rerun()