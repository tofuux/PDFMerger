import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pypdf import PdfReader, PdfWriter

class PDFMergerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Merger Tool")
        self.geometry("600x400")
        self.configure(bg="#fdeaea")
        self.file_paths = []

        self.build_ui()

    def build_ui(self):
        title = tk.Label(self, text="Upload PDF Files", font=("Helvetica", 16, "bold"), bg="#fdeaea")
        title.pack(pady=10)

        drop_frame = tk.Frame(self, bg="black", width=500, height=150)
        drop_frame.pack(pady=10)
        drop_frame.pack_propagate(False)

        choose_button = tk.Button(drop_frame, text="Choose Files", command=self.choose_files, bg="red", fg="white", font=("Arial", 12, "bold"))
        choose_button.pack(pady=20)

        self.file_listbox = tk.Listbox(self, selectmode=tk.SINGLE, width=60, height=6)
        self.file_listbox.pack(pady=10)

        # Controls
        control_frame = tk.Frame(self, bg="#fdeaea")
        control_frame.pack()

        up_button = tk.Button(control_frame, text="↑ Move Up", command=self.move_up)
        up_button.grid(row=0, column=0, padx=10)

        down_button = tk.Button(control_frame, text="↓ Move Down", command=self.move_down)
        down_button.grid(row=0, column=1, padx=10)

        merge_button = tk.Button(self, text="Merge PDFs", command=self.merge_pdfs, bg="green", fg="white", font=("Arial", 12))
        merge_button.pack(pady=15)

    def choose_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if files:
            self.file_paths = list(files)
            self.refresh_file_list()

    def refresh_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for path in self.file_paths:
            self.file_listbox.insert(tk.END, os.path.basename(path))

    def move_up(self):
        sel = self.file_listbox.curselection()
        if sel and sel[0] > 0:
            i = sel[0]
            self.file_paths[i-1], self.file_paths[i] = self.file_paths[i], self.file_paths[i-1]
            self.refresh_file_list()
            self.file_listbox.select_set(i-1)

    def move_down(self):
        sel = self.file_listbox.curselection()
        if sel and sel[0] < len(self.file_paths) - 1:
            i = sel[0]
            self.file_paths[i+1], self.file_paths[i] = self.file_paths[i], self.file_paths[i+1]
            self.refresh_file_list()
            self.file_listbox.select_set(i+1)

    def merge_pdfs(self):
        if not self.file_paths:
            messagebox.showerror("Error", "No PDF files selected.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF File", "*.pdf")])
        if not save_path:
            return

        writer = PdfWriter()
        for path in self.file_paths:
            try:
                reader = PdfReader(path)
                for page in reader.pages:
                    writer.add_page(page)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read {path}:\n{e}")
                return

        with open(save_path, "wb") as out_file:
            writer.write(out_file)

        messagebox.showinfo("Success", f"Merged PDF saved to:\n{save_path}")

if __name__ == "__main__":
    app = PDFMergerApp()
    app.mainloop()
