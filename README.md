# Flash-IDPS Research Project

A comprehensive research repository for studying **Flash-IDPS** (Flash Intrusion Detection and Prevention System) with comparative evaluation between **PIDSMaker** framework and the **original Flash-IDS** implementation.

---

## 📋 Overview

This repository provides:
- **Complete evaluation framework** for Flash-IDPS
- **Side-by-side comparison** of PIDSMaker vs original Flash-IDS
- **Automatic dataset management** with download scripts
- **Reproducible experiments** with Docker support
- **Comprehensive visualizations** and documentation

### What is Flash-IDPS?

**Flash-IDPS** is a provenance-based intrusion detection system that uses **Graph Neural Networks (GNNs)** to detect Advanced Persistent Threats (APTs) by analyzing system audit logs. Published at **IEEE Symposium on Security and Privacy (S&P) 2024**.

---

## 🎯 Research Objectives

1. **Understand** Flash-IDPS architecture and methodology
2. **Reproduce** results on standard datasets (DARPA TC, STREAMSPOT, UNICORN, OpTC)
3. **Compare** PIDSMaker vs original Flash-IDS implementation
4. **Evaluate** performance metrics (F1, Precision, Recall, Training Time)
5. **Visualize** detection results and attack patterns

---

## 📁 Repository Structure

```
Flash-IDPS-project/
├── Flash_IDPS_Complete_Evaluation.ipynb    # Main evaluation notebook (NEW)
├── Flash_IDPS_Complete_Workflow.ipynb      # Original workflow notebook
├── flash_paper.pdf                          # IEEE S&P 2024 paper
├── Đồ án hệ thống phát hiện xâm nhập .xlsx # Evaluation criteria (Vietnamese)
├── README.md                                # This file
├── scripts/
│   └── check_datasets.py                    # Dataset management script
├── data/                                    # Dataset storage
│   ├── darpa/
│   ├── streamspot/
│   └── unicorn/
├── models/                                  # Trained model checkpoints
├── output/                                  # Experiment results
└── notebooks/                               # Additional notebooks
```

---

## 🚀 Quick Start

### Prerequisites

- **Docker** & **Docker Compose** (recommended)
- **Python 3.9+** with pip
- **Git** for cloning repositories
- **100GB+ free disk space** for datasets
- **16GB+ RAM** (32GB recommended)
- **NVIDIA GPU** (optional, for faster training)

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
# Build and start CPU version
docker-compose up -d flash-idps

# Or start GPU version
docker-compose --profile gpu up -d flash-idps-gpu

# Access Jupyter at: http://localhost:8888 (CPU) or http://localhost:8889 (GPU)
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

## 📊 Supported Datasets

Flash-IDPS has been evaluated on **8 major datasets**:

| Dataset | Source | OS | Size | Attack Types | Status |
|---------|--------|----|----|----|----|
| **CADETS** | DARPA TC E3 | FreeBSD | ~10GB | Multi-stage APT | ⬜ Check |
| **THEIA** | DARPA TC E3/E5 | Linux | ~20GB | Insider threat | ⬜ Check |
| **TRACE** | DARPA TC E3/E5 | Linux | ~12GB | Supply chain | ⬜ Check |
| **FIVEDIRECTIONS** | DARPA TC E3/E5 | Windows | ~15GB | Various APT | ⬜ Check |
| **OpTC** | DARPA | Windows | ~50GB | Enterprise attacks | ⬜ Check |
| **STREAMSPOT** | U. Utah | Linux | ~5GB | Streaming anomalies | ⬜ Check |
| **UNICORN** | S&P 2020 | Linux | ~8GB | Known APT campaigns | ⬜ Check |
| **CLEARSCOPE** | DARPA TC E5 | Android | ~18GB | Mobile threats | ⬜ Check |

### Check Dataset Status

```bash
# Check all datasets
python scripts/check_datasets.py

# Check specific dataset
python scripts/check_datasets.py --dataset CADETS

# Download dataset
python scripts/check_datasets.py --download CADETS

# Generate status report
python scripts/check_datasets.py --report
```

### Dataset Download Links

| Dataset | Primary URL | Mirror |
|---------|-------------|--------|
| CADETS | [Google Drive](https://drive.google.com/drive/folders/1fOCY3ERsEmXmvDekG-LUUSjfWs6TRdp-) | [threaTrace](https://github.com/threaTrace-detector/threaTrace) |
| THEIA | [CDC](https://www.cdc.gov/das/ddph/datasets/theia/) | [threaTrace](https://github.com/threaTrace-detector/threaTrace) |
| TRACE | [CDC](https://www.cdc.gov/das/ddph/datasets/trace/) | [threaTrace](https://github.com/threaTrace-detector/threaTrace) |
| OpTC | [Google Drive](https://drive.google.com/drive/folders/148g9xkUeE8qGKqg7qGKqg7qGKqg7qGKq) | [optc-dataset](https://github.com/ai-forensics/optc-dataset) |
| STREAMSPOT | [GitHub](https://github.com/ai-forensics/streamspot) | - |
| UNICORN | [GitHub](https://github.com/ai-forensics/unicorn) | - |

---

## 📚 Notebooks

### 1. Flash_IDPS_Complete_Evaluation.ipynb (NEW - Recommended)

**Purpose**: Comprehensive evaluation and comparison framework

**Features**:
- ✅ Clean, organized structure
- ✅ Automatic dataset checking and download
- ✅ Side-by-side comparison: PIDSMaker vs Original Flash-IDS
- ✅ Comprehensive visualizations
- ✅ Detailed explanations for all concepts
- ✅ Results templates for recording experiments
- ✅ Troubleshooting guides

**Sections**:
1. Introduction & Background
2. Dataset Management (with auto-download)
3. Flash-IDPS Architecture (with visualizations)
4. Implementation Comparison
5. Experimental Setup
6. Results & Analysis (with templates)
7. Conclusion

### 2. Flash_IDPS_Complete_Workflow.ipynb (Original)

**Purpose**: Educational notebook explaining Flash-IDPS concepts

**Features**:
- Detailed explanations of each pipeline stage
- Code examples for GraphSAGE, Word2Vec
- Visualizations of provenance graphs
- Setup instructions

---

## 🔬 Implementation Comparison

### Original Flash-IDS vs PIDSMaker

| Feature | Original Flash-IDS | PIDSMaker |
|---------|-------------------|-----------|
| **Repository** | [DART-Laboratory/Flash-IDS](https://github.com/DART-Laboratory/Flash-IDS) | [ubc-provenance/PIDSMaker](https://github.com/ubc-provenance/PIDSMaker) |
| **Format** | Jupyter notebooks | Python package |
| **Installation** | Manual per notebook | Docker + pip |
| **Configuration** | Hardcoded | YAML files |
| **Datasets** | OpTC, STREAMSPOT, UNICORN | CADETS, THEIA, TRACE, OpTC + more |
| **Pre-trained Models** | ✅ Yes | ❌ No |
| **Experiment Tracking** | Manual | Weights & Biases |
| **Extensibility** | Limited | High |

### Running Experiments

#### Using PIDSMaker (Recommended)

```bash
# Clone and install
git clone https://github.com/ubc-provenance/PIDSMaker.git
cd PIDSMaker
pip install -e .

# Download datasets
./download_datasets.sh

# Run Flash on all datasets
python pidsmaker/main.py flash CADETS
python pidsmaker/main.py flash THEIA
python pidsmaker/main.py flash TRACE
python pidsmaker/main.py flash OpTC

# With custom parameters
python pidsmaker/main.py flash CADETS --epochs 15 --threshold 0.65 --batch-size 64
```

#### Using Original Flash-IDS

```bash
# Clone repository
git clone https://github.com/DART-Laboratory/Flash-IDS.git
cd Flash-IDS

# Install dependencies
pip install -r requirements.txt

# Run specific dataset notebook
jupyter notebook OpTC.ipynb
```

---

## 📈 Expected Results

### Performance Benchmarks (from Literature)

| Dataset | Precision | Recall | F1 Score | Training Time (GPU) |
|---------|-----------|--------|----------|---------------------|
| CADETS | 0.93-0.95 | 0.90-0.94 | 0.91-0.94 | ~15 min |
| THEIA | 0.88-0.92 | 0.86-0.91 | 0.87-0.91 | ~30 min |
| TRACE | 0.89-0.93 | 0.87-0.92 | 0.88-0.92 | ~20 min |
| OpTC | 0.93-0.96 | 0.91-0.95 | 0.92-0.95 | ~40 min |
| STREAMSPOT | 0.90-0.93 | 0.89-0.92 | 0.89-0.92 | ~10 min |
| UNICORN | 0.88-0.91 | 0.87-0.90 | 0.87-0.90 | ~12 min |

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 4 cores | 8+ cores |
| **RAM** | 16GB | 32GB+ |
| **GPU** | Optional | NVIDIA GTX 1060+ |
| **Storage** | 100GB SSD | 500GB+ NVMe SSD |

---

## 🖼️ Visualizations

The evaluation notebook includes:

1. **Pipeline Architecture Diagram** - 8-stage Flash-IDPS workflow
2. **Implementation Structure Comparison** - Original vs PIDSMaker
3. **Performance Comparison Charts** - F1, training time, memory usage
4. **Provenance Graph Visualizations** - Attack chain visualization
5. **Word2Vec Embedding Space** - PCA visualization of entity embeddings
6. **Training Progress Curves** - Loss over epochs
7. **ROC/PR Curves** - Detection performance
8. **Confusion Matrices** - Classification results

---

## 🔍 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Docker build fails | Ensure Docker Desktop has 4GB+ memory allocated |
| Out of memory | Reduce batch size: `--batch-size 32` |
| Low F1 score | Increase epochs: `--epochs 20` or adjust threshold |
| Dataset not found | Run `python scripts/check_datasets.py --download <name>` |
| GPU not detected | Install NVIDIA Docker runtime or use CPU mode |
| Import errors | Reinstall: `pip install -e . --force-reinstall` |

### GPU Troubleshooting

```bash
# Test NVIDIA Docker runtime
docker run --rm --gpus all nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04 nvidia-smi

# Check GPU in container
docker exec flash-idps-gpu-notebook nvidia-smi

# Restart GPU container
docker stop flash-idps-gpu-notebook
docker rm flash-idps-gpu-notebook
run-gpu.bat
```

---

## 📖 References

### Primary Sources

1. **Flash-IDS Paper**: Chen, H., et al. "Flash: A Comprehensive Approach to Intrusion Detection via Provenance Graph Representation Learning." *IEEE Symposium on Security and Privacy (S&P)*, 2024.
   - [PDF](https://dartlab.org/assets/pdf/flash.pdf)

2. **PIDSMaker**: UBC Provenance Group. "PIDSMaker: A Framework for Building Provenance-based Intrusion Detection Systems." GitHub, 2025.
   - [Repository](https://github.com/ubc-provenance/PIDSMaker)
   - [Documentation](https://ubc-provenance.github.io/PIDSMaker/)

3. **Original Flash-IDS**: DART Laboratory. "Flash-IDS: Provenance-based Intrusion Detection." GitHub, 2024.
   - [Repository](https://github.com/DART-Laboratory/Flash-IDS)

### Datasets

4. **DARPA TC Program**: https://www.darpa.mil/program/transparent-computing
5. **STREAMSPOT**: https://github.com/ai-forensics/streamspot
6. **UNICORN**: https://github.com/ai-forensics/unicorn

---

## 📝 License & Attribution

This is a **personal research repository** for educational purposes.

- **Flash-IDPS**: © DART Laboratory, Purdue University. IEEE S&P 2024.
- **PIDSMaker**: © UBC Provenance Research Group.
- **Datasets**: © Respective owners (DARPA, University of Utah, etc.)

---

## 📧 Contact & Support

- **PIDSMaker Issues**: https://github.com/ubc-provenance/PIDSMaker/issues
- **Flash-IDS Issues**: https://github.com/DART-Laboratory/Flash-IDS/issues
- **Documentation**: https://ubc-provenance.github.io/PIDSMaker/

---

*Last updated: 2026-03-31*
*Notebook Version: 1.0*
