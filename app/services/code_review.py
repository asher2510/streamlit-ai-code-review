import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
import json

def review_code(file_content, language, file_name):
    """
    Review code using LangChain and Groq.
    
    Args:
        file_content (str): The content of the code file
        language (str): The programming language
        file_name (str): The name of the file
        
    Returns:
        dict: The review results
    """
    try:
        # Get the Groq API key from environment variables
        groq_api_key = ""
        if not groq_api_key:
            return {
                "summary": "Error: GROQ_API_KEY environment variable not set. Please set your Groq API key in the .env file.",
                "issues": [],
                "recommendations": []
            }
        
        # Initialize the Groq LLM
        llm = ChatGroq(
            api_key=groq_api_key,
            model_name="llama3-70b-8192",  # Using Llama 3 70B model
            temperature=0.2,  # Low temperature for more deterministic responses
            max_tokens=4096  # Adjust based on your needs
        )
        
        # Define the output schema
        issue_schema = ResponseSchema(
            name="issues",
            description="List of issues found in the code",
            type="array",
            items={
                "type": "object",
                "properties": {
                    "lineNumber": {"type": "integer", "description": "Line number where the issue was found"},
                    "lineOfCode": {"type": "string", "description": "The line of code where the issue occurs"},
                    "title": {"type": "string", "description": "Short title describing the issue"},
                    "description": {"type": "string", "description": "Detailed description of the issue"},
                    "suggestion": {"type": "string", "description": "Suggested code to fix the issue"}
                }
            }
        )
        
        recommendation_schema = ResponseSchema(
            name="recommendations",
            description="List of general recommendations for improving the code",
            type="array",
            items={
                "type": "object",
                "properties": {
                    "lineNumber": {"type": "integer", "description": "Line number where the recommendation applies"},
                    "Code": {"type": "string", "description": "The line of code related to the recommendation"},
                    "title": {"type": "string", "description": "Short title describing the recommendation"},
                    "description": {"type": "string", "description": "Detailed description of the recommendation"},
                    "example": {"type": "string", "description": "Example code implementing the recommendation"}
                }
            }
        )
        
        summary_schema = ResponseSchema(
            name="summary",
            description="Overall summary of the code review",
            type="string"
        )
        
        # Create the output parser
        output_parser = StructuredOutputParser.from_response_schemas([
            issue_schema,
            recommendation_schema,
            summary_schema
        ])
        
        # Create the prompt template
        prompt_template = ChatPromptTemplate.from_template("""
            You are an expert code reviewer with deep knowledge of {language} programming. 
            Please review the following code and provide detailed feedback.

            File name: {file_name}

            ```{language}
            {code}
            ```

            Perform a thorough code review focusing on:
            1. Code quality and readability
            2. Potential bugs or errors
            3. Security vulnerabilities
            4. Performance issues
            5. Best practices for {language}
            6. Design patterns and architecture

            For each issue you find, specify:
            - The exact line number where the issue occurs (e.g., Line 10)
            - The line of code where the issue occurs
            - A clear title for the issue (e.g., Insecure Storage of Passwords)
            - A detailed description of why it's an issue
                                                           
            {format_instructions}
        """)
        # Format the prompt with the code and language
        prompt = prompt_template.format(
            language=language,
            code=file_content,
            file_name=file_name,
            format_instructions=output_parser.get_format_instructions()
        )
        
        # Get the response from the LLM
        response = llm.invoke(prompt)

        # Parse the response
        try:
            parsed_response = output_parser.parse(response.content)
            return parsed_response
        except Exception as e:
            # If structured parsing fails, try to extract JSON from the response
            try:
                # Look for JSON-like content in the response
                content = response.content
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = content[start_idx:end_idx]
                    parsed_response = json.loads(json_str)
                    return parsed_response
                else:
                    # Fallback to a simple structure
                    return {
                        "summary": "The code review was completed, but the results couldn't be properly structured.",
                        "issues": [],
                        "recommendations": []
                    }
            except:
                # Last resort fallback
                return {
                    "summary": response.content[:500] + "...",
                    "issues": [],
                    "recommendations": []
                }
    
    except Exception as e:
        # Handle any exceptions
        return {
            "summary": f"Error performing code review: {str(e)}",
            "issues": [],
            "recommendations": []
        } 