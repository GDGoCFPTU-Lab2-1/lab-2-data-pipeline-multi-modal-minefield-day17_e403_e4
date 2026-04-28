# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

def run_quality_gate(document_dict):
    content = document_dict.get('content', '')
    
    # Reject documents with 'content' length < 20 characters
    if len(content) < 20:
        return False
        
    # Reject documents containing toxic/error strings (e.g., 'Null pointer exception')
    if 'Null pointer exception' in content:
        return False
        
    # Flag discrepancies (e.g., if tax calculation comment says 8% but code says 10%)
    if '8%' in content and '10%' in content:
        print(f"WARNING: Discrepancy detected in document {document_dict.get('document_id')}")
        
    # Return True if pass, False if fail.
    return True
