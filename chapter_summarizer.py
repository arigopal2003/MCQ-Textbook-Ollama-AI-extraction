import re
import PyPDF2
from typing import List, Tuple

def extract_mcqs_from_pdf(pdf_path: str) -> List[Tuple[str, List[str]]]:
    """
    Extracts MCQs from a PDF textbook based on common question patterns.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of tuples containing (question, [options...])
    """
    # Patterns to identify MCQ questions
    question_patterns = [
        r'choose\s+the\s+correct\s+answer',
        r'fill\s+in\s+the\s+blanks',
        r'select\s+the\s+correct\s+answer',
        r'which\s+of\s+the\s+following',
        r'correct\s+option'
    ]
    
    # Pattern to identify options (typically a, b, c, d or i, ii, iii, iv)
    option_pattern = r'(?:^|\s)([a-divx]+)\)?\s*(.+?)(?=\s+[a-divx]+\)|$)'
    
    mcqs = []
    current_question = None
    current_options = []
    
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            
            if not text:
                continue
                
            # Split text into lines and process each line
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check if line matches any question pattern (case insensitive)
                if any(re.search(pattern, line, re.IGNORECASE) for pattern in question_patterns):
                    # If we were collecting options for previous question, save it
                    if current_question and current_options:
                        mcqs.append((current_question, current_options))
                        current_question = None
                        current_options = []
                    
                    # This is a new question
                    current_question = line
                
                # Check for options if we're in a question
                elif current_question:
                    # Find all options in the current line
                    options = re.findall(option_pattern, line, re.IGNORECASE)
                    if options:
                        for opt in options:
                            current_options.append(f"{opt[0]}. {opt[1].strip()}")
                    else:
                        # If no options found but line has content, might be continuation of question
                        if line and not line.startswith(('a)', 'b)', 'c)', 'd)', 'i)', 'ii)', 'iii)', 'iv)')):
                            current_question += " " + line
    
    # Add the last question if exists
    if current_question and current_options:
        mcqs.append((current_question, current_options))
    
    return mcqs

def save_mcqs_to_file(mcqs: List[Tuple[str, List[str]]], output_path: str):
    """
    Saves extracted MCQs to a text file.
    
    Args:
        mcqs: List of MCQs from extract_mcqs_from_pdf
        output_path: Path to save the output file
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, (question, options) in enumerate(mcqs, 1):
            f.write(f"Question {i}:\n{question}\n\n")
            f.write("Options:\n")
            for opt in options:
                f.write(f"- {opt}\n")
            f.write("\n" + "="*80 + "\n\n")

if __name__ == "__main__":
    # Replace with your actual PDF path
    pdf_file = "Class_9_Science_English_Medium-2024_Edition-www.tntextbooks.in.pdf"
    output_file = "extracted_mcqs.txt"
    
    print(f"Extracting MCQs from {pdf_file}...")
    mcqs = extract_mcqs_from_pdf(pdf_file)
    
    print(f"Found {len(mcqs)} MCQs. Saving to {output_file}...")
    save_mcqs_to_file(mcqs, output_file)
    
    print("Done!")