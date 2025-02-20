import streamlit as st
import requests
import json
import pandas as pd

def main():
    st.title("AI Resume Analyzer")
    st.write("Upload your resume for AI-powered analysis")

    # File upload
    uploaded_file = st.file_uploader("Choose a resume file", type=['pdf', 'docx'])
    
    if uploaded_file:
        # Show spinner while processing
        with st.spinner('Analyzing resume...'):
            # Prepare the file for upload
            files = {'file': (uploaded_file.name, uploaded_file, 'application/pdf')}
            
            try:
                # Make API call to Flask backend
                response = requests.post('http://localhost:5000/api/analyze', files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Display results in different sections
                    st.success("Resume analyzed successfully!")
                    
                    # Basic Information
                    st.header("Basic Information")
                    st.write(f"Name: {data['data']['name']}")
                    st.write(f"Email: {data['data']['email']}")
                    
                    # Skills Section
                    st.header("Skills")
                    skills_df = pd.DataFrame(data['data']['skills'], columns=['Skill'])
                    st.table(skills_df)
                    
                    # Education Section
                    st.header("Education")
                    for edu in data['data']['education']:
                        st.write(f"• {edu}")
                    
                    # Download JSON
                    st.download_button(
                        label="Download Analysis Results",
                        data=json.dumps(data['data'], indent=2),
                        file_name="resume_analysis.json",
                        mime="application/json"
                    )
                    
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error occurred')}")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the backend server: {str(e)}")

if __name__ == '__main__':
    main()