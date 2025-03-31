import glob
import PyPDF2
import os

# Path to the directory containing PDF files
pdf_dir = "/Users/zoehoskin/Library/CloudStorage/OneDrive-UniversityofToronto/zoes_project/lit_review_cba_iaq/lit_review_papers/lit_review_papers_for_data_collection/lit_review_papers_data_extracted"

# Get a list of all PDF files in the directory
pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))

# Loop through each PDF file
for pdf_file in pdf_files:
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        
        # Extract text from each page in the PDF
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()

        # Define the output text file name
        text_file = os.path.splitext(pdf_file)[0] + ".txt"
        
        # Write the extracted text to a text file
        with open(text_file, 'w', encoding='utf-8') as output_file:
            output_file.write(text)

    print(f"Text extracted and saved for {pdf_file}")
