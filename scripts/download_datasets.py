#!/usr/bin/env python3
"""
Flash-IDPS Dataset Download Helper
Provides download links and instructions for Flash-IDPS datasets.

Official Flash-IDPS: https://github.com/DART-Laboratory/Flash-IDS
"""

import sys
import subprocess
from pathlib import Path


DATASET_URLS = {
    'CADETS': {
        'url': 'https://drive.google.com/drive/folders/1fOCY3ERsEmXmvDekG-LUUSjfWs6TRdp-',
        'path': './data/darpa/cadets',
        'size': '~10GB',
        'description': 'DARPA TC E3 - FreeBSD multi-stage APT'
    },
    'THEIA': {
        'url': 'https://github.com/darpa-i2o/Transparent-Computing',
        'path': './data/darpa/theia',
        'size': '~20GB',
        'description': 'DARPA TC E3/E5 - Linux insider threat'
    },
    'TRACE': {
        'url': 'https://github.com/darpa-i2o/Transparent-Computing',
        'path': './data/darpa/trace',
        'size': '~12GB',
        'description': 'DARPA TC E3/E5 - Linux supply chain attack'
    },
    'FIVEDIRECTIONS': {
        'url': 'https://github.com/darpa-i2o/Transparent-Computing',
        'path': './data/darpa/fivedirections',
        'size': '~15GB',
        'description': 'DARPA TC E3/E5 - Windows APT scenarios'
    },
    'OpTC': {
        'url': 'https://drive.google.com/drive/u/0/folders/1n3kkS3KR31KUegn42yk3-e6JkZvf0Caa',
        'path': './data/optc',
        'size': '~50GB',
        'description': 'DARPA OpTC - Enterprise Windows environment'
    },
    'STREAMSPOT': {
        'url': 'https://github.com/sbustreamspot/sbustreamspot-data',
        'path': './data/streamspot',
        'size': '~5GB',
        'description': 'Streaming graph anomaly detection'
    },
    'UNICORN': {
        'url': 'https://www.ndss-symposium.org/ndss2020/',
        'path': './data/unicorn',
        'size': '~8GB',
        'description': 'Known APT campaigns (SC1, SC2) - NDSS 2020'
    }
}


def print_download_info(dataset_name: str):
    """Print download information for a specific dataset."""
    if dataset_name not in DATASET_URLS:
        print(f"❌ Unknown dataset: {dataset_name}")
        print(f"Available: {', '.join(DATASET_URLS.keys())}")
        return False

    config = DATASET_URLS[dataset_name]
    
    print("\n" + "="*70)
    print(f"📥 DOWNLOAD: {dataset_name}")
    print("="*70)
    print(f"Description: {config['description']}")
    print(f"Size:        {config['size']}")
    print(f"URL:         {config['url']}")
    print(f"Destination: {config['path']}")
    print("="*70)
    print("\nSteps:")
    print("1. Visit the URL above")
    print("2. Download the dataset files")
    print(f"3. Extract/create directory: {config['path']}")
    print("4. Run 'python scripts/check_datasets.py' to verify")
    print()
    
    return True


def print_all_download_links():
    """Print all dataset download links."""
    print("\n" + "="*80)
    print("📚 FLASH-IDPS DATASET DOWNLOAD LINKS")
    print("="*80)
    print()
    
    for name, config in DATASET_URLS.items():
        print(f"📁 {name}")
        print(f"   URL:  {config['url']}")
        print(f"   Size: {config['size']}")
        print(f"   Path: {config['path']}")
        print()
    
    print("="*80)
    print("\n💡 Tip: Download one dataset at a time to avoid confusion")
    print("   Example: python download_datasets.py CADETS")
    print()


def try_gdown_download(dataset_name: str):
    """Try to download using gdown (for Google Drive links)."""
    config = DATASET_URLS[dataset_name]
    url = config['url']
    
    if 'drive.google.com' not in url:
        print("⚠️  Not a Google Drive link, cannot use gdown")
        return False
    
    try:
        import gdown
        print(f"🔄 Attempting download with gdown...")
        print("⚠️  Note: For Google Drive folders, manual download is recommended")
        return False
    except ImportError:
        print("⚠️  gdown not installed. Install with: pip install gdown")
        return False


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Flash-IDPS Dataset Download Helper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python download_datasets.py              # Show all download links
  python download_datasets.py CADETS       # Show info for CADETS
  python download_datasets.py OpTC         # Show info for OpTC
  python download_datasets.py --all        # Show all links
        """
    )

    parser.add_argument('dataset', nargs='?', type=str,
                       help='Dataset name (CADETS, THEIA, OpTC, etc.)')
    parser.add_argument('--all', '-a', action='store_true',
                       help='Show all download links')
    parser.add_argument('--gdown', action='store_true',
                       help='Try to use gdown for Google Drive downloads')

    args = parser.parse_args()

    if args.all or (args.dataset is None):
        print_all_download_links()
        sys.exit(0)

    if args.gdown and args.dataset:
        try_gdown_download(args.dataset)
    
    success = print_download_info(args.dataset)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
