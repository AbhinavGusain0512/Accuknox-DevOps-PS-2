import os
import sys
import logging
import psutil

# --- CONFIGURATION ---
# Define thresholds (in percentages)
CPU_THRESHOLD = 80.0
MEMORY_THRESHOLD = 80.0
DISK_THRESHOLD = 85.0

# Log file path
LOG_FILE = "system_health.log"

# --- LOGGING SETUP ---
# This configures logging to print to BOTH the console and a log file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

def check_cpu():
    """Checks CPU usage percentage."""
    # interval=1 takes a sample over 1 second for accuracy
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > CPU_THRESHOLD:
        logging.warning(f"High CPU Usage Detected: {cpu_usage}% (Threshold: {CPU_THRESHOLD}%)")
    else:
        logging.info(f"CPU Usage: {cpu_usage}%")

def check_memory():
    """Checks RAM usage percentage."""
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    if memory_usage > MEMORY_THRESHOLD:
        logging.warning(f"High Memory Usage Detected: {memory_usage}% (Threshold: {MEMORY_THRESHOLD}%)")
    else:
        logging.info(f"Memory Usage: {memory_usage}%")

def check_disk():
    """Checks root directory disk usage percentage."""
    disk_info = psutil.disk_usage('/')
    disk_usage = disk_info.percent
    if disk_usage > DISK_THRESHOLD:
        logging.warning(f"High Disk Usage Detected on '/': {disk_usage}% (Threshold: {DISK_THRESHOLD}%)")
    else:
        logging.info(f"Disk Usage on '/': {disk_usage}%")

def check_processes():
    """Logs the total number of running processes."""
    # Get total count of active PIDs
    process_count = len(psutil.pids())
    logging.info(f"Total Running Processes: {process_count}")

def main():
    logging.info("--- Starting System Health Check ---")
    try:
        check_cpu()
        check_memory()
        check_disk()
        check_processes()
    except Exception as e:
        logging.error(f"An error occurred during system health monitoring: {e}")
    logging.info("--- System Health Check Complete ---\n")

if __name__ == "__main__":
    # Ensure script is running on Linux
    if not sys.platform.startswith("linux"):
        print("Warning: This script is optimized for Linux environments.")
    
    main()
