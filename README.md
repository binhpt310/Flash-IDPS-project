# Flash-IDPS Research Project

A personal research repository studying **Flash-IDPS** (Flash Intrusion Detection and Prevention System) through the **PIDSMaker** framework.

---

## 📋 Overview

This repository contains my research and analysis of **Flash-IDPS**, a provenance-based intrusion detection system that uses Graph Neural Networks (GNNs) to detect Advanced Persistent Threats (APTs) by analyzing system audit logs.

### What is Flash-IDPS?

**Flash-IDPS** is a novel intrusion detection system developed by the **DART Laboratory** at Purdue University, published at **IEEE Symposium on Security and Privacy (S&P) 2024**. It leverages:

- **Provenance graph representation learning** to model system activities
- **GraphSAGE** for neighborhood aggregation and node embedding
- **Self-supervised learning** (no labeled attack data required)
- **Word2Vec embeddings** for semantic understanding of system entities

### Key Features

| Feature | Description |
|---------|-------------|
| **Detection Method** | Provenance graph analysis with GNNs |
| **Learning Approach** | Self-supervised (Node Type Prediction) |
| **Attack Coverage** | APTs, multi-stage attacks, C2 communications |
| **Data Sources** | DARPA TC programs (CADETS, E3, THEIA, TRACE) |
| **Architecture** | 8-stage pipeline from raw logs to detection reports |

---

## 📁 Repository Contents

| File/Folder | Description |
|-------------|-------------|
| `Flash_IDPS_Complete_Workflow.ipynb` | Comprehensive Jupyter notebook (1,797 lines) explaining Flash-IDPS architecture and implementation |
| `flash_paper.pdf` | Original IEEE S&P 2024 research paper |
| `Đồ án hệ thống phát hiện xâm nhập .xlsx` | Evaluation criteria spreadsheet (Vietnamese) comparing PIDS frameworks |
| `Dockerfile` | Docker configuration for running the notebook (CPU) |
| `Dockerfile.gpu` | Docker configuration with GPU/CUDA support |
| `docker-compose.yml` | Container orchestration with volume mounts |
| `requirements.txt` | Python dependencies |
| `setup.sh` / `setup.bat` | Automated setup scripts (Linux/Mac & Windows) |
| `notebooks/` | Directory for Jupyter notebooks |
| `data/` | Dataset storage for provenance graphs |
| `models/` | Trained model checkpoints |
| `output/` | Detection results and reports |

---

## 🚀 Quick Start

### Prerequisites

- **Docker** & **Docker Compose** installed
- **Git** for cloning repositories
- At least **10GB free disk space**
- **8GB+ RAM** recommended (16GB for GPU training)

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Docker Setup

```bash
# Build the Docker image
docker-compose build

# Start the Jupyter notebook container
docker-compose up -d

# Access the notebook at: http://localhost:8888
# Check logs for the access token
docker-compose logs
```

### Option 3: Local Installation

```bash
# Create virtual environment
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Clone PIDSMaker
git clone https://github.com/ubc-provenance/PIDSMaker.git
cd PIDSMaker
pip install -e .

# Run Jupyter
jupyter notebook
```

---

## 📚 Learning Resources

### The Notebook

The `Flash_IDPS_Complete_Workflow.ipynb` notebook provides:

1. **System Architecture Overview** - Visual diagrams of the 8-stage pipeline
2. **Provenance Graph Construction** - How audit logs become graphs
3. **Word2Vec Featurization** - Semantic embeddings for system entities
4. **GraphSAGE Encoder** - Neighborhood aggregation implementation
5. **Self-Supervised Training** - Node type prediction objective
6. **Anomaly Detection** - Threshold selection and detection logic
7. **Evaluation Metrics** - ROC curves, precision-recall, confusion matrices

### Key Concepts

| Term | Definition |
|------|------------|
| **Provenance Graph** | Directed graph of system entities (nodes) and causal relationships (edges) |
| **GraphSAGE** | Graph Neural Network that learns node embeddings via neighborhood aggregation |
| **Self-Supervised Learning** | Training on benign data only; anomalies detected via prediction error |
| **Word2Vec** | Embedding technique that captures semantic similarity between entities |
| **APT** | Advanced Persistent Threat - multi-stage, long-duration cyber attacks |

---

## 🔗 Related Repositories & Resources

### Primary Resources

| Resource | URL | Description |
|----------|-----|-------------|
| **PIDSMaker** | https://github.com/ubc-provenance/PIDSMaker | Framework for building provenance-based IDS with neural networks |
| **Flash-IDS (Original)** | https://github.com/DART-Laboratory/Flash-IDS | Official Flash-IDS implementation by DART Laboratory |
| **Flash Paper (IEEE)** | https://www.computer.org/csdl/proceedings-article/sp/2024/313000a139 | IEEE S&P 2024 publication |
| **Flash Paper (PDF)** | https://dartlab.org/assets/pdf/flash.pdf | Direct PDF download |

### Related Projects

| Project | URL | Description |
|---------|-----|-------------|
| **Orthrus** | https://github.com/ubc-provenance/orthrus | High-quality attribution in PIDS (USENIX Sec'25) |
| **DART Lab** | https://dartlab.org/ | Data Analytics for Real-time Threats Laboratory |
| **UBC Provenance** | https://github.com/ubc-provenance | University of British Columbia Provenance Research Group |

### Datasets

| Dataset | Source | Description |
|---------|--------|-------------|
| **DARPA TC** | https://www.darpa.mil/program/transparent-computing | CADETS, E3, THEIA, TRACE datasets |
| **STREAMSPOT** | https://github.com/ai-forensics/streamspot | Streaming graph anomaly detection |
| **UNICORN** | https://github.com/ai-forensics/unicorn | Graph-based intrusion detection |

---

## 🏗️ Flash-IDPS Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Flash-IDPS Pipeline                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. Input          →  Raw system audit logs (DARPA TC format)          │
│       ↓                                                                 │
│  2. Construction   →  Build provenance graph (nodes + edges)           │
│       ↓                                                                 │
│  3. Transformation →  Edge fusion, label hashing, graph cleaning       │
│       ↓                                                                 │
│  4. Featurization  →  Word2Vec embeddings (30-dim)                     │
│       ↓                                                                 │
│  5. Feat_Inference →  Add embeddings to graph nodes                    │
│       ↓                                                                 │
│  6. Batching       →  Organize graphs for mini-batch training          │
│       ↓                                                                 │
│  7. Training       →  GraphSAGE encoder + self-supervised learning     │
│       ↓                                                                 │
│  8. Evaluation     →  Anomaly detection + attack evolution graphs      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Detection Workflow

```
Benign Training Data → GraphSAGE Model → Node Type Prediction
                                                  ↓
                                         Learn Normal Patterns
                                                  ↓
Inference on New Data → High Prediction Loss → ANOMALY DETECTED
```

---

## 📊 Evaluation Criteria

Based on the evaluation spreadsheet (`Đồ án hệ thống phát hiện xâm nhập .xlsx`), this research analyzes Flash-IDPS against the following criteria:

| Criterion | Description |
|-----------|-------------|
| **Detection Accuracy** | F1 scores, precision, recall on attack detection |
| **Scalability** | Ability to process millions of system events |
| **Training Efficiency** | Time and resource requirements |
| **Self-Supervised** | No labeled attack data required |
| **Interpretability** | Attack evolution graphs and attribution |
| **Framework Support** | PIDSMaker integration and extensibility |

---

## 🛠️ Configuration

### Docker Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
# Jupyter Configuration
JUPYTER_PORT=8888
JUPYTER_TOKEN=your_secure_token_here

# Resource Limits
CPU_LIMIT=4
MEMORY_LIMIT=8g

# Volume Paths
NOTEBOOKS_DIR=./notebooks
DATA_DIR=./data
MODELS_DIR=./models
OUTPUT_DIR=./output
```

### Running Flash-IDPS via PIDSMaker

```bash
# Basic execution
python pidsmaker/main.py flash CADETS_E3

# With custom parameters
python pidsmaker/main.py flash CADETS_E3 --epochs 12 --threshold 0.65 --batch-size 32

# View all options
python pidsmaker/main.py flash --help
```

---

## 📈 Expected Output

When running Flash-IDPS, expect output similar to:

```
[Pipeline] Stage 1/8: Input - Loading audit logs...
[Pipeline] Stage 2/8: Construction - Building provenance graph...
[Pipeline] Stage 3/8: Transformation - Cleaning and normalizing...
[Pipeline] Stage 4/8: Featurization - Training Word2Vec...
[Pipeline] Stage 5/8: Feat_Inference - Adding embeddings...
[Pipeline] Stage 6/8: Batching - Organizing graphs...
[Pipeline] Stage 7/8: Training - GraphSAGE encoder (Epoch 12/12)...
[Pipeline] Stage 8/8: Evaluation - Detecting anomalies...

Results saved to: results/flash/CADETS_E3/
  - detection_results.json
  - attack_evolution_graph.png
  - metrics.json (F1: 0.94, Precision: 0.92, Recall: 0.96)
```

---

## 🔍 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Docker build fails | Ensure Docker Desktop is running with 4GB+ memory allocated |
| Out of memory | Reduce batch size in training config or increase container memory limit |
| Jupyter won't start | Check port 8888 isn't in use: `docker-compose down` then restart |
| GPU not detected | Use `Dockerfile.gpu` and ensure NVIDIA Docker runtime is installed |
| PIDSMaker import error | Run `pip install -e .` in PIDSMaker directory |

### Getting Help

1. Check the notebook's troubleshooting section
2. Review PIDSMaker documentation: https://ubc-provenance.github.io/PIDSMaker/
3. Open an issue on the PIDSMaker GitHub
4. Consult the Flash-IDPS paper for algorithmic details

---

## 📝 License & Attribution

This is a **personal research repository** for educational purposes.

- **Flash-IDPS**: © DART Laboratory, Purdue University. Published at IEEE S&P 2024.
- **PIDSMaker**: © UBC Provenance Research Group. Available at https://github.com/ubc-provenance/PIDSMaker
- **Original Flash Paper**: Available at https://dartlab.org/assets/pdf/flash.pdf

---

## 📅 Research Timeline

| Date | Milestone |
|------|-----------|
| 2024 | Flash-IDPS published at IEEE S&P |
| 2025 | PIDSMaker framework released |
| 2026 | This research repository created |

---

## 🎯 Research Goals

This repository aims to:

1. **Understand** the Flash-IDPS architecture and methodology
2. **Reproduce** results using the PIDSMaker framework
3. **Evaluate** detection performance on standard datasets
4. **Document** the complete workflow for educational purposes
5. **Compare** Flash-IDPS with other provenance-based IDS approaches

---

## 📧 Contact

For questions about this research repository, please open an issue.

For Flash-IDPS specific questions, refer to:
- **DART Laboratory**: https://dartlab.org/
- **PIDSMaker Issues**: https://github.com/ubc-provenance/PIDSMaker/issues

---

*Last updated: March 2026*
