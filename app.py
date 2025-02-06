import streamlit as st
import io
import zipfile

def set_page_config():
    """Configure the Streamlit page"""
    st.set_page_config(
        page_title="Code File Generator - AI Engineering",
        page_icon="🚀",
        layout="wide"
    )

def show_header():
    """Display the header with branding"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title("🚀 Code File Generator")
        st.write("""
        Create your application files by pasting the code for each file and specifying its filename.
        All files will be packaged into a downloadable ZIP file.
        """)
    
    with col2:
        st.markdown("""
        <div style='text-align: right; color: #666;'>
            <p>AI Engineering</p>
            <p><a href='https://ai-engineering.ai' target='_blank'>ai-engineering.ai</a></p>
        </div>
        """, unsafe_allow_html=True)

def show_footer():
    """Display the footer with author information"""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Created by Dirk Wonhoefer, 2025<br>
        AI Engineering<br>
        <a href='mailto:dirk.wonhoefer@ai-engineering.ai'>dirk.wonhoefer@ai-engineering.ai</a></p>
    </div>
    """, unsafe_allow_html=True)

def create_zip(files_data):
    """Create a ZIP file containing all the files"""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for filename, content in files_data.items():
            if filename and content:  # Only process if both filename and content exist
                # Ensure content ends with newline
                if not content.endswith('\n'):
                    content += '\n'
                zip_file.writestr(filename, content)
    return zip_buffer.getvalue()

def main():
    set_page_config()
    show_header()
    
    # Initialize session state for dynamic file inputs
    if 'num_files' not in st.session_state:
        st.session_state.num_files = 3  # Start with 3 file inputs
    
    # Dictionary to store file data
    files_data = {}
    
    # Create dynamic file inputs
    for i in range(st.session_state.num_files):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            content = st.text_area(
                f"File content #{i+1}",
                height=150,
                key=f"content_{i}"
            )
        
        with col2:
            filename = st.text_input(
                f"Filename #{i+1}",
                key=f"filename_{i}"
            )
            
        if filename and content:
            files_data[filename] = content
    
    # Button to add more file inputs
    if st.button("Add Another File"):
        st.session_state.num_files += 1
        st.rerun()
    
    # Only show the process button if we have at least one file
    if files_data and st.button("Process Files"):
        # Display preview of detected files
        st.write("### Files to be created:")
        for filename, content in files_data.items():
            st.write(f"- {filename}")
            with st.expander(f"Show content of {filename}"):
                st.code(content)
        
        # Create download button
        zip_data = create_zip(files_data)
        st.download_button(
            label="Download Files as ZIP",
            data=zip_data,
            file_name="generated_files.zip",
            mime="application/zip"
        )
    
    show_footer()

if __name__ == "__main__":
    main() 