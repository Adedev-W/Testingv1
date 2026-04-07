#!/bin/bash

echo "Mulai proses setup FastAPI..."

# Membuat virtual environment (opsional tapi disarankan)
echo "Membuat virtual environment (venv)..."
python -m venv venv

# Mengaktifkan virtual environment
source venv/bin/activate || source venv/Scripts/activate

# Menginstal library dari requirements.txt
echo "Menginstal library yang dibutuhkan..."
pip install -r requirements.txt

echo "Setup selesai! Menjalankan server FastAPI..."
echo "Akses dokumentasi API di: http://127.0.0.1:8000/docs"

# Menjalankan server menggunakan uvicorn dengan fitur auto-reload
uvicorn main:app --reload
