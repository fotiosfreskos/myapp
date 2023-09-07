from tkinter import *
from PIL import ImageTk , Image
import mysql.connector
from tkinter import messagebox
from customerlibrary import CustomerLibs
from loginbackend import *
from tkinter import colorchooser
from tkinter import ttk

root=Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg='#fff')
root.resizable(False , False)


db = mysql.connector.connect(host ='xxx.xxx.xxx.xxx',
                            user = 'root',
                            password = 'password123',
                            db = 'database')
            
cur = db.cursor()


def main_app():
    othoni = Toplevel(root)
    othoni.title('MyApp')
    othoni.geometry('1280x500')
    
    def primary_color():
        primary_color = colorchooser.askcolor()[1]

        if primary_color:
            my_tree.tag_configure('evenrow' , background=primary_color)

    def secondary_color():
        secondary_color = colorchooser.askcolor()[1]
        
        if secondary_color:
            my_tree.tag_configure('oddrow' , background=secondary_color)

    def highlight_color():
        highlight_color = colorchooser.askcolor()[1]

        if highlight_color:
            style.map('Treeview' ,
                    background=[('selected', highlight_color)])

    
    db = mysql.connector.connect(host ='xxx.xxx.xxx.xxx',
                                user = 'root',
                                password = 'password123',
                                db = 'database')
    cur = db.cursor()
        
    cur.execute("""CREATE TABLE if not exists `cars` (
    `ID` int NOT NULL,
    `Brand` varchar(45) DEFAULT NULL,
    `Model` varchar(45) DEFAULT NULL,
    `YearOfProduction` date DEFAULT NULL,
    `Country` varchar(45) DEFAULT NULL,
    `Price` decimal(15,2) DEFAULT NULL,
    PRIMARY KEY (`ID`),
    UNIQUE KEY `ID_UNIQUE` (`ID`)
    )  """)
    
    def update_record():
        selected = my_tree.focus()
        my_tree.item(selected , text='', values=(id_entry.get() ,b_entry.get(), m_entry.get() , yp_entry.get() , c_entry.get(), p_entry.get(),))
        
        db = mysql.connector.connect(host ='xxx.xxx.xxx.xxx',
                                    user = 'root',
                                    password = 'password123',
                                    db = 'database')
        
        cur = db.cursor()
        

        update_query ="""UPDATE cars SET brand = %s , model =%s , yearofproduction= %s , country=%s , price=%s WHERE id =%s"""
        cur.execute(update_query , (b_entry.get() , m_entry.get() , yp_entry.get(), c_entry.get(), p_entry.get(), id_entry.get()))

        db.commit()
        db.close()

        id_entry.delete(0 , END)
        b_entry.delete(0 , END)
        m_entry.delete(0 , END)
        yp_entry.delete(0 , END)
        c_entry.delete(0 , END)
        p_entry.delete(0 , END)




    def add_record():
        
        db = mysql.connector.connect(host ='xxx.xxx.xxx.xxx',
                                    user = 'root',
                                    password = 'password123',
                                    db = 'database')
        
        cur = db.cursor()
        
        insert_query ="""INSERT INTO cars (id , brand , model , yearofproduction, country , price ) VALUES (%s,%s,%s,%s,%s,%s)"""
        cur.execute(insert_query , (id_entry.get() ,b_entry.get() , m_entry.get() , yp_entry.get(), c_entry.get(), p_entry.get()))



        db.commit()
        db.close()

        id_entry.delete(0, END)
        b_entry.delete(0 , END)
        m_entry.delete(0 , END)
        yp_entry.delete(0 , END)
        c_entry.delete(0 , END)
        p_entry.delete(0 , END)

        my_tree.delete(*my_tree.get_children())
        query_database()


    def remove_all():
        response = messagebox.askyesno("ATTENTION!", "You will delete all entries!\nAre you sure?")

        if response == 1:
            for record in my_tree.get_children():
                my_tree.delete(record)
            
            db = mysql.connector.connect(host ='xxx.xxx.xxx.xxx',
                                        user = 'root',
                                        password = 'password123',
                                        db = 'database')    
            cur = db.cursor()
            
            cur.execute("DROP TABLE cars")

            db.commit()
            db.close()        
            clear_entries()
            create_table_again()

    def remove_many():
        response = messagebox.askyesno("ATTENTION!", "You will delete all SELECTED entries!\nAre you sure?")    
        
        if response ==1:
            x = my_tree.selection()
            
            ids_to_delete = []

            
            for record in x:
                ids_to_delete.append(my_tree.item(record, 'values')[0])
            
            for record in x:
                my_tree.delete(record)
            
            db = mysql.connector.connect(host ='xxx.xxx.xxx.xxx',
                                        user = 'root',
                                        password = 'password123',
                                        db = 'database')
            cur = db.cursor()
            
            dlt = "DELETE FROM cars WHERE id IN (%s)"
            inlist=', '.join(map(lambda x: '%s', ids_to_delete))
            dlt = dlt % inlist
            cur.execute(dlt , ids_to_delete)

            

            db.commit()
            db.close()        
            clear_entries()
            create_table_again()


    def remove_one():
        x = my_tree.selection()[0]
        my_tree.delete(x)
        
        db = mysql.connector.connect(host ='xxx.xxx.xxx.xxx',
                                    user = 'root',
                                    password = 'password123',
                                    db = 'database')    
        cur = db.cursor()
        
        cur.execute("DELETE FROM cars WHERE id=" + id_entry.get())

        db.commit()
        db.close()
        clear_entries()

        messagebox.showinfo("Deleted!" , "Your Record Has Been Deleted!")

    def up():
        rows = my_tree.selection()
        for row in rows:
            my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)

    def down():
        rows = my_tree.selection()
        for row in reversed(rows):
            my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)

    def clear_entries():
        id_entry.delete(0, END)
        b_entry.delete(0 , END)
        m_entry.delete(0 , END)
        yp_entry.delete(0 , END)
        c_entry.delete(0 , END)
        p_entry.delete(0 , END)


    def select_record(e):
        id_entry.delete(0, END)
        b_entry.delete(0 , END)
        m_entry.delete(0 , END)
        yp_entry.delete(0 , END)
        c_entry.delete(0 , END)
        p_entry.delete(0 , END)

        selected = my_tree.focus()

        values = my_tree.item(selected , 'values')

        id_entry.insert(0 , values[0])
        b_entry.insert(0 , values[1])
        m_entry.insert(0 , values[2])
        yp_entry.insert(0 , values[3])
        c_entry.insert(0 , values[4])
        p_entry.insert(0 , values[5])

    def query_database():
        
        db = mysql.connector.connect(host ='xxx.xxx.xxx.xxx',
                                    user = 'root',
                                    password = 'password123',
                                    db = 'database')
        
        cur = db.cursor()
        
        cur.execute('SELECT * FROM cars')
        myresult1 = cur.fetchall()
        

        global count
        count= 0

        for record in myresult1:
            if count % 2 ==0:
                my_tree.insert(parent='', index='end', iid=count , text='' , values=(record[0], record[1] , record[2] , record[3] , record[4] , record[5]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count , text='' , values=(record[0], record[1] , record[2] , record[3] , record[4] , record[5]), tags=('oddrow',))
            count += 1
        
        db.commit()
        db.close()    

    def create_table_again():
        
        db = mysql.connector.connect(host ='xxx.xxx.xxx.xxx',
                                    user = 'root',
                                    password = 'password123',
                                    db = 'database')
        cur = db.cursor()
        
        cur.execute("""CREATE TABLE if not exists `cars` (
        `ID` int NOT NULL,
        `Brand` varchar(45) DEFAULT NULL,
        `Model` varchar(45) DEFAULT NULL,
        `YearOfProduction` date DEFAULT NULL,
        `Country` varchar(45) DEFAULT NULL,
        `Price` decimal(15,2) DEFAULT NULL,
        PRIMARY KEY (`ID`),
        UNIQUE KEY `ID_UNIQUE` (`ID`)
        )  """)
        db.commit()
        db.close()  

    frame1 = Frame(othoni)
    frame1.place(x=0 , y=0 , width='1280' , height='500')

    leftframe = Frame(othoni , relief=GROOVE , bg='white')
    leftframe.place(x=5 , y=10 , width='380' , height='470' )

    rightframe = Frame(othoni , relief=GROOVE , bg='white')
    rightframe.place(x=390 , y=10 , width='885' , height='470' )

    data_frame = LabelFrame(leftframe , text='Record' , background='white' , fg='black')
    data_frame.pack(fill='x', expand='yes', padx=0)

    id_label = Label(data_frame, text='ID' , background='white' , fg='black')
    id_label.grid(row=0 , column=0 , padx=10 , pady=10)
    id_entry = Entry(data_frame)
    id_entry.grid(row=0, column=1 , padx=10 , pady=10)

    b_label = Label(data_frame, text='Brand' , background='white' , fg='black')
    b_label.grid(row=1 , column=0 , padx=10 , pady=10)
    b_entry = Entry(data_frame)
    b_entry.grid(row=1, column=1 , padx=10 , pady=10)

    m_label = Label(data_frame, text='Model', background='white' , fg='black')
    m_label.grid(row=2 , column=0 , padx=10 , pady=10)
    m_entry = Entry(data_frame)
    m_entry.grid(row=2, column=1 , padx=10 , pady=10)

    yp_label = Label(data_frame, text='YearOfProduction', background='white' , fg='black')
    yp_label.grid(row=3 , column=0 , padx=10 , pady=10)
    yp_entry = Entry(data_frame)
    yp_entry.grid(row=3, column=1 , padx=10 , pady=10)

    c_label = Label(data_frame, text='Country', background='white' , fg='black')
    c_label.grid(row=4 , column=0 , padx=10 , pady=10)
    c_entry = Entry(data_frame)
    c_entry.grid(row=4, column=1 , padx=10 , pady=10)

    p_label = Label(data_frame, text='Price', background='white' , fg='black')
    p_label.grid(row=5 , column=0 , padx=10 , pady=10)
    p_entry = Entry(data_frame)
    p_entry.grid(row=5, column=1 , padx=10 , pady=10)

    button_frame = LabelFrame(leftframe, text='Commands' )
    button_frame.pack(fill='x' , expand='yes', padx=0)

    update_button = Button(button_frame, text='UPDATE RECORD' , command=update_record)
    update_button.grid(row=0 , column=0)

    add_button = Button(button_frame, text='ADD RECORD', command=add_record)
    add_button.grid(row=1 , column=0)

    remove_all_button = Button(button_frame, text='REMOVE ALL' , command=remove_all)
    remove_all_button.grid(row=2 , column=0)

    remove_one_button = Button(button_frame, text='REMOVE SELECTED' , command=remove_one)
    remove_one_button.grid(row=3 , column=0)

    remove_many_button = Button(button_frame, text='REMOVE MANY SELECTED' , command=remove_many)
    remove_many_button.grid(row=0 , column=1)

    select_button = Button(button_frame, text='CLEAR ENTRIES' , command=clear_entries)
    select_button.grid(row=1 , column=1)

    moveup_button = Button(button_frame, text='MOVE UP' , command=up)
    moveup_button.grid(row=2 , column=1)

    movedown_button = Button(button_frame, text='MOVE DOWN' , command=down)
    movedown_button.grid(row=3 , column=1)


    style = ttk.Style()


    style.theme_use('default')

    style.configure('Treeview',
        background='#D3D3D3',
        foreground='black',
        rowheight='25',
        filedbackground='#D3D3D3')

    style.map('Treeview',
            background=[('selected', '#347083')])

    tree_frame = Frame(rightframe)
    tree_frame.place(x=0 , y=0 ,width='880' , height='450' )

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(tree_frame , yscrollcommand=tree_scroll.set, selectmode='extended' , height='450')
    my_tree.pack()

    tree_scroll.config(command=my_tree.yview)

    my_tree.tag_configure('oddrow' , background='white')
    my_tree.tag_configure('evenrow' , background='lightblue')

    my_tree['columns'] = ('ID','Brand' , 'Model', 'YearOfProduction' , 'Country' , 'Price' )

    my_tree.column('#0', width=0, stretch=NO)
    my_tree.column('ID', anchor=W, width=142)
    my_tree.column('Brand', anchor=W, width=142)
    my_tree.column('Model', anchor=W, width=142)
    my_tree.column('YearOfProduction', anchor=CENTER, width=142)
    my_tree.column('Country', anchor=CENTER, width=142)
    my_tree.column('Price', anchor=CENTER, width=142)

    my_tree.heading('#0', text='', anchor=W)
    my_tree.heading('ID', text='ID', anchor=W)
    my_tree.heading('Brand', text='Brand', anchor=W)
    my_tree.heading('Model', text='Model', anchor=W)
    my_tree.heading('YearOfProduction', text='YearOfProduction', anchor=CENTER)
    my_tree.heading('Country', text='Country', anchor=CENTER)
    my_tree.heading('Price', text='Price', anchor=CENTER)

    my_menu = Menu(othoni)
    othoni.config(menu=my_menu)

    option_menu= Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label='Options', menu=option_menu)

    option_menu.add_command(label='Change Primary Colour', command=primary_color)
    option_menu.add_command(label='Change Secondary Colour', command=secondary_color)
    option_menu.add_command(label='Highlight Colour', command=highlight_color)
    option_menu.add_separator()
    option_menu.add_command(label='Exit', command=othoni.quit)

    my_tree.bind('<ButtonRelease-1>' , select_record)

    query_database()


def login_page():
    screen = Toplevel(root)
    screen.title('Log in')
    screen.geometry('500x500+300+200')
    screen.configure(bg='#fff')
    screen.resizable(False , False)

    
    db = mysql.connector.connect(host ='xxx.xxx.xxx.xxx',
                                user = 'root',
                                password = 'password123',
                                db = 'database')
        
    cur = db.cursor()
    
    def add_record():


        insert_query ="""INSERT INTO login (usefirstname , userlastname , userdateofbirth , usercountry, useraccountusername , userpassword ) VALUES (%s,%s,%s,%s,%s,%s)"""
        cur.execute(insert_query , (firstnameentry.get() ,lastnameentry.get() , dateofbirthentry.get() , countryentry.get(), accountusernameentry.get(), passwordentry.get()))



        db.commit()
        db.close()

        firstnameentry.delete(0, END)
        lastnameentry.delete(0 , END)
        dateofbirthentry.delete(0 , END)
        countryentry.delete(0 , END)
        accountusernameentry.delete(0 , END)
        passwordentry.delete(0 , END)

    signuplbl = Label(screen , text='Sign Up ', fg='#57a1f8', bg='White', font=('Microsoft YaHei UI Light',23,'bold'))
    signuplbl.place(x=200 , y=10)

    firstnamelbl = Label(screen , text='First Name:', fg='black', bg='White', font=('Microsoft YaHei UI Light',16))
    firstnamelbl.place(x=10 , y=60)
    firstnameentry = Entry(screen ,width=20,fg='black', border=0, highlightbackground='black',relief=GROOVE ,bg='white', font=('Microsoft YaHei UI Light',13))
    firstnameentry.place(x=120 , y=60)

    lastnamelbl = Label(screen , text='Last Name:', fg='black', bg='White', font=('Microsoft YaHei UI Light',16))
    lastnamelbl.place(x=10 , y=95)
    lastnameentry = Entry(screen ,width=20,fg='black', border=0, highlightbackground='black',relief=GROOVE ,bg='white', font=('Microsoft YaHei UI Light',13))
    lastnameentry.place(x=120 , y=95)

    dateofbirthlbl = Label(screen , text='Date of Birth:', fg='black', bg='White', font=('Microsoft YaHei UI Light',16))
    dateofbirthlbl.place(x=10 , y=130)
    dateofbirthentry = Entry(screen ,width=20,fg='black', border=0, highlightbackground='black',relief=GROOVE ,bg='white', font=('Microsoft YaHei UI Light',13))
    dateofbirthentry.place(x=120 , y=130)

    countrylbl = Label(screen , text='Country:', fg='black', bg='White', font=('Microsoft YaHei UI Light',16))
    countrylbl.place(x=10 , y=165)
    countryentry = Entry(screen ,width=20,fg='black', border=0, highlightbackground='black',relief=GROOVE ,bg='white', font=('Microsoft YaHei UI Light',13))
    countryentry.place(x=120 , y=165)

    accountusernamelbl = Label(screen , text='Username:', fg='black', bg='White', font=('Microsoft YaHei UI Light',16))
    accountusernamelbl.place(x=10 , y=200)
    accountusernameentry = Entry(screen ,width=20,fg='black', border=0, highlightbackground='black',relief=GROOVE ,bg='white', font=('Microsoft YaHei UI Light',13))
    accountusernameentry.place(x=120 , y=200)

    passwordlbl = Label(screen , text='Password:', fg='black', bg='White', font=('Microsoft YaHei UI Light',16))
    passwordlbl.place(x=10 , y=235)
    passwordentry = Entry(screen ,width=20,fg='black',show='*', border=0, highlightbackground='black',relief=GROOVE ,bg='white', font=('Microsoft YaHei UI Light',13))
    passwordentry.place(x=120 , y=235)

    submitbutton = Button(screen ,width=17,pady=7,text='Submit',fg='#57a1f8',bg='white',border=0 , command=add_record)
    submitbutton.place(x=120 , y=280)


leftframe = Frame(root , relief=GROOVE , bg='white')
leftframe.place(x=100 , y=70 , width='380' , height='300' )

img = ImageTk.PhotoImage(Image.open('/Users/xxxxxxx/Documents/myapp/login.png'))
myimg = Label(leftframe ,image=img , bg='white').pack()

frame=Frame(root,width=350,height=350,bg='white')
frame.place(x=480,y=70)

heading = Label(frame, text='Sign in', fg='#57a1f8', bg='White', font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=130,y=5)


LabelFrame(frame , text='Username',width=300,height=43 , bg='white').place(x=25,y=65)


user = Entry(frame,width=31,fg='black', border=0, highlightbackground='white', highlightcolor='white',relief=FLAT ,bg='white', font=('Microsoft YaHei UI Light',13))
user.place(x=30,y=80)


LabelFrame(frame , text='Password',width=300,height=43 , bg='white').place(x=25,y=115)


passw = Entry(frame,width=31,fg='black', show='*' ,border=0 , highlightbackground='white', highlightcolor='white',bg='white', font=('Microsoft YaHei UI Light',13))
passw.place(x=30,y=130)



def loginlogic():
            customerdata=CustomerLibs(username=user.get(), password=passw.get())
            result=login(customerdata)
            if result!=None:
                main_app()
            else:
                messagebox.showerror('Error','Incorrect Email or Password')

Button(frame,width=27,pady=7,text='Sign in',fg='#57a1f8',bg='white',border=0 , command=loginlogic).place(x=35,y=190)
label=Label(frame,text="Don't have an account?",fg='black',bg='white', font=('Microsoft YaHei UI Light',10))
label.place(x=75,y=235)


sign_up=Button(frame,width=6,text='Sign Up',border=0,background='white',cursor='hand', fg='#57a1f8',font=('Microsoft YaHei UI Light',9) , command=login_page )
sign_up.place(x=195,y=235)



root.mainloop()



