import streamlit as st
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import html
from streamlit_ace import st_ace
import time

def get_language_lexer(language):
    """
    Get the appropriate Pygments lexer for the selected language.
    
    Args:
        language (str): The programming language
        
    Returns:
        Lexer: Pygments lexer for syntax highlighting
    """
    language_map = {
        "Python": "python",
        "JavaScript": "javascript",
        "Java": "java",
        "C#": "csharp"
    }
    
    lexer_name = language_map.get(language, "text")
    try:
        return get_lexer_by_name(lexer_name)
    except:
        return get_lexer_by_name("text")

def render_code_display():
    """
    Render the code display using streamlit-ace for an editor-like experience.
    """
    if st.session_state.file_content is None:
        st.warning("No file content to display.")
        return
    
    st.subheader(f"Code: {st.session_state.file_name}")
    
    # Use a unique key based on the file name and timestamp
    unique_key = f"code_editor_{st.session_state.file_name}_{int(time.time())}"
    
    # Display the code using streamlit-ace with a unique key
    st_ace(
        value=st.session_state.file_content, 
        language=st.session_state.selected_language.lower(), 
        theme="monokai", 
        readonly=True, 
        key=unique_key,
        auto_update=True
    )

