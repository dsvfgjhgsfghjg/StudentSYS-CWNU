import tkinter as tk
from tkinter import messagebox, filedialog
from database import (fetch_students_from_db, add_student_to_db, delete_student_from_db,
                      search_students_in_db, update_student_in_db, fetch_students_with_pagination,
                      get_statistics, export_to_csv)

current_page = 1
page_size = 5

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
    global current_page, page_size
    try:
        rows = fetch_students_with_pagination(current_page, page_size)
        student_list.delete(0, tk.END)
        for row in rows:
            student_list.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Grade: {row[3]}")
    except Exception as err:
        messagebox.showerror("Error", str(err))

def search_students():
    keyword = entry_search.get()
    if not keyword:
        messagebox.showerror("Error", "Please enter a keyword to search")
        return

    try:
        rows = search_students_in_db(keyword)
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

def update_student():
    selected = student_list.curselection()
    if not selected:
        messagebox.showerror("Error", "Please select a student to update")
        return

    student = student_list.get(selected[0])
    student_id = int(student.split(",")[0].split(":")[1].strip())

    def save_update():
        name = update_name.get()
        age = update_age.get()
        grade = update_grade.get()

        if not name or not age or not grade:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            update_student_in_db(student_id, name, age, grade)
            messagebox.showinfo("Success", "Student updated successfully")
            update_window.destroy()
            fetch_students()
        except Exception as err:
            messagebox.showerror("Error", str(err))

    update_window = tk.Toplevel(root)
    update_window.title("Update Student")

    tk.Label(update_window, text="Name:").grid(row=0, column=0, padx=5, pady=5)
    update_name = tk.Entry(update_window)
    update_name.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(update_window, text="Age:").grid(row=1, column=0, padx=5, pady=5)
    update_age = tk.Entry(update_window)
    update_age.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(update_window, text="Grade:").grid(row=2, column=0, padx=5, pady=5)
    update_grade = tk.Entry(update_window)
    update_grade.grid(row=2, column=1, padx=5, pady=5)

    tk.Button(update_window, text="Save", command=save_update).grid(row=3, column=0, columnspan=2, pady=10)

def next_page():
    global current_page
    current_page += 1
    fetch_students()

def prev_page():
    global current_page
    if current_page > 1:
        current_page -= 1
        fetch_students()

def show_statistics():
    try:
        stats = get_statistics()
        stat_window = tk.Toplevel(root)
        stat_window.title("Statistics")

        for stat in stats:
            tk.Label(stat_window, text=f"Grade: {stat[2]}, Count: {stat[3]}").pack()
        tk.Label(stat_window, text=f"Total Students: {stats[0][0]}").pack()
        tk.Label(stat_window, text=f"Average Age: {stats[0][1]:.2f}").pack()
    except Exception as err:
        messagebox.showerror("Error", str(err))

def export_data():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    try:
        export_to_csv(file_path)
        messagebox.showinfo("Success", "Data exported successfully")
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

search_frame = tk.Frame(root)
search_frame.pack(pady=10)

tk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5, pady=5)
entry_search = tk.Entry(search_frame)
entry_search.grid(row=0, column=1, padx=5, pady=5)

search_button = tk.Button(search_frame, text="Search", command=search_students)
search_button.grid(row=0, column=2, padx=5, pady=5)

navigation_frame = tk.Frame(root)
navigation_frame.pack(pady=10)

prev_button = tk.Button(navigation_frame, text="Previous Page", command=prev_page)
prev_button.grid(row=0, column=0, padx=5, pady=5)

next_button = tk.Button(navigation_frame, text="Next Page", command=next_page)
next_button.grid(row=0, column=1, padx=5, pady=5)

student_list = tk.Listbox(root, width=50, height=10)
student_list.pack(pady=10)

update_button = tk.Button(root, text="Update Student", command=update_student)
update_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Student", command=delete_student)
delete_button.pack(pady=5)

stat_button = tk.Button(root, text="Show Statistics", command=show_statistics)
stat_button.pack(pady=5)

export_button = tk.Button(root, text="Export to CSV", command=export_data)
export_button.pack(pady=5)

fetch_students()  # Load students on startup

root.mainloop()
