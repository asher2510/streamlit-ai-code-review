import os
import tempfile

def read_file_content(file_path):
    """
    Read the content of a file.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Content of the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def save_uploaded_file(uploaded_file):
    """
    Save an uploaded file to a temporary location.
    
    Args:
        uploaded_file (UploadedFile): The uploaded file object from Streamlit
        
    Returns:
        str: Path to the saved file
    """
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            # Write the uploaded file content to the temporary file
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        return None

def get_file_extension(file_name):
    """
    Get the extension of a file.
    
    Args:
        file_name (str): Name of the file
        
    Returns:
        str: Extension of the file
    """
    return os.path.splitext(file_name)[1].lower()

def map_extension_to_language(extension):
    """
    Map a file extension to a programming language.
    
    Args:
        extension (str): File extension (including the dot)
        
    Returns:
        str: Programming language name
    """
    extension_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.java': 'Java',
        '.cs': 'C#',
        '.cpp': 'C++',
        '.c': 'C',
        '.go': 'Go',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.rs': 'Rust',
        '.html': 'HTML',
        '.css': 'CSS'
    }
    
    return extension_map.get(extension, 'Unknown') 