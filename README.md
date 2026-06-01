# System Health Monitoring Script

A lightweight, automated Python script designed for Linux DevOps environments to monitor critical system health metrics, log performance, and trigger alerts when thresholds are breached.

## Features
* **CPU Monitoring:** Tracks real-time CPU usage and flags utilization above a set threshold (Default: 80%).
* **Memory Monitoring:** Monitors RAM usage and alerts on high consumption.
* **Disk Space Tracking:** Checks root (`/`) partition storage availability.
* **Process Counting:** Tracks total active processes running on the system.
* **Dual Logging:** Outputs alerts and diagnostics simultaneously to the console (stdout) and a persistent log file (`system_health.log`).

## Prerequisites
* Linux-based operating system
* Python 3.6+
* `psutil` library

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/AbhinavGusain0512/Accuknox-DevOps-PS-2.git](https://github.com/AbhinavGusain0512/Accuknox-DevOps-PS-2.git)
   cd Accuknox-DevOps-PS-2
