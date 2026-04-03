#!/usr/bin/env python3
"""
Fix streamspot_local.ipynb to use DATA_DIR correctly - FIXED VERSION
"""

import json
import re
from pathlib import Path

NOTEBOOK_PATH = Path(__file__).parent.parent / "Flash-IDS" / "streamspot_local.ipynb"

def fix_notebook():
    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] != 'code':
            continue
            
        source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
        original_source = source
        
        # Fix: open(f"streamspot/{i}.txt") -> open(DATA_DIR / f"{i}.txt")
        # Need to preserve the {i} variable syntax
        source = source.replace('open(f"streamspot/{i}.txt")', 'open(DATA_DIR / f"{i}.txt")')
        source = source.replace("open(f'streamspot/{i}.txt')", 'open(DATA_DIR / f"{i}.txt")')
        
        # Fix any remaining streamspot/ paths with f-strings
        source = re.sub(r'open\(DATA_DIR / f"i\.txt"\)', r'open(DATA_DIR / f"{i}.txt")', source)
        
        if source != original_source:
            print(f"Fixed cell {i}")
            lines = source.split('\n')
            cell['source'] = [line + '\n' if idx < len(lines) - 1 else line 
                             for idx, line in enumerate(lines)]
    
    # Save fixed notebook
    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print(f"\n✅ Fixed notebook saved to: {NOTEBOOK_PATH}")

if __name__ == '__main__':
    fix_notebook()
