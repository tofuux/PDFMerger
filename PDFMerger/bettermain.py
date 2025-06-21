import os
from pypdf import PdfReader, PdfWriter

def merge_pdfs(file_name, folder_path, output_path):
    writer = PdfWriter()

    for name in file_name:
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
    # Ask for input files
    input_files = input("Enter PDF filenames (comma-separated, e.g., one.pdf, two.pdf):\n> ")
    file_list = input_files.split(",")

    # Ask for folder containing the PDFs
    folder_path = input("Enter the folder path where the PDFs are located:\n> ").strip()

    # Ask for output file name
    output_file_name = input("Enter the name for the merged PDF (e.g., merged.pdf):\n> ").strip()

    # Ask for output folder path
    output_folder = input("Enter the folder path where you want to save the merged PDF:\n> ").strip()

    # Ensure .pdf extension
    if not output_file_name.lower().endswith(".pdf"):
        output_file_name += ".pdf"

    output_path = os.path.join(output_folder, output_file_name)

    merge_pdfs(file_list, folder_path, output_path)
 