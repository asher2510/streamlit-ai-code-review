import streamlit as st
import html

def render_review_display():
    """
    Render the code review results in a structured format.
    """
    if st.session_state.review_results is None:
        st.info("Run the code review to see results here.")
        return
    
    review_results = st.session_state.review_results
    
    # Display the review summary
    st.subheader("Code Review Summary")
    
    with st.container():
        if 'summary' in review_results and review_results['summary']:
            st.markdown(f"""
            <div class="review-summary">
                {html.escape(review_results['summary'])}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No summary available.")
    
    # Display the issues
    st.subheader("Issues Found")
    
    if 'issues' in review_results and isinstance(review_results['issues'], list):
        # Sort issues by line number
        sorted_issues = sorted(
            review_results['issues'], 
            key=lambda x: x.get('lineNumber', float('inf'))
        )
        
        for i, issue in enumerate(sorted_issues):
            if isinstance(issue, dict):
                code_line = html.escape(issue.get('code', 'Code not available'))
                line_number = issue.get('lineNumber', 'N/A')
                with st.expander(
                    f"Issue #{i+1}: {issue.get('title', 'Unnamed Issue')}"
                ):
                    st.markdown(f"""
                    <div class="review-comment">
                        <div class="review-comment-header" style="font-weight: bold; font-size: 1.1em;">
                            {html.escape(issue.get('title', 'Unnamed Issue'))}
                        </div>
                        <div class="review-comment-body" style="margin-top: 10px;">
                            <strong>Description:</strong> {html.escape(issue.get('description', 'No description provided.'))}
                        </div>
                        <div style="background-color: #ffdddd; padding: 10px; margin-top: 10px; border-radius: 5px;">
                            <strong>Line {line_number}:</strong> <code>{code_line}</code>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if 'suggestion' in issue and issue['suggestion']:
                        st.markdown("#### Suggested Fix")
                        st.code(issue['suggestion'], language=st.session_state.selected_language.lower())
    else:
        st.success("No issues found in your code. Great job!")

# Note: Ensure that the 'lineOfCode' and 'lineNumber' keys in the issue dictionary contain the actual line of code and line number.