import mysql.connector
import csv

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="student_db"
    )

def fetch_students_from_db():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_student_to_db(name, age, grade):
    conn = connect_to_database()
    cursor = conn.cursor()
    query = "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, age, grade))
    conn.commit()
    conn.close()

def delete_student_from_db(student_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    query = "DELETE FROM students WHERE id = %s"
    cursor.execute(query, (student_id,))
    conn.commit()
    conn.close()

def search_students_in_db(keyword):
    conn = connect_to_database()
    cursor = conn.cursor()
    query = "SELECT * FROM students WHERE name LIKE %s OR id = %s"
    cursor.execute(query, (f"%{keyword}%", keyword))
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_student_in_db(student_id, name, age, grade):
    conn = connect_to_database()
    cursor = conn.cursor()
    query = "UPDATE students SET name = %s, age = %s, grade = %s WHERE id = %s"
    cursor.execute(query, (name, age, grade, student_id))
    conn.commit()
    conn.close()

def fetch_students_with_pagination(page, page_size):
    conn = connect_to_database()
    cursor = conn.cursor()
    offset = (page - 1) * page_size
    query = "SELECT * FROM students LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_statistics():
    conn = connect_to_database()
    cursor = conn.cursor()
    query = """
        SELECT COUNT(*) as total_students, AVG(age) as average_age, grade, COUNT(*) as grade_count
        FROM students
        GROUP BY grade
    """
    cursor.execute(query)
    stats = cursor.fetchall()
    conn.close()
    return stats

def export_to_csv(filename):
    students = fetch_students_from_db()
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Age", "Grade"])
        writer.writerows(students)
