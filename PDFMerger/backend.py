import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime


class PDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Fusion Wizard")
        self.root.configure(bg="#d62c2c")
        self.root.geometry("600x500")

        self.selected_files = []
        self.page_ranges = {}

        self.create_tabs()

    def create_tabs(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#1c1c1c", borderwidth=0)
        style.configure("TNotebook.Tab", background="#2b2b2b", foreground="white", padding=10)
        style.map("TNotebook.Tab", background=[("selected", "#d53b3b")])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.merge_tab = tk.Frame(self.notebook, bg="#1c1c1c")
        self.split_tab = tk.Frame(self.notebook, bg="#1c1c1c")

        self.notebook.add(self.merge_tab, text='Merge PDFs')
        self.notebook.add(self.split_tab, text='Split PDF')

        self.build_merge_tab()
        self.build_split_tab()

    def build_merge_tab(self):
        self.file_listbox = tk.Listbox(self.merge_tab, bg="#2b2b2b", fg="white", height=6)
        self.file_listbox.pack(pady=10, padx=30, fill="x")

        self.add_outline_button(self.merge_tab, "Choose Files", self.choose_files)
        self.add_outline_button(self.merge_tab, "Choose Folder", self.choose_folder)
        self.add_outline_button(self.merge_tab, "Select Entire Folder", self.select_entire_folder)

        control_frame = tk.Frame(self.merge_tab, bg="#1c1c1c")
        control_frame.pack(pady=5)

        self.add_standard_button(control_frame, "Move Up", self.move_up).pack(side="left", padx=5)
        self.add_standard_button(control_frame, "Move Down", self.move_down).pack(side="left", padx=5)

        self.page_range_entry = self.create_entry(self.merge_tab, "Enter page ranges (e.g., 1-3,5 for each file)")

        self.output_file_name = self.create_entry(self.merge_tab, "Output file name")

        self.add_outline_button(self.merge_tab, "Merge PDFs", self.merge_pdfs)

    def build_split_tab(self):
        self.split_file_entry = self.create_entry(self.split_tab, "Choose PDF to split")
        self.add_outline_button(self.split_tab, "Browse PDF", self.browse_split_pdf)

        self.split_range_entry = self.create_entry(self.split_tab, "Split after every N pages")
        self.add_outline_button(self.split_tab, "Split PDF", self.split_pdf)

    def create_entry(self, parent, placeholder):
        entry = tk.Entry(parent, bg="#a92626", fg="white", insertbackground="white", relief="flat", font=("Segoe UI", 10))
        entry.insert(0, placeholder)
        entry.pack(pady=6, ipadx=5, ipady=5, fill='x', padx=30)
        return entry

    def add_outline_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, command=command,
                        fg="white", bg="#1c1c1c", activebackground="#2b2b2b", activeforeground="white",
                        relief="solid", bd=1, highlightthickness=0, font=("Segoe UI", 9))
        btn.config(highlightbackground="red", highlightcolor="red", borderwidth=2)
        btn.pack(pady=6, ipadx=10, ipady=4)
        return btn

    def add_standard_button(self, parent, text, command):
        return tk.Button(parent, text=text, command=command, relief="flat", bg="#2b2b2b", fg="white")

    def choose_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        for file in files:
            if file not in self.selected_files:
                self.selected_files.append(file)
                pages = len(PdfReader(file).pages)
                self.file_listbox.insert(tk.END, f"{os.path.basename(file)} ({pages} pages)")

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            pdfs = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.pdf')]
            for file in pdfs:
                if file not in self.selected_files:
                    self.selected_files.append(file)
                    pages = len(PdfReader(file).pages)
                    self.file_listbox.insert(tk.END, f"{os.path.basename(file)} ({pages} pages)")

    def select_entire_folder(self):
        self.choose_folder()

    def move_up(self):
        idx = self.file_listbox.curselection()
        if idx and idx[0] > 0:
            i = idx[0]
            self.selected_files[i], self.selected_files[i-1] = self.selected_files[i-1], self.selected_files[i]
            temp = self.file_listbox.get(i)
            self.file_listbox.delete(i)
            self.file_listbox.insert(i-1, temp)
            self.file_listbox.select_set(i-1)

    def move_down(self):
        idx = self.file_listbox.curselection()
        if idx and idx[0] < self.file_listbox.size() - 1:
            i = idx[0]
            self.selected_files[i], self.selected_files[i+1] = self.selected_files[i+1], self.selected_files[i]
            temp = self.file_listbox.get(i)
            self.file_listbox.delete(i)
            self.file_listbox.insert(i+1, temp)
            self.file_listbox.select_set(i+1)

    def merge_pdfs(self):
        output_name = self.output_file_name.get().strip() or "merged_output.pdf"
        if not output_name.endswith(".pdf"):
            output_name += ".pdf"
        writer = PdfWriter()
        page_ranges = self.page_range_entry.get().strip().split(',')

        for file in self.selected_files:
            reader = PdfReader(file)
            total_pages = len(reader.pages)
            ranges = page_ranges if page_ranges != [''] else [f"0-{total_pages-1}"]
            for r in ranges:
                if '-' in r:
                    start, end = map(int, r.split('-'))
                    for i in range(start, end+1):
                        if i < total_pages:
                            writer.add_page(reader.pages[i])
                else:
                    i = int(r)
                    if i < total_pages:
                        writer.add_page(reader.pages[i])

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=output_name)
        if output_path:
            with open(output_path, 'wb') as f:
                writer.write(f)
            self.log_merge(output_path)

    def log_merge(self, output_path):
        with open("merge_log.txt", "a") as log:
            log.write(f"{datetime.now()} - Merged into {output_path}\n")
            for file in self.selected_files:
                log.write(f"  {file}\n")
            log.write("\n")

    def browse_split_pdf(self):
        file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        self.split_file_entry.delete(0, tk.END)
        self.split_file_entry.insert(0, file)

    def split_pdf(self):
        file = self.split_file_entry.get()
        if not file or not os.path.exists(file):
            messagebox.showerror("Error", "Invalid file")
            return
        reader = PdfReader(file)
        pages_per_split = int(self.split_range_entry.get() or 1)
        total_pages = len(reader.pages)

        for i in range(0, total_pages, pages_per_split):
            writer = PdfWriter()
            for j in range(i, min(i+pages_per_split, total_pages)):
                writer.add_page(reader.pages[j])
            output_path = f"{file[:-4]}_part{i//pages_per_split+1}.pdf"
            with open(output_path, 'wb') as f:
                writer.write(f)

        messagebox.showinfo("Success", "PDF split successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFApp(root)
    root.mainloop()
