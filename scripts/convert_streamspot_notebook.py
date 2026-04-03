#!/usr/bin/env python3
"""
Convert Flash-IDS/streamspot.ipynb to run with main venv
- Update paths to use data/ folder
- Add path setup cells
- Update kernel to use default venv kernel
"""

import json
from pathlib import Path

NOTEBOOK_PATH = Path(__file__).parent.parent / "Flash-IDS" / "streamspot.ipynb"
OUTPUT_PATH = Path(__file__).parent.parent / "Flash-IDS" / "streamspot_local.ipynb"

def convert_notebook():
    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Define paths
    PROJECT_ROOT = Path(__file__).parent.parent
    TRAINED_WEIGHTS_DIR = PROJECT_ROOT / "Flash-IDS" / "trained_weights" / "streamspot"
    
    # Add new intro cell
    intro_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Flash Evaluation on StreamSpot Dataset - Local Setup\n",
            "\n",
            "This notebook evaluates Flash on the StreamSpot dataset using the **main project virtual environment**.\n",
            "\n",
            "**Dataset Location:** `data/streamspot/`\n",
            "\n",
            "**Setup:**\n",
            "```bash\n",
            "# Activate main venv\n",
            "source venv/bin/activate\n",
            "\n",
            "# Install StreamSpot dependencies (first time only)\n",
            "bash install_streamspot_deps.sh\n",
            "\n",
            "# Start Jupyter\n",
            "jupyter notebook\n",
            "```\n",
            "\n",
            "**Kernel:** Select `Python 3 (ipykernel)` - the default venv kernel"
        ]
    }
    
    # Add path setup cell
    path_setup_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"tags": []},
        "outputs": [],
        "source": [
            "# Setup paths for local execution\n",
            "import os\n",
            "from pathlib import Path\n",
            "\n",
            "# Get project root (parent of Flash-IDS directory)\n",
            "PROJECT_ROOT = Path.cwd().parent if Path.cwd().name == 'Flash-IDS' else Path.cwd()\n",
            "if PROJECT_ROOT.name != 'Flash-IDPS-project':\n",
            "    # Try to find project root\n",
            "    for parent in Path.cwd().parents:\n",
            "        if (parent / 'data').exists() and (parent / 'Flash-IDS').exists():\n",
            "            PROJECT_ROOT = parent\n",
            "            break\n",
            "\n",
            "# Define paths\n",
            "DATA_DIR = PROJECT_ROOT / 'data' / 'streamspot'\n",
            "MODELS_DIR = PROJECT_ROOT / 'models' / 'streamspot'\n",
            "OUTPUT_DIR = PROJECT_ROOT / 'output' / 'streamspot'\n",
            "TRAINED_WEIGHTS_DIR = PROJECT_ROOT / 'Flash-IDS' / 'trained_weights' / 'streamspot'\n",
            "\n",
            "# Create directories if they don't exist\n",
            "MODELS_DIR.mkdir(parents=True, exist_ok=True)\n",
            "OUTPUT_DIR.mkdir(parents=True, exist_ok=True)\n",
            "TRAINED_WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)\n",
            "\n",
            "print(f\"Project Root: {PROJECT_ROOT}\")\n",
            "print(f\"Data Directory: {DATA_DIR}\")\n",
            "print(f\"Models Directory: {MODELS_DIR}\")\n",
            "print(f\"Output Directory: {OUTPUT_DIR}\")\n",
            "print(f\"Trained Weights: {TRAINED_WEIGHTS_DIR}\")\n",
            "\n",
            "# Verify data exists\n",
            "if DATA_DIR.exists():\n",
            "    graph_files = list(DATA_DIR.glob('*.txt'))\n",
            "    print(f\"\\n✅ Found {len(graph_files)} graph files in {DATA_DIR}\")\n",
            "else:\n",
            "    print(f\"\\n⚠️  Data directory not found: {DATA_DIR}\")\n",
            "    print(\"Please ensure StreamSpot data is in data/streamspot/\")"
        ]
    }
    
    # Insert new cells at beginning
    notebook['cells'].insert(0, intro_cell)
    notebook['cells'].insert(1, path_setup_cell)
    
    # Update existing cells
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'code':
            source = cell['source'] if isinstance(cell['source'], str) else ''.join(cell['source'])
            
            # Update parse_data cell to use existing data
            if 'def parse_data():' in source and 'tar -zxvf all.tar.gz' in source:
                new_source = source.replace(
                    "def parse_data():\n    os.system('tar -zxvf all.tar.gz')",
                    "def parse_data():\n    # Data already extracted in data/streamspot/\n    # Skip extraction step\n    print('Data already available in data/streamspot/')\n    # os.system('tar -zxvf all.tar.gz')  # Uncomment if you need to extract"
                )
                cell['source'] = new_source.split('\n')
                cell['source'] = [line + '\n' if idx < len(new_source.split('\n')) - 1 else line 
                                 for idx, line in enumerate(new_source.split('\n'))]
            
            # Update file paths in training cells
            if 'open(f"streamspot/{i}.txt")' in source:
                new_source = source.replace(
                    'open(f"streamspot/{i}.txt")',
                    'open(DATA_DIR / f"{i}.txt")'
                )
                cell['source'] = new_source.split('\n')
                cell['source'] = [line + '\n' if idx < len(new_source.split('\n')) - 1 else line 
                                 for idx, line in enumerate(new_source.split('\n'))]
            
            # Update model save/load paths
            if 'trained_weights/streamspot/streamspot.model' in source:
                new_source = source.replace(
                    'trained_weights/streamspot/streamspot.model',
                    str(TRAINED_WEIGHTS_DIR / 'streamspot.model')
                )
                cell['source'] = new_source.split('\n')
                cell['source'] = [line + '\n' if idx < len(new_source.split('\n')) - 1 else line 
                                 for idx, line in enumerate(new_source.split('\n'))]
            
            if 'trained_weights/streamspot/lstreamspot.pth' in source:
                new_source = source.replace(
                    'trained_weights/streamspot/lstreamspot.pth',
                    str(TRAINED_WEIGHTS_DIR / 'lstreamspot.pth')
                )
                cell['source'] = new_source.split('\n')
                cell['source'] = [line + '\n' if idx < len(new_source.split('\n')) - 1 else line 
                                 for idx, line in enumerate(new_source.split('\n'))]
            
            # Update torch.load to use map_location for CPU
            if "torch.load(f'trained_weights" in source and 'map_location' not in source:
                new_source = source.replace(
                    "torch.load(f'trained_weights/streamspot/lstreamspot.pth')",
                    "torch.load(TRAINED_WEIGHTS_DIR / 'lstreamspot.pth', map_location=device)"
                )
                cell['source'] = new_source.split('\n')
                cell['source'] = [line + '\n' if idx < len(new_source.split('\n')) - 1 else line 
                                 for idx, line in enumerate(new_source.split('\n'))]
    
    # Update metadata to use default kernel
    notebook['metadata']['kernelspec'] = {
        "display_name": "Python 3 (ipykernel)",
        "language": "python",
        "name": "python3"
    }
    
    # Clear all outputs
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            cell['outputs'] = []
            cell['execution_count'] = None
    
    # Save converted notebook
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print(f"✅ Converted notebook saved to: {OUTPUT_PATH}")
    print(f"\n📌 To run:")
    print(f"   1. source venv/bin/activate")
    print(f"   2. bash install_streamspot_deps.sh  (first time only)")
    print(f"   3. jupyter notebook")
    print(f"   4. Open: Flash-IDS/streamspot_local.ipynb")
    print(f"   5. Select kernel: Python 3 (ipykernel) - DEFAULT")

if __name__ == '__main__':
    convert_notebook()
