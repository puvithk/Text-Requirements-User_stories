
import os
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Function to create numbered headings with bold formatting
def create_numbered_heading(doc, text, num, level=1):
    """Creates a numbered bold heading in the Word document"""
    heading = doc.add_paragraph()
    run = heading.add_run(f'{num} {text}')
    run.font.name = 'Arial'
    run.font.size = Pt(12)  # All text is set to size 12
    run.bold = True  # Make the heading bold
    heading.alignment = WD_ALIGN_PARAGRAPH.LEFT

# Function to create paragraphs with size 12, normal text
def create_paragraph(doc, text):
    """Creates a normal paragraph with size 12 Arial font"""
    paragraph = doc.add_paragraph(text)
    run = paragraph.runs[0]
    run.font.size = Pt(12)  # Standard font size for description
    run.font.name = 'Arial'
    run.bold = False  # Ensure the paragraphs are not bold

# Function to process content into headings and paragraphs
def process_content(doc, content):
    """Processes the content and formats it into the Word document"""
    print(content)
    lines = str(content).strip().split("\n")  # Strip to remove leading/trailing whitespace
    major_heading_num = 1
    sub_heading_num = 1

    for line in lines:
        line = line.strip()  # Remove extra spaces

        # Major headings (e.g., User Registration and Login)
        if line and not line.startswith("As"):  # Major heading if not starting with 'As'
            create_numbered_heading(doc, line, major_heading_num, level=1)
            major_heading_num += 1
            sub_heading_num = 1  # Reset subheading numbering for each major heading

        # Sub-headings (e.g., As a new customer)
        elif line.startswith("As"):
            create_numbered_heading(doc, line, f'{major_heading_num-1}.{sub_heading_num}', level=2)
            sub_heading_num += 1

        # Description paragraphs
        elif line:  # Non-empty lines
            create_paragraph(doc, line)

# Function to generate Word document from uploaded txt file
def generate_word_from_txt(content , File_Name ):
    # Read the content from the uploaded text file
    
    # Create a new Word document
    doc = Document()

    # Set default document style to Arial and size 12
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(12)

    # Process the content and format it into the document
    process_content(doc, content)

    # Save the document as a Word file
    output_file = File_Name.replace(".txt", ".docx")
    doc.save(os.path.join(os.getcwd(),"AllDocuments" ,output_file))
    print(f"Document saved as {output_file}")
    return output_file

if __name__ =="__main__":
    uploaded = files.upload()

    # Step 2: Retrieve the uploaded file path
    for filename in uploaded.keys():
        print(f'Processing file: {filename}')
        output_docx = generate_word_from_txt(filename)

    # Step 3: Download the generated Word file
    files.download(output_docx)
