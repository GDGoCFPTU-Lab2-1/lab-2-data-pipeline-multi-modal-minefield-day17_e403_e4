import pandas as pd
from datetime import datetime
import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.

def parse_price(price_str):
    if pd.isna(price_str) or price_str in ['N/A', 'NULL', 'Liên hệ']:
        return None
    price_str = str(price_str).lower().strip()
    if 'five dollars' in price_str:
        return 5.0
    cleaned = re.sub(r'[^\d\.-]', '', price_str)
    if cleaned == '':
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None

def process_sales_csv(file_path):
    # --- FILE READING (Handled for students) ---
    df = pd.read_csv(file_path)
    # ------------------------------------------
    
    # Remove duplicate rows based on 'id'
    df = df.drop_duplicates(subset=['id'], keep='first')
    
    docs = []
    for _, row in df.iterrows():
        # Clean 'price' column: convert "$1200", "250000", "five dollars" to floats
        price = parse_price(row['price'])
        
        # Normalize 'date_of_sale' into a single format (YYYY-MM-DD)
        try:
            date_of_sale = pd.to_datetime(row['date_of_sale'], format='mixed', dayfirst=True)
            date_str = date_of_sale.strftime('%Y-%m-%d')
        except:
            date_str = None
            
        doc = {
            "document_id": f"csv-{row['id']}",
            "content": f"Product: {row['product_name']}, Category: {row['category']}, Price: {price}, Date: {date_str}, Seller: {row['seller_id']}, Stock: {row['stock_quantity']}",
            "source_type": "CSV",
            "author": "System",
            "timestamp": date_str,
            "source_metadata": {
                "price": price,
                "category": row['category'],
                "seller_id": row['seller_id']
            }
        }
        docs.append(doc)
    
    return docs

