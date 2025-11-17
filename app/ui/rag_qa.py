import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
# from app.rag.rag_retriever import retrieve_similar_context

# Mock function for demonstration if rag_retriever is not fully implemented
def retrieve_similar_context(query):
    # print(f"Simulating context retrieval for query: '{query}'")
    import time
    time.sleep(1.5) # Simulate work
    if "data structures" in query.lower():
        return ["Data structures are ways of organizing data in a computer so that it can be used efficiently.",
                "Common data structures include arrays, linked lists, trees, graphs, and hash tables."]
    elif "recursion" in query.lower():
        return ["Recursion is a programming technique where a function calls itself.",
                "It's often used for problems that can be broken down into smaller, self-similar subproblems. A base case is crucial to prevent infinite loops."]
    else:
        return ["No specific context found for your query in the current dummy setup. Please try uploading relevant documents in the 'RAG Document Uploader' tab for real context retrieval.",
                "The RAG system enhances AI responses by providing specific information from your documents."]


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def render():
    st.markdown("## 📖 RAG-Powered Q&A")
    st.markdown("Ask questions based on the documents you've uploaded in the 'RAG Document Uploader' tab. Get precise answers directly from your course materials! 🎯")

    st.markdown("<hr style='border: 1px dashed var(--light-blue);'>", unsafe_allow_html=True)
    st.markdown("### ❓ Ask Your Question")
    
    with st.container(border=True): # Container for the question section
        user_query = st.text_input("✍️ Enter your question here:", placeholder="e.g., What are the main types of data structures?", key="rag_qa_input")

        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("🤖 Answer with Context", use_container_width=True):
                if not user_query:
                    st.warning("Please enter a question to get an answer.")
                    return

                st.markdown("<hr style='border: 1px dashed var(--light-blue);'>", unsafe_allow_html=True)
                with st.spinner("🧠 Retrieving context from your uploaded documents and generating an answer with Gemini..."):
                    try:
                        context_chunks = retrieve_similar_context(user_query)

                        # Check if context is truly empty or just the dummy "no context" message
                        is_context_found = not (not context_chunks or all("No specific context found" in chunk for chunk in context_chunks))

                        if not is_context_found:
                            st.warning("⚠️ No direct relevant context found in your uploaded documents for this query. Gemini will try to answer based on its general knowledge. For document-specific answers, ensure relevant files are uploaded and try again.")
                            context = "" # No context for prompt if not found
                        else:
                            context = "\n".join(context_chunks)
                            with st.expander("📝 Click to view retrieved context (from your documents)"):
                                st.text(context) # This will adapt to the container's width
                            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True) # Spacer

                        prompt = f"""
                        You are an AI assistant designed to answer questions based on provided context.
                        If the context is insufficient or not provided, state that you are answering based on your general knowledge.

                        Context:
                        {context if context else "No specific context provided."}

                        Question:
                        {user_query}

                        Please provide a comprehensive answer. If your answer heavily relies on the provided context, please cite it using where x is the source given in the context.
                        If no context is provided, state that your answer is based on general knowledge.
                        """

                        response = model.generate_content(prompt)
                        st.success("✅ Gemini's Answer:")
                        st.markdown(response.text) # Use markdown to render potential formatting from Gemini

                    except Exception as e:
                        st.error(f"❌ An error occurred while generating the answer: {e}. Please try again.")
        # No else for col_btn2 as it's just an empty space holder
    
    st.markdown("<hr style='border: 1px dashed var(--light-blue);'>", unsafe_allow_html=True)
   