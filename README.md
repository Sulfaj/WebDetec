# OPD Website Status Detector – Makassar City

This repository contains a simple Python script to detect the availability status of websites managed by the Makassar City Government.

## Features
- Automatically check a list of OPD websites (`urls_opd_makassar.txt`).
- Detects whether each website is **Active** (HTTP 200) or **Inactive**.
- Sends a summary report via email using Gmail SMTP.
- Runs continuously and repeats the detection every 1 hour.

## Files
- `urls_opd_makassar.txt` → List of OPD websites.
- `webdetec.py` → Main script for detection and reporting.

## Requirements
- Python 3.x
- Install dependencies:
  ```bash
  pip install requests
