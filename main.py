import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("students_advanced.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            roll TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            course TEXT NOT NULL,
            marks REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- APP CLASS ---
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management & Analytics System")
        self.root.geometry("750x500")
        
        # Variables
        self.roll_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.course_var = tk.StringVar()
        self.marks_var = tk.StringVar()
        
        # Title
        title = tk.Label(self.root, text="Student Management System", font=("Arial", 18, "bold"), bg="#1e293b", fg="white")
        title.pack(fill=tk.X)
        
        # Form Frame
        form_frame = tk.Frame(self.root, padx=20, pady=20)
        form_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(form_frame, text="Roll No:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.roll_var, font=("Arial", 10)).grid(row=0, column=1, pady=5)
        
        tk.Label(form_frame, text="Name:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.name_var, font=("Arial", 10)).grid(row=1, column=1, pady=5)
        
        tk.Label(form_frame, text="Course:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.course_var, font=("Arial", 10)).grid(row=2, column=1, pady=5)
        
        tk.Label(form_frame, text="Marks (%):", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.marks_var, font=("Arial", 10)).grid(row=3, column=1, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=4, columnspan=2, pady=15)
        
        tk.Button(btn_frame, text="Add / Update", command=self.save_student, bg="#16a34a", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_student, bg="#dc2626", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        
        # Table Frame
        table_frame = tk.Frame(self.root, padx=10, pady=20)
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(table_frame, columns=("Roll", "Name", "Course", "Marks"), show="headings")
        self.tree.heading("Roll", text="Roll No")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Course", text="Course")
        self.tree.heading("Marks", text="Marks (%)")
        
        self.tree.column("Roll", width=70)
        self.tree.column("Name", width=120)
        self.tree.column("Course", width=100)
        self.tree.column("Marks", width=70)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<ButtonRelease-1>", self.get_cursor)
        
        self.fetch_data()

    def save_student(self):
        if not self.roll_var.get() or not self.name_var.get():
            messagebox.showerror("Error", "Roll No and Name are required!")
            return
            
        conn = sqlite3.connect("students_advanced.db")
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO students VALUES (?, ?, ?, ?)", (
            self.roll_var.get(), self.name_var.get(), self.course_var.get(), self.marks_var.get()
        ))
        conn.commit()
        conn.close()
        self.fetch_data()
        self.clear_fields()
        messagebox.showinfo("Success", "Record saved successfully!")

    def fetch_data(self):
        conn = sqlite3.connect("students_advanced.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=row)
        conn.close()

    def clear_fields(self):
        self.roll_var.set("")
        self.name_var.set("")
        self.course_var.set("")
        self.marks_var.set("")

    def get_cursor(self, ev):
        cursor_row = self.tree.focus()
        content = self.tree.item(cursor_row)
        row = content["values"]
        if row:
            self.roll_var.set(row[0])
            self.name_var.set(row[1])
            self.course_var.set(row[2])
            self.marks_var.set(row[3])

    def delete_student(self):
        if not self.roll_var.get():
            messagebox.showerror("Error", "Select a student to delete!")
            return
        conn = sqlite3.connect("students_advanced.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE roll=?", (self.roll_var.get(),))
        conn.commit()
        conn.close()
        self.fetch_data()
        self.clear_fields()
        messagebox.showinfo("Success", "Record deleted!")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()