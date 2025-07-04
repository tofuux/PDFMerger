import os
from pypdf import PdfReader, PdfWriter
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, Listbox, Scrollbar, SINGLE, END, MULTIPLE, Toplevel, StringVar
import datetime

log_file_path = "merge_log.txt"

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Fusion Wizard")
        root.geometry("700x600") 
        root.resizable(True, True)


        self.file_list = []
        self.page_ranges = {}

        self.build_gui()

    def build_gui(self):
        tb.Label(root, text="Selected PDF Files", font=("Segoe UI", 11)).pack(pady=(10, 5))

        list_frame = tb.Frame(root)
        list_frame.pack()

        self.file_listbox = Listbox(list_frame, width=80, height=8, selectmode=SINGLE)
        self.file_listbox.pack(side="left")

        scroll = Scrollbar(list_frame, command=self.file_listbox.yview)
        scroll.pack(side="right", fill="y")
        self.file_listbox.config(yscrollcommand=scroll.set)

        button_frame = tb.Frame(root)
        button_frame.pack(pady=5)

        tb.Button(button_frame, text="Move Up", command=self.move_up, width=10).pack(side="left", padx=5)
        tb.Button(button_frame, text="Move Down", command=self.move_down, width=10).pack(side="left", padx=5)
        tb.Button(button_frame, text="Set Page Range", command=self.set_page_range, width=15).pack(side="left", padx=5)

        tb.Button(root, text="Add Files", command=self.browse_files, bootstyle="danger-outline", width=20).pack(pady=5)
        tb.Button(root, text="Add Folder", command=self.add_folder_pdfs, bootstyle="danger-outline", width=20).pack(pady=5)

        tb.Label(root, text="Output File Name", font=("Segoe UI", 11)).pack(pady=(15, 2))
        self.output_name_entry = tb.Entry(root, width=40, bootstyle="dark")
        self.output_name_entry.pack()

        tb.Label(root, text="Output Folder", font=("Segoe UI", 11)).pack(pady=(15, 2))
        self.output_folder_entry = tb.Entry(root, width=65, bootstyle="dark")
        self.output_folder_entry.pack(pady=2)
        tb.Button(root, text="Choose Folder", command=self.choose_save_folder, bootstyle="danger-outline", width=20).pack(pady=5)

        tb.Button(root, text="Merge PDFs", command=self.start_merge, bootstyle="danger", width=20).pack(pady=20)
        tb.Button(root, text="Split PDF", command=self.split_pdf_gui, bootstyle="warning-outline", width=20).pack()

    def browse_files(self):
        files = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF files", "*.pdf")])
        for f in files:
            if f not in self.file_list:
                self.file_list.append(f)
                self.file_listbox.insert(END, f)

    def add_folder_pdfs(self):
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            for f in os.listdir(folder):
                if f.lower().endswith(".pdf"):
                    full_path = os.path.join(folder, f)
                    if full_path not in self.file_list:
                        self.file_list.append(full_path)
                        self.file_listbox.insert(END, full_path)

    def choose_save_folder(self):
        folder = filedialog.askdirectory(title="Choose output folder")
        if folder:
            self.output_folder_entry.delete(0, END)
            self.output_folder_entry.insert(0, folder)

    def move_up(self):
        sel = self.file_listbox.curselection()
        if sel and sel[0] > 0:
            idx = sel[0]
            self.file_list[idx - 1], self.file_list[idx] = self.file_list[idx], self.file_list[idx - 1]
            self.refresh_listbox()
            self.file_listbox.select_set(idx - 1)

    def move_down(self):
        sel = self.file_listbox.curselection()
        if sel and sel[0] < len(self.file_list) - 1:
            idx = sel[0]
            self.file_list[idx + 1], self.file_list[idx] = self.file_list[idx], self.file_list[idx + 1]
            self.refresh_listbox()
            self.file_listbox.select_set(idx + 1)

    def refresh_listbox(self):
        self.file_listbox.delete(0, END)
        for f in self.file_list:
            self.file_listbox.insert(END, f)

    def set_page_range(self):
        sel = self.file_listbox.curselection()
        if not sel:
            messagebox.showinfo("Select File", "Please select a file to set page range.")
            return

        file_path = self.file_list[sel[0]]
        top = Toplevel(root)
        top.title("Set Page Range")
        top.geometry("300x100")

        tb.Label(top, text="Enter page range (e.g., 1-3,5)").pack(pady=5)
        range_entry = tb.Entry(top, width=30)
        range_entry.pack(pady=5)

        def save_range():
            self.page_ranges[file_path] = range_entry.get()
            top.destroy()

        tb.Button(top, text="Save", command=save_range).pack(pady=5)

    def parse_range(self, text):
        pages = set()
        for part in text.split(','):
            if '-' in part:
                a, b = map(int, part.split('-'))
                pages.update(range(a-1, b))
            else:
                pages.add(int(part)-1)
        return sorted(pages)

    def start_merge(self):
        files = self.file_list
        output_name = self.output_name_entry.get().strip()
        output_folder = self.output_folder_entry.get().strip()

        if not files or not output_name or not output_folder:
            messagebox.showerror("Missing Info", "Please provide all required inputs.")
            return

        if not output_name.lower().endswith(".pdf"):
            output_name += ".pdf"

        output_path = os.path.join(output_folder, output_name)

        writer = PdfWriter()
        for file in files:
            try:
                reader = PdfReader(file)
                total_pages = len(reader.pages)
                if file in self.page_ranges:
                    pages = self.parse_range(self.page_ranges[file])
                    pages = [p for p in pages if 0 <= p < total_pages]
                else:
                    pages = range(total_pages)

                for p in pages:
                    writer.add_page(reader.pages[p])
            except Exception as e:
                messagebox.showerror("Error", f"Could not read {file}:\n{e}")
                return

        if writer.pages:
            with open(output_path, "wb") as out_file:
                writer.write(out_file)
            messagebox.showinfo("Success", f"PDFs merged successfully!\nSaved to: {output_path}")
            self.log_merge(files, output_path)
        else:
            messagebox.showwarning("Warning", "No valid PDF files were merged.")

    def log_merge(self, files, output):
        with open(log_file_path, "a") as log:
            log.write(f"\n[{datetime.datetime.now()}] Merged into: {output}\n")
            for f in files:
                log.write(f" - {f}\n")

    def split_pdf_gui(self):
        file_path = filedialog.askopenfilename(title="Select PDF to Split", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return

        split_top = Toplevel(root)
        split_top.title("Split PDF")
        split_top.geometry("300x200")

        tb.Label(split_top, text="Split Options").pack(pady=5)

        range_var = StringVar()
        tb.Radiobutton(split_top, text="Each Page", variable=range_var, value="each").pack()
        tb.Radiobutton(split_top, text="Every N Pages", variable=range_var, value="n").pack()
        tb.Label(split_top, text="N =").pack()
        n_entry = tb.Entry(split_top, width=10)
        n_entry.pack()

        def do_split():
            reader = PdfReader(file_path)
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            folder = filedialog.askdirectory(title="Select Output Folder")
            if not folder:
                return

            if range_var.get() == "each":
                for i, page in enumerate(reader.pages):
                    writer = PdfWriter()
                    writer.add_page(page)
                    with open(os.path.join(folder, f"{base_name}_page_{i+1}.pdf"), "wb") as out:
                        writer.write(out)
            elif range_var.get() == "n":
                try:
                    n = int(n_entry.get())
                    for i in range(0, len(reader.pages), n):
                        writer = PdfWriter()
                        for j in range(i, min(i + n, len(reader.pages))):
                            writer.add_page(reader.pages[j])
                        with open(os.path.join(folder, f"{base_name}_part_{i//n + 1}.pdf"), "wb") as out:
                            writer.write(out)
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter a valid number for N.")

            messagebox.showinfo("Process completed", " Split PDF.")
            split_top.destroy()

        tb.Button(split_top, text="Split", command=do_split, bootstyle="success").pack(pady=10)

if __name__ == '__main__':
    root = tb.Window(themename="darkly")
    app = PDFMergerApp(root)
    root.mainloop()
