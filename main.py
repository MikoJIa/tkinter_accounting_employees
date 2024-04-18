import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect('accounting.db')
cur = conn.cursor()

cur.execute(
    """CREATE TABLE IF NOT EXISTS employees(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    fio TEXT,
    place_of_work TEXT,
    job_title TEXT,
    salary_advance TEXT,
    salary TEXT,
    stay_salary TEXT,
    vacation_pay TEXT,
    comment TEXT
    )
""")
conn.commit()


def add_in_table():
    list_get = [ent_date.get(), ent_fio.get()]
    reply = messagebox.askyesno('Успех', 'Действительно добавить?')
    if all(list_get):
        if reply == True:
            date = ent_date.get()
            fio = ent_fio.get()
            place_of_work = ent_place_of_work.get()
            job_title = ent_job_title.get()
            salary_advance = ent_salary_advance.get()
            salary = ent_salary.get()
            stay_salary = ent_stay_salary.get()
            vacation_pay = ent_vacation_pay.get()
            comment = ent_commit.get()
            cur.execute(
                """INSERT INTO employees (date, fio,
                                          place_of_work, 
                                          job_title, salary_advance, salary, 
                                          stay_salary, vacation_pay, 
                                          comment)
                                          VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                                          """,
                (date, fio, place_of_work, job_title, salary_advance, salary, stay_salary, vacation_pay, comment)
            )
            conn.commit()
            add_id = cur.lastrowid
            tree.insert('', tk.END, values=(add_id, date, fio,
                                            place_of_work,
                                            job_title, salary_advance, salary,
                                            stay_salary, vacation_pay, comment))
            ent_date.delete(0, tk.END)
            ent_fio.delete(0, tk.END)
            ent_place_of_work.delete(0, tk.END)
            ent_job_title.delete(0, tk.END)
            ent_salary_advance.delete(0, tk.END)
            ent_salary.delete(0, tk.END)
            ent_stay_salary.delete(0, tk.END)
            ent_vacation_pay.delete(0, tk.END)
            ent_commit.delete(0, tk.END)
            messagebox.showinfo('Успех', 'Новая информация добавлена')
        else:
            messagebox.showinfo('Error', 'В другой раз!!!')
    else:
        messagebox.showinfo('Внимание!!!', 'Необходимо заполнить все обязательные поля\n'
                                                        'ФИО\n'
                            )


def sort_data(number_col, reverse):
    lst = [(tree.set(i, number_col), i) for i in tree.get_children('')]
    lst.sort(reverse=reverse)
    for index, (_, item) in enumerate(lst):
        tree.move(item, '', index)

    tree.heading(number_col, command=lambda: sort_data(number_col, not reverse))


def button_delete():
    # Сначало в переменную item_row мы сохраним выбранную строку
    item_row = tree.selection()
    # далее если строка выбранна, то мы её удаляем
    if item_row:
        item_row_values = tree.item(item_row, 'values')
        tran_id = item_row_values[0]
        cur.execute(
            """DELETE FROM employees WHERE id=?""", (tran_id,)
        )
        conn.commit()
        tree.delete(item_row)
        messagebox.showinfo('Успех', 'Информация успешна удалена')
    else:
        messagebox.showinfo('Внимание', 'Выберите желаемую строку!!!')


def deffault_row_info(event):
    if tree.selection():
        item = tree.selection()[0]
        values = tree.item(item, 'values')
        ent_date.delete(0, tk.END)
        ent_date.insert(0, values[1])
        ent_fio.delete(0, tk.END)
        ent_fio.insert(0, values[2])
        ent_place_of_work.delete(0, tk.END)
        ent_place_of_work.insert(0, values[3])
        ent_job_title.delete(0, tk.END)
        ent_job_title.insert(0, values[4])
        ent_salary_advance.delete(0, tk.END)
        ent_salary_advance.insert(0, values[5])
        ent_salary.delete(0, tk.END)
        ent_salary.insert(0, values[6])
        ent_stay_salary.delete(0, tk.END)
        ent_stay_salary.insert(0, values[7])
        ent_vacation_pay.delete(0, tk.END)
        ent_vacation_pay.insert(0, values[8])
        ent_commit.delete(0, tk.END)
        ent_commit.insert(0, values[9])


def update_data():
    item_row = tree.selection()
    if not item_row:
        messagebox.showerror('Строка изменения не выброна', 'Выберите строку для изменения')
        return
    tran_id = tree.set(item_row, '#1')
    date = ent_date.get()
    fio = ent_fio.get()
    place_of_work = ent_place_of_work.get()
    job_title = ent_job_title.get()
    salary_advance = ent_salary_advance.get()
    salary = ent_salary.get()
    stay_salary = ent_stay_salary.get()
    vacation_pay = ent_vacation_pay.get()
    comment = ent_commit.get()
    cur.execute(
        """UPDATE employees SET date=?, fio=?, 
                                 place_of_work=?, job_title=?, salary_advance=?, salary=?,
                                  stay_salary=?, vacation_pay=?, comment=?
                                  WHERE id=?""",
                    (date, fio,
                                place_of_work,
                                job_title, salary_advance, salary,
                                stay_salary, vacation_pay, comment, tran_id)
    )
    conn.commit()
    tree.item(item_row, values=(tran_id, date, fio, place_of_work, job_title, salary_advance, salary,
                                stay_salary, vacation_pay, comment))


def clear_rows():
    ent_date.delete(0, tk.END)
    ent_fio.delete(0, tk.END)
    ent_place_of_work.delete(0, tk.END)
    ent_job_title.delete(0, tk.END)
    ent_salary_advance.delete(0, tk.END)
    ent_salary.delete(0, tk.END)
    ent_stay_salary.delete(0, tk.END)
    ent_vacation_pay.delete(0, tk.END)
    ent_commit.delete(0, tk.END)


def search_data():
    keyword = ent_search.get()
    cur.execute(
        """SELECT * FROM employees WHERE fio LIKE ?
         OR place_of_work LIKE ?
         OR job_title LIKE ?
        """, ('%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%')
    )
    result = cur.fetchall()
    # conn.close()
    [tree.delete(i) for i in tree.get_children()]

    for row in result:
        tree.insert('', tk.END, values=row)


def return_to_main_page():
    [tree.delete(i) for i in tree.get_children()]
    cur.execute(
        """SELECT * FROM employees ORDER BY date"""
    )
    rows = cur.fetchall()

    for row in rows:
        tree.insert('', tk.END, values=row)


window = tk.Tk()
window.title('Учёт сотрудников')
window.geometry('1500x900')

left_frame = tk.Frame(window, relief=tk.SUNKEN, borderwidth=5, bg='silver')
left_frame.pack(side=tk.LEFT, fill=tk.Y)

lbl_date = tk.Label(left_frame, text='Дата', font=('Arial', 15), bg='silver')
lbl_date.grid(row=0, column=0, sticky='e')
ent_date = DateEntry(left_frame, width=25, font='Arial 14', relief=tk.SUNKEN, borderwidth=3, date_pattern='dd.mm.yy')
ent_date.grid(row=0, column=1)

lbl_fio = tk.Label(left_frame, text='ФИО', font=('Arial', 15), bg='silver')
lbl_fio.grid(row=1, column=0, sticky='e')
ent_fio = tk.Entry(left_frame, width=25, font='Arial 15', relief=tk.SUNKEN, borderwidth=3)
ent_fio.grid(row=1, column=1)


# lbl_last_name = tk.Label(left_frame, text='Фамилия', font=('Arial', 15), bg='silver')
# lbl_last_name.grid(row=2, column=0, sticky='e')
# ent_last_name = tk.Entry(left_frame, width=25, font='Arial 15', relief=tk.SUNKEN, borderwidth=3)
# ent_last_name.grid(row=2, column=1)

lbl_place_of_work = tk.Label(left_frame, text='Место работы', font=('Arial', 15), bg='silver')
lbl_place_of_work.grid(row=2, column=0)
ent_place_of_work = tk.Entry(left_frame, width=25, font='Arial 15', relief=tk.SUNKEN, borderwidth=3)
ent_place_of_work.grid(row=2, column=1)

lbl_job_title = tk.Label(left_frame, text='Должность', font=('Arial', 15), bg='silver')
lbl_job_title.grid(row=3, column=0, sticky='e')
ent_job_title = tk.Entry(left_frame, width=25, font='Arial 15', relief=tk.SUNKEN, borderwidth=3)
ent_job_title.grid(row=3, column=1)

lbl_salary_advance = tk.Label(left_frame, text='Аванс', font=('Arial', 15), bg='silver')
lbl_salary_advance.grid(row=4, column=0, sticky='e')
ent_salary_advance = tk.Entry(left_frame, width=25, font='Arial 15', relief=tk.SUNKEN, borderwidth=3)
ent_salary_advance.grid(row=4, column=1)

lbl_salary = tk.Label(left_frame, text='Зарплата', font=('Arial', 15), bg='silver')
lbl_salary.grid(row=5, column=0, sticky='e')
ent_salary = tk.Entry(left_frame, width=25, font='Arial 15', relief=tk.SUNKEN, borderwidth=3)
ent_salary.grid(row=5, column=1)

lbl_stay_salary = tk.Label(left_frame, text='Ставка', font=('Arial', 15), bg='silver')
lbl_stay_salary.grid(row=6, column=0, sticky='e')
ent_stay_salary = tk.Entry(left_frame, width=25, font='Arial 15', relief=tk.SUNKEN, borderwidth=3)
ent_stay_salary.grid(row=6, column=1)

lbl_vacation_pay = tk.Label(left_frame, text='Отпускные', font=('Arial', 15), bg='silver')
lbl_vacation_pay.grid(row=7, column=0, sticky='e')
ent_vacation_pay = tk.Entry(left_frame, width=25, font='Arial 15', relief=tk.SUNKEN, borderwidth=3)
ent_vacation_pay.grid(row=7, column=1)

lbl_commit = tk.Label(left_frame, text='Описание', font=('Arial', 15), bg='silver')
lbl_commit.grid(row=8, column=0, sticky='e')
ent_commit = tk.Entry(left_frame, width=25, font='Arial 15', relief=tk.SUNKEN, borderwidth=3)
ent_commit.grid(row=8, column=1)

btn_add_employee = tk.Button(left_frame, text='Добавить', font=('Arial', 15),
                             bg='Cadetblue1', relief=tk.RAISED, width=25, command=add_in_table)
btn_add_employee.place(relx=0.33, rely=0.32)

btn_update_employee = tk.Button(left_frame, text='Изменить', font=('Arial', 15),
                                bg='Cadetblue3', relief=tk.RAISED, width=25, command=update_data)
btn_update_employee.place(relx=0.33, rely=0.37)

btn_remove_employee = tk.Button(left_frame, text='Удалить', font=('Arial', 15),
                                bg='Cadetblue4', relief=tk.RAISED, width=25, command=button_delete)
btn_remove_employee.place(relx=0.33, rely=0.42)

btn_clear = tk.Button(left_frame, text='Очистить поля ввода', font=('Arial', 15), bg='LightGreen', relief=tk.RAISED,
                      width=25, command=clear_rows)
btn_clear.place(relx=0.33, rely=0.47)

btn_return_data_all = tk.Button(left_frame, text='Вернуться на главную', font=('Arial', 15), relief=tk.RAISED, width=25,
                                command=return_to_main_page, bg='LightBlue2')
btn_return_data_all.place(relx=0.33, rely=0.52)

frame_search = tk.Frame(master=left_frame, width=424, height=100, relief=tk.SUNKEN, bd=4)
frame_search.place(relx=0.01, rely=0.58)

lbl_search = tk.Label(master=frame_search, text='Поиск', font=('Arial', 20))
lbl_search.place(relx=0.01, rely=0.03)

ent_search = tk.Entry(master=frame_search, width=25, font=('Arial', 15), background='black', fg='yellow')
ent_search.place(relx=0.28, rely=0.1)

btn_search = tk.Button(master=frame_search, text='Найти', font=('Arial', 15), relief=tk.RAISED, width=15, bg='Cadetblue1',
                       command=search_data)
btn_search.place(relx=0.40, rely=0.45)
ent_search.config(cursor='gumby red red', insertbackground='red')


right_frame = tk.LabelFrame(master=window)
right_frame.pack(side=tk.LEFT, fill=tk.BOTH)

data_frame = tk.LabelFrame(right_frame, bd=1, relief=tk.SUNKEN)
data_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


tree = ttk.Treeview(data_frame)
tree.pack(side=tk.LEFT, fill=tk.BOTH)
tree['columns'] = ('id', 'date', 'fio',
                   'place_of_work',
                   'job_title', 'salary_advance', 'salary',
                   'stay_salary', 'vacation_pay', 'comment')


scrollbar = ttk.Scrollbar(data_frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scrollbar.set)

# scrollbar2 = ttk.Scrollbar(data_frame, orient=tk.HORIZONTAL, command=tree.xview)
# scrollbar2.pack(side=tk.BOTTOM, fill=tk.X)
# tree.configure(xscrollcommand=scrollbar2.set)

# назаначаем размеры колонок и в какой стороне будет находится название колонки
tree.column('#0', width=0)
tree.column('id', anchor='w', width=30)
tree.column('date', anchor='w', width=60)
tree.column('fio', anchor='w', width=200)
tree.column('place_of_work', anchor='w', width=150)
tree.column('job_title', anchor='w', width=80)
tree.column('salary_advance', anchor='w', width=60)
tree.column('salary', anchor='w', width=60)
tree.column('stay_salary', anchor='w', width=60)
tree.column('vacation_pay', anchor='w', width=80)
tree.column('comment', anchor='w', width=200)
# Название колонок
tree.heading('#0', text='')
tree.heading('id', text='ID')
tree.heading('date', text='Дата', command=lambda : sort_data(1, False))
tree.heading('fio', text='ФИО')
tree.heading('place_of_work', text='Место работы')
tree.heading('job_title', text='Должность')
tree.heading('salary_advance', text='Аванс')
tree.heading('salary', text='Зарплата')
tree.heading('stay_salary', text='Ставка')
tree.heading('vacation_pay', text='Отпускные')
tree.heading('comment', text='Описание')
# Получение данных из ТАБЛИЦЫ
cur.execute(
    """SELECT * FROM employees ORDER BY date"""
)
rows = cur.fetchall()

for row in rows:
    tree.insert('', tk.END, values=row)

tree.bind('<ButtonRelease-1>', deffault_row_info)

window.mainloop()
conn.close()