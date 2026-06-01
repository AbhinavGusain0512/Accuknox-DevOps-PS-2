import os
import sys
import tarfile
import logging
from datetime import datetime
import paramiko

# --- CONFIGURATION ---
LOCAL_DIR_TO_BACKUP = "/path/to/source_directory"  # Change to your target folder
BACKUP_TEMP_DIR = "/tmp"                          # Temporary space to hold the archive

# Remote Server configuration
REMOTE_HOST = "your.remote.server.ip"
REMOTE_PORT = 22
REMOTE_USER = "your_username"
REMOTE_PASSWORD = "your_password"                 # Alternatively, use SSH keys
REMOTE_DEST_DIR = "/path/to/remote/backup/folder"

# --- LOGGING SETUP ---
LOG_FILE = "backup_report.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)]
)

def create_archive():
    """Compresses the specified directory into a .tar.gz archive."""
    if not os.path.exists(LOCAL_DIR_TO_BACKUP):
        logging.error(f"Backup Failed: Local directory {LOCAL_DIR_TO_BACKUP} does not exist.")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"backup_{timestamp}.tar.gz"
    archive_path = os.path.join(BACKUP_TEMP_DIR, archive_name)

    try:
        logging.info(f"Starting compression of {LOCAL_DIR_TO_BACKUP}...")
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(LOCAL_DIR_TO_BACKUP, arcname=os.path.basename(LOCAL_DIR_TO_BACKUP))
        logging.info(f"Archive successfully created locally at: {archive_path}")
        return archive_path
    except Exception as e:
        logging.error(f"Compression failed: {e}")
        return None

def transfer_to_remote(local_archive_path):
    """Transfers the archive file to the remote server using SFTP."""
    file_name = os.path.basename(local_archive_path)
    remote_file_path = os.path.join(REMOTE_DEST_DIR, file_name)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        logging.info(f"Connecting to remote server {REMOTE_HOST}...")
        ssh.connect(hostname=REMOTE_HOST, port=REMOTE_PORT, username=REMOTE_USER, password=REMOTE_PASSWORD)
        
        sftp = ssh.open_sftp()
        logging.info(f"Transferring {file_name} to remote directory {REMOTE_DEST_DIR}...")
        sftp.put(local_archive_path, remote_file_path)
        sftp.close()
        
        logging.info("SUCCESS: Backup transfer operation completed flawlessly.")
        return True
    except Exception as e:
        logging.error(f"FAILURE: Remote transfer operation failed. Reason: {e}")
        return False
    finally:
        ssh.close()
        # Clean up local temp archive file
        if os.path.exists(local_archive_path):
            os.remove(local_archive_path)
            logging.info("Cleaned up temporary local archive file.")

def main():
    logging.info("================== BACKUP PROCESS STARTED ==================")
    archive = create_archive()
    if archive:
        success = transfer_to_remote(archive)
        if success:
            logging.info("REPORT STATUS: [SUCCESS]")
        else:
            logging.info("REPORT STATUS: [FAILED]")
    else:
        logging.info("REPORT STATUS: [FAILED]")
    logging.info("================== BACKUP PROCESS FINISHED ==================\n")

if __name__ == "__main__":
    main()
