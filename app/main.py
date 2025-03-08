import streamlit as st
import os
from dotenv import load_dotenv
import sys

# Add the app directory to the path so we can import from our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import components
from app.components.sidebar import render_sidebar
from app.components.code_display import render_code_display
from app.components.review_display import render_review_display
from app.services.code_review import review_code
from app.utils.file_utils import read_file_content

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Code Review",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
with open(os.path.join(os.path.dirname(__file__), "static/css/style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    # Initialize session state variables if they don't exist
    if "file_content" not in st.session_state:
        st.session_state.file_content = None
    if "review_results" not in st.session_state:
        st.session_state.review_results = None
    if "selected_language" not in st.session_state:
        st.session_state.selected_language = "Python"
    if "file_name" not in st.session_state:
        st.session_state.file_name = None
    
    # Render sidebar with file upload and language selection
    render_sidebar()
    
    # Main content area
    st.title("AI Code Review")
    
    # Display content only if a file has been uploaded
    if st.session_state.file_content is not None:
        # Display the code with highlighted issues
        render_code_display()
        
        # Display review results only if available
        if st.session_state.review_results is not None:
            # Display the code review results
            render_review_display()
    else:
        # Display instructions when no file is uploaded
        st.info("👈 Please upload a file from the sidebar to get started.")
        
        # Show example of what the app does
        st.markdown("""
        ## How it works
        
        1. **Select a programming language** from the dropdown in the sidebar
        2. **Upload your code file** using the file uploader
        3. **Click the "Review Code" button** to analyze your code
        4. **View the AI-generated code review** alongside your code with highlighted issues
        
        This app uses Groq's powerful language models through LangChain to provide insightful code reviews.
        """)

if __name__ == "__main__":
    main() 