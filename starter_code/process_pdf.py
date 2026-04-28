import google.generativeai as genai
import os
import json

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Use Gemini API to extract structured data from lecture_notes.pdf

def extract_pdf_data(file_path):
    # --- FILE CHECK (Handled for students) ---
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None
    # ------------------------------------------

    # Initialize Gemini API
    if "GEMINI_API_KEY" not in os.environ:
        print("GEMINI_API_KEY not set. Skipping PDF extraction to prevent crash.")
        return None

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        # Load the PDF file
        pdf_file = genai.upload_file(path=file_path)
        
        # Send a prompt to Gemini to extract: Title, Author, and a Summary.
        prompt = "Extract Title, Author, and a 3-sentence summary. Output as pure JSON with exactly these keys: title, author, summary"
        response = model.generate_content([pdf_file, prompt])
        
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]
            
        data = json.loads(text.strip())
        
        # Return a dictionary that fits the UnifiedDocument schema.
        return {
            "document_id": "pdf-001",
            "content": data.get("summary", ""),
            "source_type": "PDF",
            "author": data.get("author", "Unknown"),
            "timestamp": None,
            "source_metadata": {
                "title": data.get("title", "")
            }
        }
    except Exception as e:
        print(f"PDF extraction failed: {e}")
        return None
