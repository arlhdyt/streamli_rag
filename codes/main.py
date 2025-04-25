# main.py


from ask_groq import ask_groq

if __name__ == "__main__":
    file_path = "data/01_Pneumonia_Komunitas.pdf"
    question = "Apa saja bakteri penyebab pneumonia komunitas?"

    print("🔄 Parsing dokumen...")
    markdown = parse_pdf_to_markdown(file_path)
    print("✅ Parsing selesai. Simpan sebagai 'parsed_output.md'")

    with open("parsed_output.md", "w", encoding="utf-8") as f:
        f.write(markdown)

    print("🤖 Menanyakan ke Groq...")
    answer = ask_groq(question, markdown)
    print("🟢 Jawaban Groq:")
    print(answer)
