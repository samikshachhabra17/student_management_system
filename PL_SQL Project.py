import psycopg2
from psycopg2 import sql
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Database connection setup
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="your_database_name",
            user="your_username",
            password="your_password",
            host="localhost",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        messagebox.showerror("Connection Error", str(e))
        return None

# Function to fetch all students
def fetch_students():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Students")
        rows = cur.fetchall()
        conn.close()
        return rows
    return []

# Function to add a new student
def add_student():
    student_name = entry_name.get()
    percentage = entry_percentage.get()
    fathers_name = entry_fathers_name.get()

    if not student_name or not percentage:
        messagebox.showwarning("Input Error", "Please provide the necessary details.")
        return

    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            insert_query = sql.SQL(
                "INSERT INTO Students (student_name, percentage, fathers_name) VALUES (%s, %s, %s)"
            )
            cur.execute(insert_query, (student_name, percentage, fathers_name))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student added successfully!")
            refresh_display()
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", str(e))

# Refresh display to show all students
def refresh_display():
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_students():
        tree.insert("", "end", values=row)

# Tkinter GUI setup
root = tk.Tk()
root.title("Student Management System")
root.geometry("500x400")
root.configure(bg="#EAECEE")  # Main background color

# Style configurations for ttk widgets
style = ttk.Style()
style.configure("Treeview", background="#E8F8F5", foreground="black", rowheight=25, fieldbackground="#E8F8F5")
style.map("Treeview", background=[("selected", "#A3E4D7")])

# Labels and Entries for Student Data
label_color = "#1ABC9C"  # Label color
entry_bg_color = "#E8F8F5"  # Entry background color
button_bg_color = "#1ABC9C"  # Button background color

tk.Label(root, text="Student Name", bg="#EAECEE", fg=label_color, font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=10)
entry_name = tk.Entry(root, bg=entry_bg_color)
entry_name.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Percentage", bg="#EAECEE", fg=label_color, font=("Arial", 10, "bold")).grid(row=1, column=0, padx=10, pady=10)
entry_percentage = tk.Entry(root, bg=entry_bg_color)
entry_percentage.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Father's Name", bg="#EAECEE", fg=label_color, font=("Arial", 10, "bold")).grid(row=2, column=0, padx=10, pady=10)
entry_fathers_name = tk.Entry(root, bg=entry_bg_color)
entry_fathers_name.grid(row=2, column=1, padx=10, pady=10)

# Button to Add Student
btn_add = tk.Button(root, text="Add Student", bg=button_bg_color, fg="white", font=("Arial", 10, "bold"), command=add_student)
btn_add.grid(row=3, column=0, columnspan=2, pady=10, ipadx=20)

# Treeview for displaying student data
columns = ("student_uid", "student_name", "percentage", "fathers_name")
tree = ttk.Treeview(root, columns=columns, show="headings", selectmode="browse")
tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

for col in columns:
    tree.heading(col, text=col, anchor="center")
    tree.column(col, anchor="center", width=100)

# Button to Refresh Display
btn_refresh = tk.Button(root, text="Refresh", bg=button_bg_color, fg="white", font=("Arial", 10, "bold"), command=refresh_display)
btn_refresh.grid(row=5, column=0, columnspan=2, pady=10, ipadx=20)

# Load initial data
refresh_display()

root.mainloop()
