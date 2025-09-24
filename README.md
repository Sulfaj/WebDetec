# 🛰️ OPD Website Status Detector – Makassar City

This repository contains Python scripts to detect the availability status of websites managed by the Makassar City Government (OPD websites).

The tool will check whether each website is accessible (**Active**) or not (**Inactive**) and provide reporting options via **email** and/or **CSV logging** for further analysis.

---

## ✨ Features
- Automatically checks a list of OPD websites (`urls_opd_makassar.txt`).
- Detects whether each website is **Active (HTTP 200)** or **Inactive**.
- Sends a summary report via **email (SMTP Gmail)**.
- Runs continuously and repeats the detection every 1 hour.
- (Optional) Logs all results into a **CSV file** for historical analysis.

---

## 📂 Project Structure
```
.
├── urls_opd_makassar.txt   # List of OPD websites (targets to check)
├── webdetec.py             # Script to check websites and send email reports
├── webdetec_logger.py      # Script to check websites, send email reports, AND log results to CSV
└── hasil_deteksi.csv       # Generated log file (only if using webdetec_logger.py)
```

---

## 🛠️ Requirements
- Python 3.x
- Install dependencies:
  ```bash
  pip install requests
  ```

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/username/repo-name.git
cd repo-name
```

### 2. Edit email settings  
In both `webdetec.py` and `webdetec_logger.py`, update the following:
```python
sender_email = "your_email@gmail.com"
sender_password = "your_app_password"   # use Gmail App Password
receiver_email = "your_email@gmail.com"
```

⚠️ For security: use **App Password** in Gmail (not your real password).  

### 3. Run the script
#### Option A – Email only
```bash
python webdetec.py
```
#### Option B – Email + CSV logging
```bash
python webdetec_logger.py
```

The program will:
- Start checking all URLs listed in `urls_opd_makassar.txt`.
- Repeat the detection every 1 hour.
- Send an email report.
- (If using logger) Append results to `hasil_deteksi.csv`.

---

## 📂 File Options

1. **`webdetec.py`**  
   - Checks website status.  
   - Sends summary via **email**.  
   - Use this if you only need reports in your inbox.  

2. **`webdetec_logger.py`**  
   - Same as above (**check + email report**).  
   - **Extra:** Saves results into a CSV log file (`hasil_deteksi.csv`).  
   - Use this if you want **historical logs** for later analysis.  

### Example CSV Log
```csv
Timestamp,URL,Status
2025-09-24 18:00:00,https://data.makassarkota.go.id/,Aktif
2025-09-24 18:00:00,https://dukcapil.makassarkota.go.id/,Nonaktif (Tidak dapat diakses)
```

---

## 📊 Analyzing Logs with Pandas

If you use `webdetec_logger.py`, you can analyze `hasil_deteksi.csv` with Python.

```python
import pandas as pd

# Read log file
df = pd.read_csv("hasil_deteksi.csv")

# Show first 5 rows
print(df.head())

# Count active vs inactive per website
status_counts = df.groupby(["URL", "Status"]).size().unstack(fill_value=0)
print(status_counts)

# Calculate uptime percentage
status_counts["Total"] = status_counts.sum(axis=1)
if "Aktif" in status_counts.columns:
    status_counts["Uptime (%)"] = (status_counts["Aktif"] / status_counts["Total"]) * 100
else:
    status_counts["Uptime (%)"] = 0

print(status_counts[["Total", "Uptime (%)"]])
```

### Example Output
```text
                                   Nonaktif (Tidak dapat diakses)  Aktif  Total  Uptime (%)
https://data.makassarkota.go.id/                               1      9     10       90.0
https://dukcapil.makassarkota.go.id/                           5      5     10       50.0
```

---

## 📈 Future Improvements
- Add **graphical visualization** of uptime with matplotlib.
- Deploy with **Docker** for easier server execution.
- Add **alert notifications** (e.g., Telegram bot, Slack).

---

## 📜 License
This project is open-source and available under the MIT License.
