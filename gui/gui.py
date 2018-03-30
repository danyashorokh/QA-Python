from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *

final = []

def from_gui(event):

    final.append(ent1.get())
    final.append(ent2.get())
    final.append(ent3.get())
    final.append(var1.get())
    final.append(var2.get())
    final.append(var3.get())
    final.append(var4.get())

    for item in final:
        if item == "" or  final[1] == final[2]:
            showinfo("Ошибка", "Заполните все поля")
            break
    #for item in final:
    #    print(item)
    root.destroy()
    return final


# Главное окно
root = Tk()

# Кнопка "Создать"
but1 = Button(root, text = "Создать", width = 20, height = 3, bg = "white",fg = "black")
but1.bind("<Button-1>", from_gui)

# Поле для ввода пути к файлу
lab1 = Label(root, text = "Путь к таблице excel")
ent1 = Entry(root, width = 50, bd =3)
ent1.insert(END, 'C:/Users/DShorokh/Desktop/selenium_excel.xls')

# Поле для ввода номера строки с ключами
lab2 = Label(root, text = "Номер строки с ключами")
ent2 = Entry(root, width = 40, bd =3)
ent2.insert(END, '1')


# Поле для ввода начальной строки с клиентом
lab3 = Label(root, text = "Первая строчка с клиентом")
ent3 = Entry(root, width = 40, bd =3)
ent3.insert(END, '2')

# Выбор количества заявок
lab4 = Label(root, text = "Количество заявок")
var1=IntVar()
var1.set(1)
rad1_1 = Radiobutton(root,text="1",
          variable=var1,value=1)
rad1_2 = Radiobutton(root,text="2",
          variable=var1,value=2)
rad1_3 = Radiobutton(root, text="3",
          variable=var1, value=3)
rad1_4 = Radiobutton(root, text="4",
          variable=var1, value=4)

# Выбор тестовой среды
lab5 = Label(root, text = "Тестовая среда")
var2=IntVar()
var2.set(1)
rad2_1 = Radiobutton(root,text="test1",
          variable=var2,value=1)
rad2_2 = Radiobutton(root,text="test3",
          variable=var2,value=2)

# Выбор региона
lab6 = Label(root, text = "Выбор региона")
var3=IntVar()
var3.set(1)
rad3_1 = Radiobutton(root,text="Регион присутствия",
          variable=var3,value=1)
rad3_2 = Radiobutton(root,text="Не регион присутствия",
          variable=var3,value=2)

# Выбор способа выдачи
lab7 = Label(root, text = "Выбор способа выдачи")
var4=IntVar()
var4.set(1)
rad4_1 = Radiobutton(root,text="Карта",
          variable=var4,value=1)
rad4_2 = Radiobutton(root,text="Контакт",
          variable=var4,value=2)
rad4_3 = Radiobutton(root, text="Юнистрим",
          variable=var4,value=3)

# Размещение элементов
lab1.pack()
ent1.pack()
lab2.pack()
ent2.pack()
lab3.pack()
ent3.pack()
lab4.pack()
rad1_1.pack()
rad1_2.pack()
rad1_3.pack()
rad1_4.pack()
lab5.pack()
rad2_1.pack()
rad2_2.pack()
lab6.pack()
rad3_1.pack()
rad3_2.pack()
lab7.pack()
rad4_1.pack()
rad4_2.pack()
rad4_3.pack()
but1.pack()
root.mainloop()

#----------------

print(final)