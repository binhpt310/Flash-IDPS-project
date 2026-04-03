#!/usr/bin/env python3
"""
Update both notebooks for GPU execution and separate output folders
"""

import json
from pathlib import Path

def update_streamspot_local():
    """Update Flash-IDS/streamspot_local.ipynb for GPU"""
    notebook_path = Path("Flash-IDS/streamspot_local.ipynb")
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
            
            # Update device to use GPU
            if 'device = torch.device("cuda" if torch.cuda.is_available() else "cpu")' in source:
                print(f"Cell {i}: Updating device to GPU")
                source = source.replace(
                    'device = torch.device("cuda" if torch.cuda.is_available() else "cpu")',
                    '# GPU Execution\n'
                    'device = torch.device("cuda" if torch.cuda.is_available() else "cpu")\n'
                    'if torch.cuda.is_available():\n'
                    '    print(f"✅ GPU Enabled: {torch.cuda.get_device_name(0)}")\n'
                    '    print(f"   CUDA Version: {torch.version.cuda}")\n'
                    '    print(f"   GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")\n'
                    'else:\n'
                    '    print("⚠️  GPU not available, using CPU")'
                )
                lines = source.split('\n')
                cell['source'] = [line + '\n' if idx < len(lines) - 1 else line for idx, line in enumerate(lines)]
            
            # Update output paths
            if 'OUTPUT_DIR = PROJECT_ROOT / ' in source and 'streamspot' in source:
                print(f"Cell {i}: Updating output path for Flash-IDS")
                source = source.replace(
                    "OUTPUT_DIR = PROJECT_ROOT / 'output' / 'streamspot'",
                    "OUTPUT_DIR = PROJECT_ROOT / 'output' / 'Flash-IDS' / 'streamspot'"
                )
                lines = source.split('\n')
                cell['source'] = [line + '\n' if idx < len(lines) - 1 else line for idx, line in enumerate(lines)]
    
    # Save updated notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print(f"✅ Updated: {notebook_path}")

def update_flash_ids_analysis():
    """Update Flash_IDS_StreamSpot_Analysis.ipynb for GPU and separate output"""
    notebook_path = Path("Flash_IDS_StreamSpot_Analysis.ipynb")
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
            
            # Update output paths
            if 'OUTPUT_DIR = PROJECT_ROOT / ' in source and "'output'" in source:
                print(f"Cell {i}: Updating output path for PIDSMaker-Flash-IDS")
                source = source.replace(
                    "OUTPUT_DIR = PROJECT_ROOT / 'output'",
                    "OUTPUT_DIR = PROJECT_ROOT / 'output' / 'PIDSMaker-Flash-IDS'"
                )
                lines = source.split('\n')
                cell['source'] = [line + '\n' if idx < len(lines) - 1 else line for idx, line in enumerate(lines)]
    
    # Save updated notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print(f"✅ Updated: {notebook_path}")

if __name__ == '__main__':
    print("Updating notebooks for GPU execution...\n")
    update_streamspot_local()
    print()
    update_flash_ids_analysis()
    print("\n✅ All notebooks updated!")
    print("\n📁 Output structure:")
    print("   output/")
    print("   ├── Flash-IDS/")
    print("   │   └── streamspot/     (from streamspot_local.ipynb)")
    print("   └── PIDSMaker-Flash-IDS/")
    print("       └── ...             (from Flash_IDS_StreamSpot_Analysis.ipynb)")
