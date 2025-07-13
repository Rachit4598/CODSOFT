import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, os, csv

CONTACT_FILE = "contacts.json"

class SmartContactManager:
    def __init__(self, window):
        self.window = window
        self.window.title("📘 Smart Contact Manager")
        self.window.geometry("850x580")
        self.window.configure(bg="#F4F6F8")

        self.contact_list = []
        self.load_data()
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.window, text="Smart Contact Manager", font=("Segoe UI", 22, "bold"), bg="#F4F6F8", fg="#2C3E50").pack(pady=10)

        form_frame = tk.Frame(self.window, bg="#F4F6F8")
        form_frame.pack(pady=5)

        self.fields = {}
        for i, field in enumerate(["Full Name", "Phone No.", "Email ID", "Residence"]):
            tk.Label(form_frame, text=field + ":", font=("Segoe UI", 11, "bold"), bg="#F4F6F8", fg="#2C3E50").grid(row=i, column=0, sticky='e', pady=3)
            entry = tk.Entry(form_frame, width=42)
            entry.grid(row=i, column=1, padx=10)
            self.fields[field.lower()] = entry

        btn_frame = tk.Frame(self.window, bg="#F4F6F8")
        btn_frame.pack(pady=10)

        buttons = [
            ("➕ Add", "#27AE60", self.add_entry),
            ("✏️ Edit", "#F39C12", self.edit_entry),
            ("🗑️ Remove", "#E74C3C", self.remove_entry),
            ("🔄 Reset", "#34495E", self.reset_fields),
            ("📤 Export CSV", "#8E44AD", self.export_csv)
        ]
        for i, (text, color, cmd) in enumerate(buttons):
            tk.Button(btn_frame, text=text, bg=color, fg="white", font=("Segoe UI", 11, "bold"), command=cmd).grid(row=0, column=i, padx=6)

        search_frame = tk.Frame(self.window, bg="#F4F6F8")
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="🔍 Search:", font=("Segoe UI", 11, "bold"), bg="#F4F6F8", fg="#2C3E50").grid(row=0, column=0)
        self.search_input = tk.Entry(search_frame, width=35)
        self.search_input.grid(row=0, column=1, padx=8)
        tk.Button(search_frame, text="Find", bg="#2C3E50", fg="white", font=("Segoe UI", 10, "bold"), command=self.search_entry).grid(row=0, column=2)

        tk.Button(search_frame, text="Sort by Name", bg="#16A085", fg="white", font=("Segoe UI", 10), command=self.sort_name).grid(row=0, column=3, padx=5)
        tk.Button(search_frame, text="Sort by Number", bg="#2980B9", fg="white", font=("Segoe UI", 10), command=self.sort_phone).grid(row=0, column=4)

        self.tree = ttk.Treeview(self.window, columns=("Name", "Phone", "Email", "Address"), show="headings", height=10)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#3F51B5", foreground="white")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28, background="white", fieldbackground="white")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200, anchor='center')
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)
        self.tree.bind("<ButtonRelease-1>", self.select_row)

        self.status = tk.Label(self.window, text="Ready", bg="#F4F6F8", fg="#27AE60", font=("Segoe UI", 10), anchor='w')
        self.status.pack(fill=tk.X)

        self.refresh_tree()

    def load_data(self):
        if os.path.exists(CONTACT_FILE):
            try:
                with open(CONTACT_FILE, 'r') as f:
                    self.contact_list = json.load(f)
                    if not isinstance(self.contact_list, list):
                        self.contact_list = []
            except:
                self.contact_list = []
        else:
            self.contact_list = []

    def save_data(self):
        with open(CONTACT_FILE, 'w') as f:
            json.dump(self.contact_list, f, indent=2)

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for contact in self.contact_list:
            self.tree.insert("", "end", values=(
                contact.get('full name', ''),
                contact.get('phone no.', ''),
                contact.get('email id', ''),
                contact.get('residence', '')
            ))
        self.status.config(text=f"{len(self.contact_list)} contacts loaded.")
        self.search_input.delete(0, tk.END)

    def add_entry(self):
        data = {k: v.get().strip() for k, v in self.fields.items()}
        if not data['full name'] or not data['phone no.']:
            messagebox.showwarning("Missing Fields", "Full Name and Phone No. are required.")
            return
        if any(c.get('phone no.') == data['phone no.'] for c in self.contact_list):
            messagebox.showwarning("Duplicate", "Phone number already exists.")
            return
        self.contact_list.append(data)
        self.save_data()
        self.refresh_tree()
        self.reset_fields()
        self.status.config(text="Contact added.")

    def edit_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Contact", "Please select a contact to edit.")
            return
        index = self.tree.index(selected[0])
        updated = {k: v.get().strip() for k, v in self.fields.items()}
        self.contact_list[index] = updated
        self.save_data()
        self.refresh_tree()
        self.reset_fields()
        self.status.config(text="Contact updated.")

    def remove_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Contact", "Please select a contact to delete.")
            return
        index = self.tree.index(selected[0])
        if messagebox.askyesno("Confirm", "Delete this contact?"):
            del self.contact_list[index]
            self.save_data()
            self.refresh_tree()
            self.reset_fields()
            self.status.config(text="Contact deleted.")

    def reset_fields(self):
        for field in self.fields.values():
            field.delete(0, tk.END)
        self.search_input.delete(0, tk.END)
        self.status.config(text="Fields cleared.")

    def select_row(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            for i, key in enumerate(self.fields.keys()):
                self.fields[key].delete(0, tk.END)
                self.fields[key].insert(0, values[i])

    def search_entry(self):
        term = self.search_input.get().lower()
        results = [c for c in self.contact_list if term in c.get('full name', '').lower() or term in c.get('phone no.', '')]
        self.tree.delete(*self.tree.get_children())
        for contact in results:
            self.tree.insert("", "end", values=(
                contact.get('full name', ''),
                contact.get('phone no.', ''),
                contact.get('email id', ''),
                contact.get('residence', '')
            ))
        self.status.config(text=f"{len(results)} match(es) found.")

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV File", "*.csv")])
        if path:
            with open(path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Full Name", "Phone No.", "Email ID", "Residence"])
                for c in self.contact_list:
                    writer.writerow([
                        c.get('full name', ''),
                        c.get('phone no.', ''),
                        c.get('email id', ''),
                        c.get('residence', '')
                    ])
            self.status.config(text="Contacts exported.")

    def sort_name(self):
        self.contact_list.sort(key=lambda x: x.get('full name', '').lower())
        self.refresh_tree()
        self.status.config(text="Sorted by Name.")

    def sort_phone(self):
        self.contact_list.sort(key=lambda x: x.get('phone no.', ''))
        self.refresh_tree()
        self.status.config(text="Sorted by Phone No.")

# Run App
if __name__ == "__main__":
    win = tk.Tk()
    app = SmartContactManager(win)
    win.mainloop()
