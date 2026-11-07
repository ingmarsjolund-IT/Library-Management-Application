import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


# Import application layer
from application.manage_book import ManageBook
from application.manage_member import ManageMember
from domain.models import ViewBook, ViewMember
from interface.graph_viewer import (
    show_books_by_genre_popup,
    show_members_by_type_popup,
)

print("Starting LBMMSApp...")

class LBMMSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Book & Member Management System")
        self.geometry("1000x600")
        self._create_widgets()

    def _create_widgets(self):
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=8, pady=8)

        # ----------------- Home Tab -----------------
        home_tab = ttk.Frame(self.nb)
        self.nb.add(home_tab, text="Home")

        h_frame = ttk.Frame(home_tab)
        h_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(h_frame, text="Library Overview", font=("Segoe UI", 16, "bold")).pack(pady=10)

        stats_frame = ttk.Frame(h_frame)
        stats_frame.pack(pady=10)

        self.var_books_available = tk.StringVar(value="0")
        self.var_books_rented = tk.StringVar(value="0")

        ttk.Label(stats_frame, text="Books Available:", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(stats_frame, textvariable=self.var_books_available, font=("Segoe UI", 12, "bold")).grid(row=0, column=1, sticky="w", padx=10, pady=5)

        ttk.Label(stats_frame, text="Books Checked Out:", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(stats_frame, textvariable=self.var_books_rented, font=("Segoe UI", 12, "bold")).grid(row=1, column=1, sticky="w", padx=10, pady=5)

        ttk.Button(h_frame, text="Refresh Overview", command=self.load_overview).pack(pady=15)

        # ----------------- Books Tab -----------------
        books_tab = ttk.Frame(self.nb)
        self.nb.add(books_tab, text="Books")

        b_top = ttk.Frame(books_tab)
        b_top.pack(fill="x", padx=8, pady=6)

        ttk.Label(b_top, text="Search: ").pack(side="left")
        self.b_search_var = tk.StringVar()
        ttk.Entry(b_top, textvariable=self.b_search_var, width=30).pack(side="left", padx=4)
        ttk.Label(b_top, text="Filter (Availability):").pack(side="left", padx=(10, 0))
        self.b_filter_var = tk.StringVar()
        ttk.Combobox(b_top, textvariable=self.b_filter_var, values=["", "Available", "Checked Out"], width=14).pack(side="left", padx=4)
        ttk.Button(b_top, text="Search/Filter", command=self.search_books).pack(side="left", padx=6)
        ttk.Button(b_top, text="Refresh", command=self.load_books).pack(side="left")

        # Form
        self.var_booktitle = tk.StringVar()
        self.var_bookauthor = tk.StringVar()
        self.var_bookisbn = tk.StringVar()
        self.var_bookgenre = tk.StringVar()
        self.var_bookavailability = tk.StringVar()

        b_form = ttk.Frame(books_tab)
        b_form.pack(fill="x", padx=8, pady=6)

        ttk.Label(b_form, text="Title:").pack(side="left")
        ttk.Entry(b_form, textvariable=self.var_booktitle, width=22).pack(side="left", padx=4)

        ttk.Label(b_form, text="Author:").pack(side="left")
        ttk.Entry(b_form, textvariable=self.var_bookauthor, width=16).pack(side="left", padx=4)

        ttk.Label(b_form, text="ISBN:").pack(side="left")
        ttk.Entry(b_form, textvariable=self.var_bookisbn, width=12).pack(side="left", padx=4)

        ttk.Label(b_form, text="Genre:").pack(side="left")
        ttk.Entry(b_form, textvariable=self.var_bookgenre, width=12).pack(side="left", padx=4)

        ttk.Label(b_form, text="Availability:").pack(side="left")
        ttk.Combobox(b_form, textvariable=self.var_bookavailability, values=["Available", "Checked Out"], width=12).pack(side="left", padx=4)

        b_buttons = ttk.Frame(books_tab)
        b_buttons.pack(fill="x", padx=8, pady=6)
        ttk.Button(b_buttons, text="Add Book", command=self.add_book).pack(side="left", padx=6)
        ttk.Button(b_buttons, text="Update Book", command=self.update_book).pack(side="left", padx=6)
        ttk.Button(b_buttons, text="Delete Book", command=self.delete_book).pack(side="left", padx=6)
        ttk.Button(b_buttons, text="Clear Form", command=self.clear_book_form).pack(side="left", padx=6)
        ttk.Button(b_buttons, text="View Genre Graph", command=self.show_genre_graph).pack(side="left", padx=6)

        self.b_tree = ttk.Treeview(books_tab, columns=("Title", "Author", "ISBN", "Genre", "Availability"), show="headings")
        for col in ("Title", "Author", "ISBN", "Genre", "Availability"):
            self.b_tree.heading(col, text=col)
            self.b_tree.column(col, width=150, anchor="w")
        self.b_tree.pack(fill="both", expand=True, padx=8, pady=6)
        self.b_tree.bind("<<TreeviewSelect>>", self.on_book_select)

        # ----------------- Members Tab -----------------
        members_tab = ttk.Frame(self.nb)
        self.nb.add(members_tab, text="Members")

        m_top = ttk.Frame(members_tab)
        m_top.pack(fill="x", padx=8, pady=6)

        ttk.Label(m_top, text="Search: ").pack(side="left")
        self.m_search_var = tk.StringVar()
        ttk.Entry(m_top, textvariable=self.m_search_var, width=30).pack(side="left", padx=4)
        ttk.Label(m_top, text="Filter (Type):").pack(side="left", padx=(10, 0))
        self.m_filter_var = tk.StringVar()
        ttk.Combobox(m_top, textvariable=self.m_filter_var, values=["", "Student", "Staff", "Guest"], width=14).pack(side="left", padx=4)
        ttk.Button(m_top, text="Search/Filter", command=self.search_members).pack(side="left", padx=6)
        ttk.Button(m_top, text="Refresh", command=self.load_members).pack(side="left")

        self.var_membername = tk.StringVar()
        self.var_memberid = tk.StringVar()
        self.var_membercontact = tk.StringVar()
        self.var_membertype = tk.StringVar()

        m_form = ttk.Frame(members_tab)
        m_form.pack(fill="x", padx=8, pady=6)

        ttk.Label(m_form, text="Name:").pack(side="left")
        ttk.Entry(m_form, textvariable=self.var_membername, width=24).pack(side="left", padx=4)

        ttk.Label(m_form, text="ID:").pack(side="left")
        ttk.Entry(m_form, textvariable=self.var_memberid, width=8).pack(side="left", padx=4)

        ttk.Label(m_form, text="Contact:").pack(side="left")
        ttk.Entry(m_form, textvariable=self.var_membercontact, width=20).pack(side="left", padx=4)

        ttk.Label(m_form, text="Type:").pack(side="left")
        ttk.Combobox(m_form, textvariable=self.var_membertype, values=["Student", "Staff", "Guest"], width=12).pack(side="left", padx=4)

        m_buttons = ttk.Frame(members_tab)
        m_buttons.pack(fill="x", padx=8, pady=6)
        ttk.Button(m_buttons, text="Add Member", command=self.add_member).pack(side="left", padx=6)
        ttk.Button(m_buttons, text="Update Member", command=self.update_member).pack(side="left", padx=6)
        ttk.Button(m_buttons, text="Delete Member", command=self.delete_member).pack(side="left", padx=6)
        ttk.Button(m_buttons, text="Clear Form", command=self.clear_member_form).pack(side="left", padx=6)
        ttk.Button(m_buttons, text="View Member Types Graph", command=self.show_member_types_graph).pack(side="left", padx=6)

        self.m_tree = ttk.Treeview(members_tab, columns=("ID", "Name", "Contact", "Type"), show="headings")
        for col in ("ID", "Name", "Contact", "Type"):
            self.m_tree.heading(col, text=col)
            self.m_tree.column(col, width=180, anchor="w")
        self.m_tree.pack(fill="both", expand=True, padx=8, pady=6)
        self.m_tree.bind("<<TreeviewSelect>>", self.on_member_select)

        # ----------------- Logs Tab -----------------
        logs_tab = ttk.Frame(self.nb)
        self.nb.add(logs_tab, text="Logs")

        self.log_tree = ttk.Treeview(logs_tab, columns=("Entity", "Action", "Details", "Timestamp"), show="headings")
        for col in ("Entity", "Action", "Details", "Timestamp"):
            self.log_tree.heading(col, text=col)
            self.log_tree.column(col, width=200, anchor="w")
        self.log_tree.pack(fill="both", expand=True, padx=8, pady=8)

        ttk.Button(logs_tab, text="Refresh Logs", command=self.load_logs).pack(pady=5)

        # ----------------- Load initial data -----------------
        self.load_books()
        self.load_members()
        self.load_overview()
        self.load_logs()

    # ----------------- Book operations -----------------
    def load_books(self):
        try:
            books = ManageBook.GetAllBooks()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load books: {e}")
            return
        self.b_tree.delete(*self.b_tree.get_children())
        for b in books:
            self.b_tree.insert("", "end", values=(b.title, b.author, b.isbn, b.genre, b.availability))

    def add_book(self):
        vb = ViewBook(
            title=self.var_booktitle.get(),
            author=self.var_bookauthor.get(),
            isbn=self.var_bookisbn.get(),
            genre=self.var_bookgenre.get(),
            availability=self.var_bookavailability.get(),
        )
        errs = ManageBook.CreateBook(vb)
        if errs:
            messagebox.showerror("Validation", "\n".join(errs))
        else:
            messagebox.showinfo("Success", "Book added successfully.")
            self.clear_book_form()
            self.load_books()
            self.load_overview()
            self.write_log("Book", "Add", f"{vb.title} by {vb.author}, ISBN {vb.isbn}")
            self.load_logs()

    def update_book(self):
        vb = ViewBook(
            title=self.var_booktitle.get(),
            author=self.var_bookauthor.get(),
            isbn=self.var_bookisbn.get(),
            genre=self.var_bookgenre.get(),
            availability=self.var_bookavailability.get(),
        )
        errs = ManageBook.UpdateBook(vb)
        if errs:
            messagebox.showerror("Validation", "\n".join(errs))
        else:
            messagebox.showinfo("Success", "Book updated successfully.")
            self.clear_book_form()
            self.load_books()
            self.load_overview()
            self.write_log("Book", "Update", f"{vb.title} by {vb.author}, ISBN {vb.isbn}")
            self.load_logs()

    def delete_book(self):
        isbn = self.var_bookisbn.get()
        if not isbn.strip():
            messagebox.showerror("Validation", "ISBN is required to delete a book.")
            return
        vb = ViewBook(isbn=isbn)
        errs = ManageBook.DeleteBook(vb)
        if errs:
            messagebox.showerror("Error", "\n".join(errs))
        else:
            messagebox.showinfo("Success", "Book deleted.")
            self.clear_book_form()
            self.load_books()
            self.load_overview()
            self.write_log("Book", "Delete", f"ISBN {vb.isbn}")
            self.load_logs()

    def on_book_select(self, _evt: Optional[tk.Event] = None):
        sel = self.b_tree.selection()
        if not sel:
            return
        vals = self.b_tree.item(sel[0], "values")
        self.var_booktitle.set(vals[0])
        self.var_bookauthor.set(vals[1])
        self.var_bookisbn.set(vals[2])
        self.var_bookgenre.set(vals[3])
        self.var_bookavailability.set(vals[4])

    def clear_book_form(self):
        self.var_booktitle.set("")
        self.var_bookauthor.set("")
        self.var_bookisbn.set("")
        self.var_bookgenre.set("")
        self.var_bookavailability.set("")

    def search_books(self):
        query = self.b_search_var.get().strip().lower()
        filt = self.b_filter_var.get().strip()
        try:
            books = ManageBook.GetAllBooks()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load books: {e}")
            return
        results = []
        for b in books:
            if filt and b.availability != filt:
                continue
            if not query or (query in b.title.lower() or query in b.author.lower() or query in b.genre.lower() or query in b.isbn.lower()):
                results.append(b)
        self.b_tree.delete(*self.b_tree.get_children())
        for b in results:
            self.b_tree.insert("", "end", values=(b.title, b.author, b.isbn, b.genre, b.availability))

    def show_genre_graph(self):
        try:
            books = ManageBook.GetAllBooks()
            if not books:
                messagebox.showinfo("Info", "No books found to plot.")
                return
            show_books_by_genre_popup(self, books)
        except Exception as e:
            messagebox.showerror("Error", f"Unable to display graph: {e}")

    # ----------------- Member operations -----------------
    def load_members(self):
        try:
            members = ManageMember.GetAllMembers()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load members: {e}")
            return
        self.m_tree.delete(*self.m_tree.get_children())
        for m in members:
            self.m_tree.insert("", "end", values=(m.id, m.name, m.contact, m.type))

    def add_member(self):
        vm = ViewMember(
            name=self.var_membername.get(),
            id=self.var_memberid.get(),
            contact=self.var_membercontact.get(),
            type=self.var_membertype.get(),
        )
        errs = ManageMember.CreateMember(vm)
        if errs:
            messagebox.showerror("Validation", "\n".join(errs))
        else:
            messagebox.showinfo("Success", "Member added successfully.")
            self.clear_member_form()
            self.load_members()
            self.write_log("Member", "Add", f"{vm.name}, ID {vm.id}")
            self.load_logs()

    def update_member(self):
        vm = ViewMember(
            name=self.var_membername.get(),
            id=self.var_memberid.get(),
            contact=self.var_membercontact.get(),
            type=self.var_membertype.get(),
        )
        errs = ManageMember.UpdateMember(vm)
        if errs:
            messagebox.showerror("Validation", "\n".join(errs))
        else:
            messagebox.showinfo("Success", "Member updated successfully.")
            self.clear_member_form()
            self.load_members()
            self.write_log("Member", "Update", f"{vm.name}, ID {vm.id}")
            self.load_logs()

    def delete_member(self):
        mid = self.var_memberid.get()
        if not mid.strip():
            messagebox.showerror("Validation", "Member ID is required to delete.")
            return
        vm = ViewMember(id=mid)
        errs = ManageMember.DeleteMember(vm)
        if errs:
            messagebox.showerror("Error", "\n".join(errs))
        else:
            messagebox.showinfo("Success", "Member deleted.")
            self.clear_member_form()
            self.load_members()
            self.write_log("Member", "Delete", f"ID {vm.id}")
            self.load_logs()

    def on_member_select(self, _evt: Optional[tk.Event] = None):
        sel = self.m_tree.selection()
        if not sel:
            return
        vals = self.m_tree.item(sel[0], "values")
        self.var_memberid.set(vals[0])
        self.var_membername.set(vals[1])
        self.var_membercontact.set(vals[2])
        self.var_membertype.set(vals[3])

    def clear_member_form(self):
        self.var_membername.set("")
        self.var_memberid.set("")
        self.var_membercontact.set("")
        self.var_membertype.set("")

    def search_members(self):
        query = self.m_search_var.get().strip().lower()
        filt = self.m_filter_var.get().strip()
        try:
            members = ManageMember.GetAllMembers()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load members: {e}")
            return
        results = []
        for m in members:
            if filt and m.type != filt:
                continue
            if not query or (query in m.name.lower() or query in m.contact.lower() or query in m.id.lower()):
                results.append(m)
        self.m_tree.delete(*self.m_tree.get_children())
        for m in results:
            self.m_tree.insert("", "end", values=(m.id, m.name, m.contact, m.type))

    def show_member_types_graph(self):
        try:
            members = ManageMember.GetAllMembers()
            if not members:
                messagebox.showinfo("Info", "No members found to plot.")
                return
            show_members_by_type_popup(self, members)
        except Exception as e:
            messagebox.showerror("Error", f"Unable to display graph: {e}")

    # ----------------- Home tab -----------------
    def load_overview(self):
        try:
            books = ManageBook.GetAllBooks()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load overview: {e}")
            return
        available = sum(1 for b in books if b.availability.lower() == "available")
        rented = sum(1 for b in books if b.availability.lower() == "checked out")
        self.var_books_available.set(str(available))
        self.var_books_rented.set(str(rented))

    # ----------------- Logs -----------------
    def write_log(self, entity: str, action: str, details: str):
        from infrastructure.db.database import get_connection
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                log_id INTEGER PRIMARY KEY,
                entity TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                timestamp TEXT NOT NULL
            )
        ''')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("INSERT INTO logs (entity, action, details, timestamp) VALUES (?, ?, ?, ?)",
                    (entity, action, details, timestamp))
        conn.commit()
        cur.close()

    def load_logs(self):
        from infrastructure.db.database import get_connection
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT entity, action, details, timestamp FROM logs ORDER BY log_id DESC")
        rows = cur.fetchall()
        self.log_tree.delete(*self.log_tree.get_children())
        for r in rows:
            self.log_tree.insert("", "end", values=(r["entity"], r["action"], r["details"], r["timestamp"]))
        cur.close()

if __name__ == "__main__":
    app = LBMMSApp()
    app.mainloop()
