#!/usr/bin/env python3
"""
Flash-IDPS Auto Dataset Downloader
Tải datasets TRỰC TIẾP trên remote Linux server từ Google Drive.

Usage:
    python scripts/auto_download_datasets.py [--all | --cadets | --optc | --streamspot]
    
Google Drive Folder chính (chứa CADETS, THEIA, TRACE, FIVEDIRECTIONS, CLEARSCOPE):
    https://drive.google.com/drive/folders/1fOCY3ERsEmXmvDekG-LUUSjfWs6TRdp-
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Optional
import time

# Google Drive Folder IDs
DARPA_TC_FOLDER_ID = "1fOCY3ERsEmXmvDekG-LUUSjfWs6TRdp-"  # CADETS, THEIA, TRACE, FIVEDIRECTIONS, CLEARSCOPE
OPTC_FOLDER_ID = "1n3kkS3KR31KUegn42yk3-e6JkZvf0Caa"      # OpTC

# Dataset configuration
DATASETS = {
    'CADETS': {
        'type': 'gdrive_subfolder',
        'folder_id': DARPA_TC_FOLDER_ID,
        'subfolder': 'cadets',
        'dest': './data/darpa/cadets',
        'description': 'DARPA TC E3 - FreeBSD multi-stage APT (~10GB)',
    },
    'THEIA': {
        'type': 'gdrive_subfolder',
        'folder_id': DARPA_TC_FOLDER_ID,
        'subfolder': 'theia',
        'dest': './data/darpa/theia',
        'description': 'DARPA TC E3/E5 - Linux insider threat (~20GB)',
    },
    'TRACE': {
        'type': 'gdrive_subfolder',
        'folder_id': DARPA_TC_FOLDER_ID,
        'subfolder': 'trace',
        'dest': './data/darpa/trace',
        'description': 'DARPA TC E3/E5 - Linux supply chain attack (~12GB)',
    },
    'FIVEDIRECTIONS': {
        'type': 'gdrive_subfolder',
        'folder_id': DARPA_TC_FOLDER_ID,
        'subfolder': 'fivedirections',
        'dest': './data/darpa/fivedirections',
        'description': 'DARPA TC E3/E5 - Windows APT scenarios (~15GB)',
    },
    'CLEARSCOPE': {
        'type': 'gdrive_subfolder',
        'folder_id': DARPA_TC_FOLDER_ID,
        'subfolder': 'clearscope',
        'dest': './data/darpa/clearscope',
        'description': 'DARPA TC - Clearscope dataset',
    },
    'OpTC': {
        'type': 'gdrive_folder',
        'folder_id': OPTC_FOLDER_ID,
        'dest': './data/optc',
        'description': 'DARPA OpTC - Enterprise Windows environment (~50GB)',
    },
    'STREAMSPOT': {
        'type': 'github',
        'url': 'https://github.com/sbustreamspot/sbustreamspot-data',
        'dest': './data/streamspot',
        'description': 'Streaming graph anomaly detection (~5GB)',
    }
}


def check_disk_space(required_gb: int = 100) -> bool:
    """Kiểm tra dung lượng disk còn trống."""
    stat = shutil.disk_usage('.')
    free_gb = stat.free / (1024 ** 3)
    print(f"\n💾 Disk space check:")
    print(f"   Free: {free_gb:.1f} GB")
    print(f"   Required: ~{required_gb} GB for all datasets")
    
    if free_gb < required_gb:
        print(f"   ⚠️  WARNING: Not enough disk space!")
        return False
    print(f"   ✅ Sufficient disk space")
    return True


def check_gdown_installed() -> bool:
    """Kiểm tra xem gdown đã được cài chưa."""
    try:
        import gdown
        return True
    except ImportError:
        return False


def install_gdown():
    """Cài đặt gdown nếu chưa có."""
    print("\n📦 Installing gdown...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown", "-q"])
        print("   ✅ gdown installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Failed to install gdown: {e}")
        return False


def install_gdown_if_needed() -> bool:
    """Kiểm tra và cài gdown nếu cần."""
    if not check_gdown_installed():
        print("\n⚠️  gdown is not installed")
        print("   Installing gdown automatically...")
        return install_gdown()
    print("\n✅ gdown is installed")
    return True


def download_google_drive_folder(folder_id: str, dest_path: str, quiet: bool = False) -> bool:
    """
    Tải thư mục từ Google Drive sử dụng gdown.
    
    Args:
        folder_id: Google Drive folder ID
        dest_path: Đường dẫn thư mục đích
        quiet: Silent mode
    """
    try:
        import gdown
        
        url = f"https://drive.google.com/drive/folders/{folder_id}"
        
        print(f"\n   📥 Downloading Google Drive folder...")
        print(f"   URL: {url}")
        print(f"   Destination: {dest_path}")
        print(f"   ⚠️  This may take a while for large folders...")
        print(f"   💡 Tip: Press Ctrl+C to cancel if stuck")
        
        # Tạo thư mục đích
        os.makedirs(dest_path, exist_ok=True)
        
        # Sử dụng gdown với folder download
        # remaining_ok=True để tiếp tục nếu download dở trước đó
        gdown.download_folder(
            url, 
            output=dest_path, 
            quiet=quiet,
            remaining_ok=True,
            use_cookies=False
        )
        
        # Kiểm tra files đã tải
        files = list(Path(dest_path).rglob('*'))
        files = [f for f in files if f.is_file()]
        
        if len(files) > 0:
            total_size = sum(f.stat().st_size for f in files) / (1024 ** 3)
            print(f"\n   ✅ Downloaded {len(files)} files ({total_size:.2f} GB)")
            return True
        else:
            print(f"   ⚠️  No files downloaded")
            return False
            
    except KeyboardInterrupt:
        print("\n   ⚠️  Download cancelled by user")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def download_darpa_tc_folder() -> bool:
    """
    Tải toàn bộ folder DARPA TC (CADETS, THEIA, TRACE, FIVEDIRECTIONS, CLEARSCOPE).
    Sử dụng phương pháp download từng file riêng để tránh lỗi folder lớn.
    """
    print("\n" + "="*80)
    print("📥 DOWNLOADING DARPA TC DATASETS")
    print("="*80)
    print("\n📁 This folder contains:")
    print("   - CADETS")
    print("   - THEIA")
    print("   - TRACE")
    print("   - FIVEDIRECTIONS")
    print("   - CLEARSCOPE")

    # Tạo thư mục tạm để tải
    temp_dir = "./data/darpa_temp"
    os.makedirs(temp_dir, exist_ok=True)

    # Download folder
    success = download_google_drive_folder(DARPA_TC_FOLDER_ID, temp_dir)

    if not success:
        print("\n⚠️  Download failed or incomplete")
        print("\n💡 Alternative: Download manually from browser")
        print("   URL: https://drive.google.com/drive/folders/1fOCY3ERsEmXmvDekG-LUUSjfWs6TRdp-")
        return False

    # Di chuyển các subfolders vào đúng vị trí
    print("\n📁 Organizing datasets...")

    subfolders = ['cadets', 'theia', 'trace', 'fivedirections', 'clearscope']

    for subfolder in subfolders:
        src = Path(temp_dir) / subfolder
        if src.exists():
            # Tạo destination path
            dest = Path(f"./data/darpa/{subfolder}")
            dest.mkdir(parents=True, exist_ok=True)

            # Di chuyển files
            for item in src.iterdir():
                if item.is_file() or item.is_dir():
                    shutil.move(str(item), str(dest / item.name))

            print(f"   ✅ Moved {subfolder} to {dest}")
        else:
            print(f"   ⚠️  {subfolder} not found in downloaded folder")

    # Xóa thư mục tạm
    if Path(temp_dir).exists():
        shutil.rmtree(temp_dir)
        print(f"   🗑️  Cleaned up temporary directory")

    return True


def download_optc() -> bool:
    """Tải OpTC dataset từ Google Drive."""
    print("\n" + "="*80)
    print("📥 DOWNLOADING OpTC DATASET")
    print("="*80)
    
    dest_path = "./data/optc"
    os.makedirs(dest_path, exist_ok=True)
    
    success = download_google_drive_folder(OPTC_FOLDER_ID, dest_path)
    
    if success:
        print(f"\n✅ OpTC downloaded to {dest_path}")
    else:
        print(f"\n⚠️  OpTC download failed or incomplete")
    
    return success


def download_streamspot() -> bool:
    """Tải STREAMSPOT dataset từ GitHub."""
    print("\n" + "="*80)
    print("📥 DOWNLOADING STREAMSPOT DATASET")
    print("="*80)
    
    dest_path = "./data/streamspot"
    repo_url = "https://github.com/sbustreamspot/sbustreamspot-data"
    
    print(f"\n   Cloning from GitHub: {repo_url}")
    
    try:
        # Clone repo
        cmd = ['git', 'clone', '--depth', '1', repo_url, dest_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"   ✅ Cloned successfully")
            
            # Kiểm tra files
            files = list(Path(dest_path).rglob('*'))
            files = [f for f in files if f.is_file()]
            print(f"   📁 {len(files)} files downloaded")
            return True
        else:
            print(f"   ❌ Clone failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def download_single_dataset(dataset_name: str) -> bool:
    """Download một dataset cụ thể."""
    if dataset_name not in DATASETS:
        print(f"❌ Unknown dataset: {dataset_name}")
        print(f"Available: {', '.join(DATASETS.keys())}")
        return False
    
    config = DATASETS[dataset_name]
    
    print(f"\n📥 Downloading: {dataset_name}")
    print(f"   Description: {config['description']}")
    
    if config['type'] == 'gdrive_subfolder':
        # Tải cả folder DARPA TC và extract subfolder
        return download_darpa_tc_folder()
    elif config['type'] == 'gdrive_folder':
        if dataset_name == 'OpTC':
            return download_optc()
    elif config['type'] == 'github':
        if dataset_name == 'STREAMSPOT':
            return download_streamspot()
    
    return False


def interactive_mode():
    """Chế độ tương tác - hỏi user muốn tải datasets nào."""
    print("\n" + "="*80)
    print("🚀 FLASH-IDPS AUTO DATASET DOWNLOADER")
    print("="*80)
    
    # Kiểm tra disk space
    if not check_disk_space(100):
        print("\n⚠️  Please free up disk space before continuing")
        return
    
    # Kiểm tra và cài gdown
    gdown_ready = install_gdown_if_needed()
    if not gdown_ready:
        print("\n⚠️  Cannot proceed without gdown")
        return
    
    # Hiển thị datasets available
    print("\n📊 Available Datasets:")
    print("\n   📁 DARPA TC Folder (contains multiple datasets):")
    print("      - CADETS (~10GB)")
    print("      - THEIA (~20GB)")
    print("      - TRACE (~12GB)")
    print("      - FIVEDIRECTIONS (~15GB)")
    print("      - CLEARSCOPE")
    print("\n   📁 OpTC Folder:")
    print("      - OpTC (~50GB)")
    print("\n   📁 GitHub:")
    print("      - STREAMSPOT (~5GB)")
    
    # Menu
    print("\n" + "-"*80)
    print("Which datasets do you want to download?")
    print("\n   1. DARPA TC Folder (CADETS + THEIA + TRACE + FIVEDIRECTIONS + CLEARSCOPE) ~60GB")
    print("   2. OpTC only (~50GB)")
    print("   3. STREAMSPOT only (~5GB)")
    print("   4. All datasets (~115GB)")
    print("   5. Custom selection")
    print("   6. Exit")
    
    choice = input("\nEnter choice (1-6): ").strip()
    
    if choice == '1':
        download_darpa_tc_folder()
    elif choice == '2':
        download_optc()
    elif choice == '3':
        download_streamspot()
    elif choice == '4':
        print("\n📥 Downloading ALL datasets...")
        download_darpa_tc_folder()
        print("\n   Waiting 10 seconds before next download...")
        time.sleep(10)
        download_optc()
        print("\n   Waiting 10 seconds before next download...")
        time.sleep(10)
        download_streamspot()
    elif choice == '5':
        print("\nSelect datasets (comma-separated, e.g., CADETS,OpTC):")
        user_input = input("> ").strip()
        selected = [s.strip().upper() for s in user_input.split(',')]
        
        for ds in selected:
            if ds in ['CADETS', 'THEIA', 'TRACE', 'FIVEDIRECTIONS', 'CLEARSCOPE']:
                print(f"\n📥 Downloading {ds} (will download entire DARPA TC folder)...")
                download_darpa_tc_folder()
                break  # Chỉ cần tải 1 lần
        
        if 'OPTC' in selected or 'OPTC' in [s.upper() for s in selected]:
            print(f"\n📥 Downloading OpTC...")
            download_optc()
        
        if 'STREAMSPOT' in selected:
            print(f"\n📥 Downloading STREAMSPOT...")
            download_streamspot()
    elif choice == '6':
        print("Exiting...")
        return
    else:
        print("Invalid choice")
        return
    
    # Summary
    print("\n" + "="*80)
    print("✅ DOWNLOAD COMPLETE!")
    print("="*80)
    print("\n💡 To verify downloaded datasets:")
    print("   python scripts/check_datasets.py")
    print("\n💡 To check dataset files:")
    print("   ls -lh data/darpa/")
    print("   ls -lh data/optc/")
    print("   ls -lh data/streamspot/")
    print("="*80 + "\n")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Flash-IDPS Auto Dataset Downloader',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python auto_download_datasets.py              # Interactive mode
  python auto_download_datasets.py --all        # Download all datasets
  python auto_download_datasets.py --darpa-tc   # Download DARPA TC folder
  python auto_download_datasets.py --optc       # Download OpTC only
  python auto_download_datasets.py --streamspot # Download STREAMSPOT only
  python auto_download_datasets.py --cadets     # Download CADETS (from DARPA TC folder)
        """
    )
    
    parser.add_argument('--all', action='store_true',
                       help='Download all datasets (DARPA TC + OpTC + STREAMSPOT)')
    parser.add_argument('--darpa-tc', action='store_true',
                       help='Download DARPA TC folder (CADETS, THEIA, TRACE, FIVEDIRECTIONS, CLEARSCOPE)')
    parser.add_argument('--optc', action='store_true',
                       help='Download OpTC dataset')
    parser.add_argument('--streamspot', action='store_true',
                       help='Download STREAMSPOT dataset')
    parser.add_argument('--cadets', action='store_true',
                       help='Download CADETS dataset (from DARPA TC folder)')
    parser.add_argument('--theia', action='store_true',
                       help='Download THEIA dataset (from DARPA TC folder)')
    parser.add_argument('--trace', action='store_true',
                       help='Download TRACE dataset (from DARPA TC folder)')
    parser.add_argument('--fivedirections', action='store_true',
                       help='Download FIVEDIRECTIONS dataset (from DARPA TC folder)')
    
    args = parser.parse_args()
    
    # Check if gdown is needed and install if necessary
    needs_gdown = args.all or args.darpa_tc or args.optc or args.cadets or args.theia or args.trace or args.fivedirections
    
    if needs_gdown and not check_gdown_installed():
        print("\n⚠️  gdown is required for Google Drive downloads")
        install_gdown()
    
    # Process arguments
    if args.all:
        print("\n📥 Downloading ALL datasets...")
        install_gdown_if_needed()
        download_darpa_tc_folder()
        print("\n   Waiting 10 seconds before next download...")
        time.sleep(10)
        download_optc()
        print("\n   Waiting 10 seconds before next download...")
        time.sleep(10)
        download_streamspot()
    elif args.darpa_tc or args.cadets or args.theia or args.trace or args.fivedirections:
        # Tất cả đều tải từ cùng 1 folder
        install_gdown_if_needed()
        download_darpa_tc_folder()
    elif args.optc:
        install_gdown_if_needed()
        download_optc()
    elif args.streamspot:
        download_streamspot()
    else:
        # Interactive mode
        interactive_mode()


if __name__ == '__main__':
    main()
