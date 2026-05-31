import streamlit as st
import sqlite3
import pandas as pd

# ---------- DATABASE HELPERS ----------

DB_PATH = "employees.db"

def get_connection():
    # Create a new connection each time (simpler & safe for Streamlit reruns)
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL
        )
    """)
    conn.commit()
    conn.close()

def add_employee(name, department, salary):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)",
        (name, department, salary)
    )
    conn.commit()
    conn.close()

def get_employees(department_filter=None):
    conn = get_connection()
    cur = conn.cursor()
    if department_filter and department_filter != "All":
        cur.execute(
            "SELECT id, name, department, salary FROM employees WHERE department = ?",
            (department_filter,)
        )
    else:
        cur.execute("SELECT id, name, department, salary FROM employees")
    rows = cur.fetchall()
    conn.close()
    return rows

# ---------- STREAMLIT APP ----------

def main():
    st.title("Employee Management App (SQLite + Streamlit)")
    st.write("This app collects employee data and stores it in a SQLite database.")

    # Ensure table exists
    create_table()

    st.subheader("Add a new employee")

    # Form for data collection
    with st.form("employee_form"):
        name = st.text_input("Name")
        department = st.selectbox("Department", ["HR", "Engineering", "Marketing", "Finance"])
        salary = st.number_input("Salary", min_value=0.0, step=1000.0)
        submitted = st.form_submit_button("Save employee")

    if submitted:
        if name.strip() == "":
            st.error("Name cannot be empty.")
        else:
            add_employee(name, department, salary)
            st.success(f"Employee {name} added successfully!")

    st.subheader("Browse employees")

    # Department filter
    dept_filter = st.selectbox("Filter by department", ["All", "HR", "Engineering", "Marketing", "Finance"])

    rows = get_employees(dept_filter)

    if rows:
        df = pd.DataFrame(rows, columns=["ID", "Name", "Department", "Salary"])
        st.dataframe(df)
    else:
        st.info("No employees in the database yet.")

if __name__ == "__main__":
    main()
