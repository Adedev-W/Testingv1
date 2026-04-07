from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import os

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="API CRUD Produk",
    description="API sederhana untuk manajemen produk menggunakan file JSON",
    version="1.0.0"
)

# Nama file JSON yang akan bertindak sebagai database
FILE_DB = "database_produk.json"

# Model Data menggunakan Pydantic
class Produk(BaseModel):
    id: int
    nama: str
    deskripsi: Optional[str] = None
    harga: float
    stok: int

# Fungsi Bantuan: Membaca data dari file JSON
def baca_data() -> List[dict]:
    if not os.path.exists(FILE_DB):
        return []
    with open(FILE_DB, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

# Fungsi Bantuan: Menyimpan data ke file JSON
def simpan_data(data: List[dict]):
    with open(FILE_DB, "w") as file:
        json.dump(data, file, indent=4)

# ==========================================
# ENDPOINT CRUD
# ==========================================

# 1. READ ALL (Mendapatkan semua produk)
@app.get("/produk", response_model=List[Produk], tags=["Produk"])
def ambil_semua_produk():
    """Mengambil daftar semua produk yang ada di database."""
    return baca_data()

# 2. READ ONE (Mendapatkan satu produk berdasarkan ID)
@app.get("/produk/{produk_id}", response_model=Produk, tags=["Produk"])
def ambil_satu_produk(produk_id: int):
    """Mengambil detail satu produk berdasarkan ID-nya."""
    data_produk = baca_data()
    for produk in data_produk:
        if produk["id"] == produk_id:
            return produk
    
    # Jika tidak ditemukan, kembalikan error 404
    raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

# 3. CREATE (Menambahkan produk baru)
@app.post("/produk", response_model=Produk, tags=["Produk"], status_code=201)
def tambah_produk(produk_baru: Produk):
    """Menambahkan produk baru ke dalam database JSON."""
    data_produk = baca_data()
    
    # Cek apakah ID sudah ada
    for produk in data_produk:
        if produk["id"] == produk_baru.id:
            raise HTTPException(status_code=400, detail="ID Produk sudah digunakan")
            
    # Tambahkan produk ke list dan simpan
    data_produk.append(produk_baru.model_dump())
    simpan_data(data_produk)
    return produk_baru

# 4. UPDATE (Mengubah data produk yang ada)
@app.put("/produk/{produk_id}", response_model=Produk, tags=["Produk"])
def perbarui_produk(produk_id: int, produk_update: Produk):
    """Memperbarui data produk yang sudah ada berdasarkan ID."""
    data_produk = baca_data()
    
    for index, produk in enumerate(data_produk):
        if produk["id"] == produk_id:
            # Memastikan ID tidak berubah (opsional, tergantung kebutuhan bisnis)
            if produk_update.id != produk_id:
                raise HTTPException(status_code=400, detail="Tidak diizinkan mengubah ID produk")
                
            data_produk[index] = produk_update.model_dump()
            simpan_data(data_produk)
            return produk_update
            
    raise HTTPException(status_code=404, detail="Produk tidak ditemukan untuk diperbarui")

# 5. DELETE (Menghapus produk)
@app.delete("/produk/{produk_id}", tags=["Produk"])
def hapus_produk(produk_id: int):
    """Menghapus produk dari database berdasarkan ID."""
    data_produk = baca_data()
    
    for index, produk in enumerate(data_produk):
        if produk["id"] == produk_id:
            data_produk.pop(index)
            simpan_data(data_produk)
            return {"pesan": f"Produk dengan ID {produk_id} berhasil dihapus"}
            
    raise HTTPException(status_code=404, detail="Produk tidak ditemukan untuk dihapus")
