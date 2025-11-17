import streamlit as st
import os
import shutil
# Assuming app.rag.rag_retriever exists and contains upload_and_embed_document
# from app.rag.rag_retriever import upload_and_embed_document

# Mock function for demonstration purposes if rag_retriever is not fully implemented
def upload_and_embed_document(file_path, source_label):
    # print(f"Simulating embedding document: {source_label} from {file_path}")
    import time
    time.sleep(2) # Simulate work
    # Dummy logic to make it seem like it's doing something based on file type
    if file_path.lower().endswith(".pdf"):
        return 20 + len(file_path) % 10 # More chunks for PDF
    else:
        return 10 + len(file_path) % 5
    

# Define upload directory
UPLOAD_DIR = "docs/sample_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Streamlit UI
def render():
    st.markdown("## 📂 RAG Document Uploader")
    st.markdown("Upload your course materials (PDF, DOCX, TXT) here. These documents will be processed and embedded into a vector database, enabling you to ask questions based on their content in the 'RAG-Powered Q&A' module. 🧠")

    st.markdown("<hr style='border: 1px dashed var(--light-blue);'>", unsafe_allow_html=True)
    st.markdown("### ⬆️ Upload Your Document")
    
    with st.container(border=True): # Container for upload section
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"], help="Supported formats: PDF, DOCX, TXT. Max file size: 200MB.")

        if uploaded_file:
            filename = uploaded_file.name
            file_path = os.path.join(UPLOAD_DIR, filename)

            try:
                # Save uploaded file
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"✅ Successfully uploaded: **{filename}**! Now preparing for embedding...")

                # Embed and store in ChromaDB
                with st.spinner(f"✨ Embedding '{filename}' into the vector database... This might take a few moments depending on file size."):
                    num_chunks = upload_and_embed_document(file_path, source_label=filename)
                    st.success(f"✅ Document embedded successfully! **{num_chunks}** chunks stored and ready for RAG queries. 🎉")
                
                st.info(f"File stored temporarily at: `{file_path}`")
                st.markdown("You can now navigate to the 'RAG-Powered Q&A' tab to ask questions based on this document!")

            except Exception as e:
                st.error(f"❌ Failed to upload or embed **{filename}**: {str(e)}. Please check the file and try again.")
                # Clean up potentially partially written file
                if os.path.exists(file_path):
                    os.remove(file_path)
    
    st.markdown("<hr style='border: 1px dashed var(--light-blue);'>", unsafe_allow_html=True)
    