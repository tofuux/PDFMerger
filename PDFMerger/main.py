import os
from pypdf import PdfReader, PdfWriter

def merge_pdfs(file_names, folder_path, output_path):
    writer = PdfWriter()

    for name in file_names:
        pdf_path = os.path.join(folder_path, name.strip())
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                writer.add_page(page)
        except FileNotFoundError:
            print(f"❌ File not found: {pdf_path}")
        except Exception as e:
            print(f"⚠️ Error reading {pdf_path}: {e}")

    if writer.pages:
        with open(output_path, "wb") as out_file:
            writer.write(out_file)
        print(f"✅ PDFs merged successfully into {output_path}")
    else:
        print("❗ No valid PDF files were merged.")

# === MAIN EXECUTION ===
if __name__ == "__main__":
    input_files = input("Enter PDF filenames (comma-separated):\n> ")
    file_list = input_files.split(",")

    folder = os.path.join(os.path.dirname(__file__), "pdfs")
    output_file = os.path.join(os.path.dirname(__file__), "merged.pdf")

    merge_pdfs(file_list, folder, output_file)
