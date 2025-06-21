import os
from pypdf import PdfReader, PdfWriter
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox

def merge_pdfs_gui(file_paths, output_path):
    writer = PdfWriter()
    for pdf_path in file_paths:
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                writer.add_page(page)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read {pdf_path}:\n{e}")
            return

    if writer.pages:
        with open(output_path, "wb") as out_file:
            writer.write(out_file)
        messagebox.showinfo("Success", f"PDFs merged successfully!\nSaved to: {output_path}")
    else:
        messagebox.showwarning("Warning", "No valid PDF files were merged.")

def browse_files():
    file_paths = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF files", "*.pdf")])
    if file_paths:
        files_entry.delete(0, 'end')
        files_entry.insert(0, ";".join(file_paths))

def choose_save_folder():
    folder = filedialog.askdirectory(title="Choose output folder")
    if folder:
        output_folder_entry.delete(0, 'end')
        output_folder_entry.insert(0, folder)

def start_merge():
    files = files_entry.get().split(";")
    output_name = output_name_entry.get().strip()
    output_folder = output_folder_entry.get().strip()

    if not files or not output_name or not output_folder:
        messagebox.showerror("Missing Info", "Please provide all required inputs.")
        return

    if not output_name.lower().endswith(".pdf"):
        output_name += ".pdf"

    output_path = os.path.join(output_folder, output_name)
    merge_pdfs_gui(files, output_path)

# === GUI SETUP with ttkbootstrap ===
root = tb.Window(themename="darkly")
root.title("PDF Fusion Wizard")
root.geometry("600x360")
root.resizable(False, False)

tb.Label(root, text="Upload PDF Files", font=("Segoe UI", 11)).pack(pady=(20, 5))
files_entry = tb.Entry(root, width=65, bootstyle="dark")
files_entry.pack(pady=2)
tb.Button(root, text="Choose Files", command=browse_files, bootstyle="danger-outline", width=20).pack(pady=5)

tb.Label(root, text="Output File Name", font=("Segoe UI", 11)).pack(pady=(15, 2))
output_name_entry = tb.Entry(root, width=40, bootstyle="dark")
output_name_entry.pack()

tb.Label(root, text="Output Folder", font=("Segoe UI", 11)).pack(pady=(15, 2))
output_folder_entry = tb.Entry(root, width=65, bootstyle="dark")
output_folder_entry.pack(pady=2)
tb.Button(root, text="Choose Folder", command=choose_save_folder, bootstyle="danger-outline", width=20).pack(pady=5)

tb.Button(root, text="Merge PDFs", command=start_merge, bootstyle="danger", width=20).pack(pady=20)

root.mainloop()
