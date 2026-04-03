# Flash-IDS Visualization & Research

Research repository for **Flash-IDS** (Fast Hierarchical Anomaly Detection System) — a provenance-based intrusion detection system using Graph Neural Networks, published at **IEEE S&P 2024**.

**Paper**: [Flash: A Comprehensive Approach to Intrusion Detection via Provenance Graph Representation Learning](https://www.computer.org/csdl/proceedings-article/sp/2024/313000a139/1Ub23WQw20U)  
**Official Repo**: https://github.com/DART-Laboratory/Flash-IDS

---

## 📓 Visualization Notebooks

This repository contains **interactive visualization notebooks** for Flash-IDS across three DARPA TC datasets. Each notebook loads pre-trained Word2Vec + GraphSAGE models and produces 10+ publication-ready figures with academic analysis.

| Notebook | Dataset | Format | Visualizations |
|----------|---------|--------|----------------|
| [`Flash_IDS_CADETS_Visualization.ipynb`](Flash_IDS_CADETS_Visualization.ipynb) | CADETS | JSON Lines (CDM v18) | Architecture, t-SNE, provenance graph, confusion matrix, confidence distribution, dashboard |
| [`Flash_IDS_OPTC_Visualization.ipynb`](Flash_IDS_OPTC_Visualization.ipynb) | OPTC | Bro/Zeek TSV (gzip) | Architecture, t-SNE, provenance graph, confusion matrix, confidence distribution, dashboard |
| [`Flash_IDS_StreamSpot_Visualization.ipynb`](Flash_IDS_StreamSpot_Visualization.ipynb) | StreamSpot | Tab-separated stream logs | Architecture, t-SNE, provenance graph, confusion matrix, confidence distribution, dashboard |

### What each notebook does

1. **Load pre-trained models** — Word2Vec (30-dim) and GraphSAGE (32 hidden, 6-class)
2. **Visualize architecture** — Flash-IDS pipeline diagram
3. **t-SNE embeddings** — 2D projection of Word2Vec node embeddings
4. **Provenance graph** — Graph structure with node/edge type coloring
5. **Confidence distribution** — Anomaly score histogram
6. **Confusion matrix** — Per-class classification performance
7. **Complete dashboard** — Evaluation summary
8. **Interactive 3D graph** — Plotly-based provenance graph with click-to-inspect (CADETS)

### Output

All figures are saved to `output/{Dataset}_Visualization/`:

```
output/
├── CADETS_Visualization/
│   ├── flash_ids_architecture.png
│   ├── word2vec_tsne_2d.png
│   ├── provenance_graph.png
│   ├── confidence_distribution.png
│   ├── confusion_matrix.png
│   ├── complete_dashboard.png
│   └── provenance_graph_full_interactive.html
├── OPTC_Visualization/
│   ├── flash_ids_architecture.png
│   ├── word2vec_tsne_2d.png
│   ├── provenance_graph.png
│   ├── confidence_distribution.png
│   ├── confusion_matrix.png
│   ├── complete_dashboard.png
│   └── provenance_graph_optc_interactive.html
└── StreamSpot_Visualization/
    ├── flash_ids_architecture.png
    ├── word2vec_tsne_2d.png
    ├── provenance_graph.png
    ├── confidence_distribution.png
    ├── confusion_matrix.png
    ├── complete_dashboard.png
    └── provenance_graph_streamspot_interactive.html
```

---

## 🚀 Quick Start

### 1. Setup

```bash
cd Flash-IDPS-project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Install additional dependencies

```bash
pip install plotly   # For interactive 3D graphs
pip install gensim   # For Word2Vec model loading
pip install torch torch-geometric  # For GraphSAGE
```

### 3. Place pre-trained models

Copy trained weights into the appropriate folders:

```
Flash-IDS/trained_weights/
├── cadets/
│   ├── word2vec_cadets_E3.model
│   └── lword2vec_gnn_cadets0_E3.pth
├── optc/
│   ├── word2vec_optc_E3.model
│   └── lword2vec_gnn_optc0_E3.pth
└── streamspot/
    ├── word2vec_streamspot_E3.model
    └── lword2vec_gnn_streamspot0_E3.pth
```

### 4. Run a notebook

```bash
jupyter notebook Flash_IDS_CADETS_Visualization.ipynb
```

Execute cells from top to bottom. All visualizations will be generated automatically.

---

## 🔬 Flash-IDS Method

```
Raw Logs → Graph Construction → Word2Vec Embeddings → GraphSAGE → Confidence Scoring
  ↓              ↓                    ↓                   ↓              ↓
System logs   Provenance graph   30-dim vectors    2-layer GNN    Anomaly detection
(JSON/CDM)    (nodes + edges)    (semantic sim)    (32 hidden)    (confidence score)
```

### Key components

| Component | Technology | Configuration |
|-----------|------------|---------------|
| **Word2Vec** | Gensim | 30-dim embeddings, window=5 |
| **GraphSAGE** | PyTorch Geometric | 2 layers, Mean aggregator, 32 hidden, 6 classes |
| **Anomaly Detection** | Confidence-based | `(P(class₁) - P(class₂)) / P(class₁)` |

### Datasets

| Dataset | Format | Size | Node Types | Attack Scenarios |
|---------|--------|------|------------|-----------------|
| **CADETS** | JSON Lines (CDM v18) | ~15M records | Process, File, Socket, Dir, Memory, NetFlow | Data exfiltration, privilege escalation, lateral movement |
| **OPTC** | Bro/Zeek TSV (gzip) | ~1.1 MB | Same as above | Same as above |
| **StreamSpot** | Tab-separated streams | 1200 files (4.5 GB) | Same as above | Same as above |

---

## 📁 Repository Structure

```
Flash-IDPS-project/
├── README.md
├── requirements.txt
├── .gitignore
├── Flash_IDS_CADETS_Visualization.ipynb      # CADETS visualization + analysis
├── Flash_IDS_OPTC_Visualization.ipynb        # OPTC visualization + analysis
├── Flash_IDS_StreamSpot_Visualization.ipynb  # StreamSpot visualization + analysis
├── Flash_IDS_CADETS_Visualization.html       # HTML export
├── scripts/                                   # Utility scripts
├── output/                                    # Generated visualizations (git-ignored)
├── Flash-IDS/                                 # Original Flash-IDS repo (git-ignored, submodule)
├── PIDSMaker/                                 # PIDSMaker framework (git-ignored, submodule)
├── data/                                      # Datasets (git-ignored)
└── venv/                                      # Virtual environment (git-ignored)
```

> **Note**: `Flash-IDS/`, `PIDSMaker/`, `data/`, and `output/` are separate git repositories or large folders tracked independently. They are excluded from this repo's `.gitignore`.

---

## 📈 Expected Results

From Flash-IDS paper (IEEE S&P 2024):

| Dataset | Precision | Recall | F1 Score |
|---------|-----------|--------|----------|
| OpTC | 0.94 | 0.96 | 0.95 |
| CADETS | 0.93 | 0.95 | 0.94 |
| StreamSpot | 0.91 | 0.93 | 0.92 |

StreamSpot evaluation with pre-trained weights (`streamspot_local.ipynb`):

```
Precision: 1.0
Recall: 0.95
F1-Score: 0.974
```

---

## 📖 References

1. **Flash-IDS Paper**: Rehman, M. U., Ahmadi, H., & Hassan, W. U. "FLASH: A Comprehensive Approach to Intrusion Detection via Provenance Graph Representation Learning." *IEEE Symposium on Security and Privacy (S&P)*, 2024.
2. **Official Repo**: https://github.com/DART-Laboratory/Flash-IDS
3. **PIDSMaker**: https://github.com/ubc-provenance/PIDSMaker
4. **StreamSpot Dataset**: https://github.com/sbustreamspot/sbustreamspot-data

---

*Last updated: 2026-04-03*
