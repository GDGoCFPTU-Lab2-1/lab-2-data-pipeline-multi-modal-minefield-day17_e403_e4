from bs4 import BeautifulSoup
from datetime import datetime

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def parse_html_catalog(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # ------------------------------------------
    
    docs = []
    # Use BeautifulSoup to find the table with id 'main-catalog'
    table = soup.find('table', id='main-catalog')
    if table:
        tbody = table.find('tbody')
        if tbody:
            # Extract rows, handling 'N/A' or 'Liên hệ' in the price column.
            for row in tbody.find_all('tr'):
                cols = [col.text.strip() for col in row.find_all('td')]
                if len(cols) == 6:
                    doc_id, name, category, price, stock, rating = cols
                    if price in ['N/A', 'Liên hệ']:
                        price_val = None
                    else:
                        try:
                            price_val = float(price.replace(',', '').replace(' VND', ''))
                        except:
                            price_val = None
                    
                    # Return a list of dictionaries for the UnifiedDocument schema.
                    doc = {
                        "document_id": f"html-{doc_id}",
                        "content": f"Product: {name}, Category: {category}, Price: {price}, Stock: {stock}, Rating: {rating}",
                        "source_type": "HTML",
                        "author": "VinShop",
                        "timestamp": datetime.now().isoformat(),
                        "source_metadata": {
                            "price": price_val,
                            "category": category,
                            "stock": stock
                        }
                    }
                    docs.append(doc)
    
    return docs
