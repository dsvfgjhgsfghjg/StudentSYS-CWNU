import tkinter as tk
from tkinter import messagebox
from database import fetch_students_from_db, add_student_to_db, delete_student_from_db

def add_student():
    name = entry_name.get()
    age = entry_age.get()
    grade = entry_grade.get()

    if not name or not age or not grade:
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        add_student_to_db(name, age, grade)
        messagebox.showinfo("Success", "Student added successfully")
        entry_name.delete(0, tk.END)
        entry_age.delete(0, tk.END)
        entry_grade.delete(0, tk.END)
        fetch_students()
    except Exception as err:
        messagebox.showerror("Error", str(err))

def fetch_students():
    try:
        rows = fetch_students_from_db()
        student_list.delete(0, tk.END)
        for row in rows:
            student_list.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Grade: {row[3]}")
    except Exception as err:
        messagebox.showerror("Error", str(err))

def delete_student():
    selected = student_list.curselection()
    if not selected:
        messagebox.showerror("Error", "Please select a student to delete")
        return

    student = student_list.get(selected[0])
    student_id = int(student.split(",")[0].split(":")[1].strip())

    try:
        delete_student_from_db(student_id)
        messagebox.showinfo("Success", "Student deleted successfully")
        fetch_students()
    except Exception as err:
        messagebox.showerror("Error", str(err))

# Initialize the Tkinter application
root = tk.Tk()
root.title("Student Management System")

# GUI Components
frame = tk.Frame(root)
frame.pack(pady=20)

tk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Age:").grid(row=1, column=0, padx=5, pady=5)
entry_age = tk.Entry(frame)
entry_age.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Grade:").grid(row=2, column=0, padx=5, pady=5)
entry_grade = tk.Entry(frame)
entry_grade.grid(row=2, column=1, padx=5, pady=5)

add_button = tk.Button(frame, text="Add Student", command=add_student)
add_button.grid(row=3, column=0, columnspan=2, pady=10)

student_list = tk.Listbox(root, width=50, height=10)
student_list.pack(pady=10)

delete_button = tk.Button(root, text="Delete Student", command=delete_student)
delete_button.pack(pady=5)

fetch_students()  # Load students on startup

root.mainloop()