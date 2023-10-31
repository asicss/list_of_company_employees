import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3

class EmployeeManagementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Список сотрудников компании")

        self.conn = sqlite3.connect('employees.db')
        self.create_table()

        self.tree = ttk.Treeview(master)
        self.tree["columns"] = ("ID", "Name", "Phone", "Email", "Salary")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="ФИО")
        self.tree.heading("Phone", text="Телефон")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Salary", text="Зарплата")
        self.tree.pack(padx=20, pady=20)

        self.create_widgets()
        self.update_treeview()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                email TEXT,
                salary INTEGER
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        self.add_button = tk.Button(self.master, text="добавить сотрудника", command=self.add_employee)
        self.add_button.pack(pady=10)
        self.update_button = tk.Button(self.master, text="изменить текущего сотрудника", command=self.update_employee)
        self.update_button.pack(pady=10)
        self.delete_button = tk.Button(self.master, text="удалить сотрудника", command=self.delete_employee)
        self.delete_button.pack(pady=10)
        self.search_button = tk.Button(self.master, text="искать по ФИО", command=self.search_employee)
        self.search_button.pack(pady=10)
        self.undo_button = tk.Button(self.master, text="отменить", command=self.undo_action)
        self.undo_button.pack(pady=10)

        # Bind double click event on treeview
        self.tree.bind("<Double-1>", self.on_double_click)

        self.last_action = None  # To store the last action for undo

    def add_employee(self):
        name = simpledialog.askstring("Ввести", "Введите имя сотрудника:")
        phone = simpledialog.askstring("Ввести", "Введите телефон сотрудника:")
        email = simpledialog.askstring("Ввести", "Введите email сотрудника:")
        salary = simpledialog.askinteger("Ввести", "Введите заработную плату сотрудника:")

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)", (name, phone, email, salary))
        self.conn.commit()
        self.update_treeview()
        self.last_action = "добавить"

    def update_employee(self):
        emp_id = simpledialog.askinteger("Ввод", "Введите ID сотрудника:")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id=?", (emp_id,))
        employee = cursor.fetchone()

        if employee:
            name = simpledialog.askstring("Ввод", "Введите обновлённое имя сотрудника:", initialvalue=employee[1])
            phone = simpledialog.askstring("Ввод", "Введите обновлённый номер телефона сотрудника:", initialvalue=employee[2])
            email = simpledialog.askstring("Ввод", "Введите обновлённый адрес электронной почты сотрудника:", initialvalue=employee[3])
            salary = simpledialog.askinteger("Ввод", "Введите обновлённую заработную плату сотрудника:", initialvalue=employee[4])

            cursor.execute("UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?", (name, phone, email, salary, emp_id))
            self.conn.commit()
            self.update_treeview()
            self.last_action = "изменить"
        else:
            messagebox.showerror("Ошибка", "Сотрудник не найден.")

    def delete_employee(self):
        emp_id = simpledialog.askinteger("Ввод", "Введите ID сотрудника:")

        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id=?", (emp_id,))
        self.conn.commit()
        self.update_treeview()
        self.last_action = "удалить"

    def search_employee(self):
        name = simpledialog.askstring("Ввод", "Введите имя сотрудника:")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE name=?", (name,))
        employees = cursor.fetchall()

        if employees:
            self.tree.delete(*self.tree.get_children())
            for employee in employees:
                self.tree.insert("", "end", values=employee)
        else:
            messagebox.showinfo("", "Сотрудника с таким именем нет.")

    def update_treeview(self):
        # Clear the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

        for employee in employees:
            self.tree.insert("", "end", values=employee)

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        employee_id = self.tree.item(item, "values")[0]  # Get the employee ID
        messagebox.showinfo("Employee ID", f"Employee ID: {employee_id}")

    def undo_action(self):
        if self.last_action == "добавить":
            messagebox.showinfo("Отменить", "Отменить добавление сотрудника.")
            # Implement code to undo the add action
        elif self.last_action == "изменить":
            messagebox.showinfo("Отменить", "Отменить изменение сотрудника.")
            # Implement code to undo the update action
        elif self.last_action == "удалить":
            messagebox.showinfo("Отменить", "Отменить удаление сотрудника.")
            # Implement code to undo the delete action
        else:
            messagebox.showinfo("Отменить", "Нельзя отменить преведущее действие.")

    def on_closing(self):
        self.conn.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()