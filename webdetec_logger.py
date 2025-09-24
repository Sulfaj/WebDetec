# webdetec_logger.py
# Versi dengan logging ke CSV selain mengirim email

import requests
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import os

def cek_status_web(url):
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            return "Aktif"
        else:
            return f"Nonaktif (Status code: {response.status_code})"
    except requests.RequestException:
        return "Nonaktif (Tidak dapat diakses)"

def send_email_report(hasil, timestamp):
    sender_email = "your_email@gmail.com"     # ganti dengan email kamu
    sender_password = "your_app_password"     # ganti dengan app password Gmail
    receiver_email = "your_email@gmail.com"

    subject = f"Laporan Deteksi Website OPD Makassar {timestamp}"
    body = "Ringkasan hasil deteksi website OPD Kota Makassar:\n\n"
    for item in hasil:
        body += f"{item['url']} : {item['status']}\n"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"Ringkasan hasil deteksi telah dikirim ke {receiver_email}")
    except Exception as e:
        print(f"Gagal mengirim email: {e}")

def log_to_csv(hasil, timestamp, filename="hasil_deteksi.csv"):
    """Simpan hasil deteksi ke file CSV (append mode)."""
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # tulis header kalau file baru
        if not file_exists:
            writer.writerow(["Timestamp", "URL", "Status"])
        for item in hasil:
            writer.writerow([timestamp, item["url"], item["status"]])
    print(f"Hasil deteksi tersimpan ke {filename}")

def run_detection():
    with open("urls_opd_makassar.txt", "r", encoding="utf-8") as f:
        daftar_web = [line.strip() for line in f if line.strip()]

    hasil = []
    for web in daftar_web:
        status = cek_status_web(web)
        hasil.append({"url": web, "status": status})
        print(f"{web} : {status}")

    # timestamp sekali untuk semua hasil
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # kirim email
    send_email_report(hasil, timestamp)
    # simpan ke CSV
    log_to_csv(hasil, timestamp)

if __name__ == "__main__":
    while True:
        print(f"\nMulai pengecekan pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        run_detection()
        print("Menunggu 1 jam untuk pengecekan berikutnya...")
        time.sleep(3600)
