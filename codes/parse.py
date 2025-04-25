import time
import os
from llama_parse import LlamaParse

# Catat waktu mulai
start_time = time.time()

# API key
api_key = "llx-yom5lc4fqes8xtq2dkne1YpVZSvNvZ7UWfItriNtJ6yj3NLX"

# Inisialisasi parser dengan parameter minimal
parser = LlamaParse(
    api_key=api_key,
    result_type="markdown",
    parse_mode="parse_document_with_lvm",  # Coba mode document untuk ekstraksi lengkap
    verbose=True
    # Hilangkan parameter yang tidak didukung untuk sementara
)

# Path file PDF
pdf_path = "pneumonia.pdf"
print(f"🚀 Parsing dokumen: {pdf_path}")

try:
    print("⏳ Memulai proses parsing...")
    
    # Coba cetak versi LlamaParse jika memungkinkan
    try:
        import llama_parse
        print(f"LlamaParse version: {llama_parse.__version__}")
    except:
        print("Tidak dapat menentukan versi LlamaParse")
    
    docs = parser.load_data(pdf_path)
    
    if docs and len(docs) > 0:
        doc = docs[0]
        
        # Loop menunggu hasil parsing dengan waktu tunggu lebih lama
        for i in range(30):
            if doc.text != "NO_CONTENT_HERE":
                break
            print(f"⏳ Menunggu hasil parsing... ({(i+1)*6} detik)")
            time.sleep(6)
        
        # Simpan hasil parsing
        if doc.text != "NO_CONTENT_HERE":
            with open("hasil_pneumonia_full.md", "w", encoding="utf-8") as f:
                f.write(doc.text)
            
            print("✅ Markdown berhasil disimpan")
            
            # Tampilkan informasi ukuran file
            file_size = os.path.getsize("hasil_pneumonia_full.md") / 1024  # Konversi ke KB
            print(f"📊 Ukuran file hasil: {file_size:.2f} KB")
            
            # Simpan juga metadata jika ada
            try:
                if hasattr(doc, 'metadata') and doc.metadata:
                    with open("metadata_pneumonia.json", "w", encoding="utf-8") as f:
                        import json
                        json.dump(doc.metadata, f, indent=2)
                    print("✅ Metadata berhasil disimpan ke metadata_pneumonia.json")
            except:
                print("⚠️ Tidak dapat menyimpan metadata")
        else:
            print("❌ Gagal parsing setelah waktu tunggu maksimum")
    else:
        print("❌ Tidak ada hasil parsing yang diterima")
        
except Exception as e:
    print(f"❌ Terjadi kesalahan: {str(e)}")

# Catat waktu selesai dan tampilkan total waktu
end_time = time.time()
print(f"⏱️ Total waktu pemrosesan: {end_time - start_time:.2f} detik")