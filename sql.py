import sqlite3

# ----------------------------
# STEP 1: Connect to SQLite
# ----------------------------
connection = sqlite3.connect("employees.db")
cursor = connection.cursor()

# ----------------------------
# STEP 2: Create Employees Table
# ----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    department TEXT,
    position TEXT,
    salary REAL,
    join_date TEXT
);
""")

# ----------------------------
# STEP 3: Insert Dummy Employee Data
# ----------------------------
employees_data = [
    ("John Doe", "john.doe@example.com", "Engineering", "Software Engineer", 85000, "2022-03-15"),
    ("Alice Smith", "alice.smith@example.com", "Marketing", "Marketing Manager", 72000, "2021-07-01"),
    ("Robert Brown", "robert.brown@example.com", "HR", "HR Executive", 60000, "2020-11-20"),
    ("Emma Johnson", "emma.johnson@example.com", "Engineering", "Data Scientist", 95000, "2023-01-10"),
    ("Michael Lee", "michael.lee@example.com", "Finance", "Financial Analyst", 68000, "2019-09-05"),
    ("Sophia Davis", "sophia.davis@example.com", "Sales", "Sales Associate", 55000, "2022-06-12"),
    ("Daniel Wilson", "daniel.wilson@example.com", "Engineering", "DevOps Engineer", 88000, "2021-02-25"),
    ("Olivia Miller", "olivia.miller@example.com", "Support", "Customer Support Specialist", 50000, "2020-04-18")
]

cursor.executemany("""
INSERT INTO employees (name, email, department, position, salary, join_date)
VALUES (?, ?, ?, ?, ?, ?)
""", employees_data)


print("Employees database created successfully with dummy data!")
print("The inserted records are: ")

data = cursor.execute('''Select * From employees''')
for row in data:
    print(row)


# STEP 4: Commit and Close
# ----------------------------
connection.commit()
connection.close()

# ----------------------------
