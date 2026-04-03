#!/usr/bin/env python3
"""
Clean notebook outputs and ensure it's ready for fresh execution
"""

import json
from pathlib import Path

NOTEBOOK_PATH = Path(__file__).parent.parent / "Flash_IDS_StreamSpot_Analysis.ipynb"

def clean_notebook():
    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    cleaned_count = 0
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            # Clear execution count and outputs
            if 'execution_count' in cell and cell['execution_count'] is not None:
                cleaned_count += 1
            cell['execution_count'] = None
            cell['outputs'] = []
    
    # Save cleaned notebook
    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print(f"✅ Cleaned {cleaned_count} cells with cached outputs")
    print(f"   Notebook ready for fresh execution: {NOTEBOOK_PATH}")

if __name__ == '__main__':
    clean_notebook()
