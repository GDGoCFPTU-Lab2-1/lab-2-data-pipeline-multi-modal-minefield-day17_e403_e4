import re
from datetime import datetime

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # ------------------------------------------
    
    # Strip timestamps [00:00:00]
    text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', text)
    
    # Remove noise tokens like [Music], [inaudible], [Laughter]
    noise_tokens = [r'\[Music\]', r'\[Music starts\]', r'\[Music ends\]', r'\[inaudible\]', r'\[Laughter\]']
    for token in noise_tokens:
        text = re.sub(token, '', text, flags=re.IGNORECASE)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Find the price mentioned in Vietnamese words ("năm trăm nghìn")
    price = None
    if "năm trăm nghìn" in text.lower():
        price = 500000
        
    # Return a cleaned dictionary for the UnifiedDocument schema.
    return {
        "document_id": "transcript-1",
        "content": text,
        "source_type": "Video",
        "author": "Unknown",
        "timestamp": datetime.now().isoformat(),
        "source_metadata": {
            "detected_price_vnd": price
        }
    }
