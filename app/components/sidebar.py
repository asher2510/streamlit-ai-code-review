import streamlit as st
import os
from app.utils.file_utils import read_file_content
from app.services.code_review import review_code

def render_sidebar():
    """
    Render the sidebar with file upload and language selection options.
    """
    with st.sidebar:
        st.title("AI Code Review")
        st.markdown("---")
        
        # Language selection
        st.subheader("1. Select Language")
        languages = [
            "C#", "Python", "JavaScript", "Java"
        ]
        selected_language = st.selectbox(
            "Programming Language",
            options=languages,
            index=0,
            key="language_selector"
        )
        st.session_state.selected_language = selected_language
        
        st.markdown("---")
        
        # File upload
        st.subheader("2. Upload Code File")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["py", "js", "java", "cs"],
            help="Upload your code file for AI review"
        )
        
        if uploaded_file is not None:
            # Read and store the file content
            file_content = uploaded_file.getvalue().decode("utf-8")
            st.session_state.file_content = file_content
            st.session_state.file_name = uploaded_file.name
            
            st.success(f"File uploaded: {uploaded_file.name}")
            
            st.markdown("---")
            
            # Review button
            st.subheader("3. Start Review")
            if st.button("Review Code", key="review_button"):
                with st.spinner("Analyzing your code..."):
                    # Call the code review service
                    review_results = review_code(
                        file_content=st.session_state.file_content,
                        language=st.session_state.selected_language,
                        file_name=st.session_state.file_name
                    )
                    
                    # Store the review results in session state
                    st.session_state.review_results = review_results
                    
                    st.success("Code review completed!")
        
        st.markdown("---")
        
        # About section
        st.markdown("### About")
        st.markdown("""
        This app uses Groq's powerful language models through LangChain to provide insightful code reviews.
        
        Upload your code file, select the programming language, and get AI-powered suggestions to improve your code.
        """)
        
        # Footer
        st.markdown("---")
        st.markdown("Made with ❤️ using Streamlit and LangChain") 