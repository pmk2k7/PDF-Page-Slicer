import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
import os

class PDFSlicerApp:
    def __init__(self, master):
        self.master = master
        master.title("PDF Page Slicer")
        master.geometry("500x400")

        # PDF File Selection
        self.file_label = tk.Label(master, text="Select PDF File:")
        self.file_label.pack(pady=10)

        self.file_path = tk.StringVar()
        self.file_entry = tk.Entry(master, textvariable=self.file_path, width=50)
        self.file_entry.pack(pady=5)

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_pdf)
        self.browse_button.pack(pady=5)

        # Output Folder Selection
        self.output_label = tk.Label(master, text="Select Output Folder:")
        self.output_label.pack(pady=10)

        self.output_path = tk.StringVar()
        self.output_entry = tk.Entry(master, textvariable=self.output_path, width=50)
        self.output_entry.pack(pady=5)

        self.output_browse_button = tk.Button(master, text="Browse", command=self.browse_output)
        self.output_browse_button.pack(pady=5)

        # Page Range Input
        self.start_label = tk.Label(master, text="Start Page:")
        self.start_label.pack(pady=5)
        self.start_page = tk.Entry(master, width=10)
        self.start_page.pack()

        self.end_label = tk.Label(master, text="End Page:")
        self.end_label.pack(pady=5)
        self.end_page = tk.Entry(master, width=10)
        self.end_page.pack()

        # Slice Button
        self.slice_button = tk.Button(master, text="Slice PDF", command=self.slice_pdf)
        self.slice_button.pack(pady=20)

        # Status Label
        self.status_label = tk.Label(master, text="", fg="green")
        self.status_label.pack(pady=10)

    def browse_pdf(self):
        filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        self.file_path.set(filename)

    def browse_output(self):
        folder = filedialog.askdirectory()
        self.output_path.set(folder)

    def slice_pdf(self):
        # Validate inputs
        if not self.file_path.get():
            messagebox.showerror("Error", "Please select a PDF file")
            return

        if not self.output_path.get():
            messagebox.showerror("Error", "Please select an output folder")
            return

        try:
            start = int(self.start_page.get())
            end = int(self.end_page.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid page numbers")
            return

        # Adjust for 0-based indexing
        start -= 1
        end -= 1

        try:
            # Read the PDF
            pdf_reader = PdfReader(open(self.file_path.get(), 'rb'))
            
            # Validate page range
            if start < 0 or end >= len(pdf_reader.pages) or start > end:
                messagebox.showerror("Error", "Invalid page range")
                return

            # Create PDF writer
            pdf_writer = PdfWriter()

            # Add selected pages
            for page_num in range(start, end + 1):
                pdf_writer.add_page(pdf_reader.pages[page_num])

            # Generate output filename
            input_filename = os.path.basename(self.file_path.get())
            output_filename = f"sliced_{input_filename}"
            output_path = os.path.join(self.output_path.get(), output_filename)

            # Write the sliced PDF
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)

            # Update status
            self.status_label.config(text=f"PDF sliced successfully!\nSaved to: {output_path}", fg="green")

        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = PDFSlicerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
