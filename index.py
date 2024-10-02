import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
from datetime import datetime
import os
from pathlib import Path

class InvoiceGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)

    def add_header(self, invoice_number):
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 10, "INVOICE", ln=1, align="C")
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, f"# {invoice_number}", ln=1, align="C")

    def add_company_details(self, company_name):
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, company_name, ln=1)

    def add_client_details(self, client_name):
        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(0, 10, "Bill To:", ln=1)
        self.pdf.cell(0, 10, client_name, ln=1)
        self.pdf.cell(0, 10, "Ship To:", ln=1)
        self.pdf.cell(0, 10, client_name, ln=1)

    def add_invoice_details(self, payment_terms, po_number):
        today = datetime.now().strftime("%b %d, %Y")
        self.pdf.cell(0, 10, f"Date: {today}", ln=1)
        self.pdf.cell(0, 10, f"Payment Terms: {payment_terms}", ln=1)
        self.pdf.cell(0, 10, f"Due Date: {today}", ln=1)
        self.pdf.cell(0, 10, f"PO Number: {po_number}", ln=1)

    def add_item(self, description, quantity, rate):
        amount = quantity * rate
        self.pdf.cell(90, 10, description, border=1)
        self.pdf.cell(20, 10, str(quantity), border=1, align="C")
        self.pdf.cell(40, 10, f"KES {rate:.2f}", border=1, align="R")
        self.pdf.cell(40, 10, f"KES {amount:.2f}", border=1, align="R", ln=1)
        return amount

    def add_total(self, subtotal):
        self.pdf.cell(150, 10, "Subtotal:", border=1)
        self.pdf.cell(40, 10, f"KES {subtotal:.2f}", border=1, align="R", ln=1)
        self.pdf.cell(150, 10, "Tax:", border=1)
        self.pdf.cell(40, 10, "KES 0.00", border=1, align="R", ln=1)
        self.pdf.cell(150, 10, "Total:", border=1)
        self.pdf.cell(40, 10, f"KES {subtotal:.2f}", border=1, align="R", ln=1)
        self.pdf.cell(150, 10, "Amount Paid:", border=1)
        self.pdf.cell(40, 10, f"KES {subtotal:.2f}", border=1, align="R", ln=1)

    def add_notes_and_terms(self, notes, terms):
        self.pdf.cell(0, 10, "Notes:", ln=1)
        self.pdf.multi_cell(0, 10, notes)
        self.pdf.cell(0, 10, "Terms:", ln=1)
        self.pdf.multi_cell(0, 10, terms)

    def generate_invoice(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"invoice_{timestamp}.pdf"
        home_dir = str(Path.home())
        full_path = os.path.join(home_dir, filename)
        try:
            self.pdf.output(full_path)
            return full_path
        except Exception as e:
            return str(e)

class InvoiceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Invoice Generator")
        self.geometry("400x500")
        self.create_widgets()

    def create_widgets(self):
        labels = ["Invoice Number", "Company Name", "Client Name", "Payment Terms", 
                  "PO Number", "Item Description", "Quantity", "Rate", "Notes", "Terms"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(self, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = tk.Entry(self)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label] = entry

        generate_button = tk.Button(self, text="Generate Invoice", command=self.generate_invoice)
        generate_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def generate_invoice(self):
        generator = InvoiceGenerator()
        generator.add_header(self.entries["Invoice Number"].get())
        generator.add_company_details(self.entries["Company Name"].get())
        generator.add_client_details(self.entries["Client Name"].get())
        generator.add_invoice_details(self.entries["Payment Terms"].get(), self.entries["PO Number"].get())
        
        try:
            quantity = int(self.entries["Quantity"].get())
            rate = float(self.entries["Rate"].get())
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and Rate must be a number.")
            return

        subtotal = generator.add_item(self.entries["Item Description"].get(), quantity, rate)
        generator.add_total(subtotal)
        generator.add_notes_and_terms(self.entries["Notes"].get(), self.entries["Terms"].get())

        result = generator.generate_invoice()
        if os.path.exists(result):
            messagebox.showinfo("Success", f"Invoice generated successfully as '{result}'")
        else:
            messagebox.showerror("Error", f"Failed to generate invoice: {result}")

if __name__ == "__main__":
    app = InvoiceApp()
    app.mainloop()