from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Style, Treeview
from cryptography.fernet import Fernet
import sqlite3
import textwrap
import smtplib
from email.message import EmailMessage
import random
import time



mainscreen = Tk()
mainscreen.geometry('600x600')

mycon = sqlite3.connect('Password_Manager_DB.db')
cur = mycon.cursor()

cur.execute(
    '''
    CREATE TABLE IF NOT EXISTS PASSWORDS
    (
        PASS_ID INT(5) PRIMARY KEY,
        KEY VARCHAR(50),
        ENCRYPT_PASS MEDIUMTEXT NOT NULL,
        PASS_DETAILS VARCHAR(100) NOT NULL UNIQUE,
        ACC_NO INT(5) 
    );
    '''
)

# cur.execute("Drop table passwords;")
cur.execute(
    '''
    CREATE TABLE IF NOT EXISTS ACCOUNTS
    (
        ACC_ID INT(5) PRIMARY KEY,
        ACC_NAME VARCHAR(30) UNIQUE,
        ACC_PASS VARCHAR(30) NOT NULL,
        EMAIL TEXT NOT NULL
    );
    '''
)

def Password_Details():
    cur.execute('SELECT * FROM PASSWORDS;')
    pass_data = cur.fetchall()

    return pass_data, (len(pass_data))


def Account_Details():
    cur.execute('SELECT * FROM ACCOUNTS;')
    acc_data = cur.fetchall()

    return acc_data, (len(acc_data))


def create_new_acc():
    global entscr51
    global entscr52
    global entscr53
    global screen6
    global entscr6_email
    global btn_show_pass

    data, no_of_accounts = Account_Details()

    if no_of_accounts == 5:
        messagebox.showinfo('Maximum Accounts Created', 
                            "You have already created the 5 accounts and that is the maximum number of accounts you can create. Please delete an account to create another one.")

    elif no_of_accounts < 5:
        screen6 = Toplevel(mainscreen)
        screen6.geometry('732x438')
        Label(screen6,text='Create an Account to store all your Passwords along with their Keys',font=('Consolas Bold',20),wraplength=600).place(x=90,y=30)
        Label(screen6,text='Account Name:',font=('Consolas Bold',16)).place(x=10,y=150)
        Label(screen6,text='Password:',font=('Consolas Bold',16)).place(x=10,y=190)
        Label(screen6, text='Email:', font=('Consolas Bold', 16)).place(x=10,y=230)
        Label(screen6,text='Confirm Password:',font=('Consolas Bold',16), fg='#FF0000').place(x=10,y=270)

        entscr51 = Entry(screen6,width=30,border=6,font=('Arial 14')) # Taking Account Name
        entscr52 = Entry(screen6,width=30,border=6,font=('Arial 14'), show='*') # Taking Password
        entscr53 = Entry(screen6,width=30,border=6,font=('Arial 14'), show='*') # Taking Confirmed Password
        entscr6_email = Entry(screen6, width=30, border=6, font=('Arial 14')) # Taking Email

        entscr51.place(x=370,y=150)
        entscr52.place(x=370,y=190)
        entscr6_email.place(x=370,y=230)
        entscr53.place(x=370,y=270)

        entscr51.focus() 
        entscr51.bind('<Return>', func=lambda x: entscr52.focus())
        entscr52.bind('<Return>', func=lambda x: entscr6_email.focus())
        entscr6_email.bind('<Return>', func=lambda x: entscr53.focus())
        entscr53.bind('<Return>', lambda x: save_to_acc())

        btn_show_pass = Button(screen6, text='Show Password*', font=('Arial', 10, 'bold'), padx=113, pady=2, border=1, command=reveal_password)
        Button(screen6,text='Create Account',font=('Malgun Gothic Bold',18),padx=70,pady=10,borderwidth=5,command=save_to_acc).place(x=10,y=340)
        Button(screen6,text='Cancel',font=('Malgun Gothic Bold',18),padx=125,pady=10,borderwidth=5,command=screen6.destroy).place(x=365,y=340)

        btn_show_pass.place(x=370, y=300)


def reveal_password():
    entscr52.configure(show='')
    entscr53.config(show='')
    btn_show_pass.config(text='Hide Password*', command=conceal_pass, padx=117)


def conceal_pass():
    entscr52.config(show='*')
    entscr53.config(show='*')

    btn_show_pass.config(text='Show Password*', command=reveal_password, padx=113)


def show_pass(entry_wid: Entry, button_text: Button, show_x_coords:int, hide_x_coords:int):
    entry_wid.config(show='')

    button_text.config(text='Hide Password*', 
                        command=lambda: hide_pass(entry_wid, button_text, show_x_coords, hide_x_coords),
                        padx=hide_x_coords)


def hide_pass(entry_wid: Entry, button_text: Button, show_x_coords: int, hide_x_coords: int):
    entry_wid.config(show='*')

    button_text.config(text='Show Password*', 
                        command=lambda: show_pass(entry_wid, button_text, show_x_coords, hide_x_coords), 
                        padx=show_x_coords)


def save_existing_acc():
    cur.execute('SELECT * FROM ACCOUNTS;')
    acc_indb = cur.fetchall()

    if len(entscr54.get()) and len(entscr55.get()) > 0:
        for acc in acc_indb:
            if (acc[1] == entscr54.get()) and (acc[2] == entscr55.get()):
                cur.execute('SELECT * FROM PASSWORDS;')
                last_pass = cur.fetchall()

                cur.execute(f'''UPDATE PASSWORDS SET KEY = '{gen_key.decode()}' , ACC_NO = {acc[0]} 
                                WHERE PASS_ID = {last_pass[-1][0]};''')
                mycon.commit()

                screen5.destroy()
                screen4.destroy()
                ent2scr3.focus()

                ent1scr3.delete(0,END)

                data, num_of_data = Password_Details()
                if (num_of_data+1) < 10:
                    ent1scr3.insert(0,f"0{num_of_data + 1}")
                elif (num_of_data+1) >= 10:
                    ent1scr3.insert(0,f"{num_of_data + 1}")

                ent2scr3.delete(0,END)
                ent3scr3.delete(0,END)
                break
        else:
            for acc2 in acc_indb:
                if acc2[1] == entscr54.get() and acc2[2] != entscr55.get():
                    messagebox.showerror('Wrong Password','You have entered the wrong Password',parent=screen5)
                    break
            else:
                messagebox.showerror('Wrong Account Name',f'''Account "{entscr54.get()}" doesn't exist''',parent=screen5)


def create_another_acc(win: Toplevel): 
    data, number_of_data = Account_Details()

    if number_of_data == 5:
        messagebox.showinfo('Maximum Accounts Created', "You can create a maximum of 5 accounts. To create another account you need to delete any of the current accounts.", parent=win)
    elif number_of_data < 5:
        win.destroy()
        create_new_acc()


def save_to_acc():
    if len(entscr51.get().split()) and len(entscr53.get().split()) and len(entscr6_email.get().split()) > 0:
        if entscr52.get() == entscr53.get():
            if len(entscr53.get()) >= 5:
                cur.execute('SELECT * FROM ACCOUNTS;')
                acc_nos = cur.fetchall()

                global last_pass
                cur.execute('SELECT * FROM PASSWORDS;')
                last_pass = cur.fetchall()
                
                data, num_of_data = Account_Details()
                cur.execute(f'''INSERT INTO ACCOUNTS VALUES({num_of_data+1},'{entscr51.get()}',
                                '{entscr53.get()}', '{entscr6_email.get()}');''')
                mycon.commit()

                cur.execute(f"UPDATE PASSWORDS SET KEY = '{gen_key.decode()}' , ACC_NO = {len(acc_nos)+1} WHERE PASS_ID = {last_pass[-1][0]};")
                mycon.commit()
                
                screen6.destroy()
                screen4.destroy()
                ent2scr3.focus()

                ent1scr3.delete(0,END)

                data, num_of_recs = Password_Details()
                if (num_of_recs+1) < 10:
                    ent1scr3.insert(0,f"0{num_of_recs + 1}")
                elif (num_of_recs+1) >= 10:
                    ent1scr3.insert(0,f"{num_of_recs + 1}")

                ent2scr3.delete(0,END)
                ent3scr3.delete(0,END)

                messagebox.showinfo('Operation Successful',f"Your Account has been Created with Account ID:{len(acc_nos)+1} and your password along with the Encryption Key has been saved here",parent=screen3)

            else:
                messagebox.showwarning('Passoword too short','Password must contain atleast 5 characters',parent=screen6)
        else:
            messagebox.showerror('Error','Wrong Password! Password Confirmation cannot procced',parent=screen6)
    else:
        messagebox.showwarning('Details not filled','You need to fill the details to create an account',parent=screen6)


def ok_dontsave():
    msg = messagebox.askyesnocancel("Key Won't be Saved","You need to enter the key in order to decrypt the password, if you do not save your key you have to protect the key at your own risk. Do you want to continue?",parent=screen4)
    if msg == True:
        screen4.destroy()
        ent2scr3.focus()
        
        ent1scr3.delete(0,END)

        data, total_data = Password_Details()
        if (total_data+1) < 10:
            ent1scr3.insert(0,f"0{total_data + 1}")
        elif (total_data+1) >= 10:
            ent1scr3.insert(0,f"{total_data + 1}")
            
        ent2scr3.delete(0,END)
        ent3scr3.delete(0,END)


def saveto_acc():
    global entscr54
    global entscr55
    global screen5

    screen5 = Toplevel(mainscreen)
    cur.execute("SELECT * FROM ACCOUNTS;")
    acc_data = cur.fetchall()

    if len(acc_data) == 0:
        create_another_acc(win=screen5)

    elif len(acc_data) > 0:
        screen5.geometry('656x314')
        Label(screen5,text='Your Account Details',font=('Cambria Bold',20)).place(x=20,y=20)
        Label(screen5,text='Account Name:',font=('Cambria Bold',16)).place(x=20,y=90)
        Label(screen5,text='Account Password:',font=('Cambria Bold',16)).place(x=20,y=140)

        entscr54 = Entry(screen5,width=30,border=10,font=('Arial 14'))
        entscr55 = Entry(screen5,width=30,border=10,font=('Arial 14'))

        entscr54.place(x=280,y=90)
        entscr55.place(x=280,y=140)

        entscr54.focus()
        entscr54.bind(sequence='<Return>', func=lambda x: entscr55.focus())
        entscr55.bind(sequence='<Return>', func=lambda x: save_existing_acc())

        Button(screen5,text='Create New Account',font=('Malgun Gothic Bold',16),padx=20,pady=10,borderwidth=5,command=lambda: create_another_acc(win=screen5)).place(x=20,y=210)
        Button(screen5,text='OK',font=('Malgun Gothic Bold',16),padx=55,pady=10,borderwidth=5,command=save_existing_acc).place(x=294,y=210)
        Button(screen5,text='Cancel',font=('Malgun Gothic Bold',16),padx=40,pady=10,borderwidth=5,command=screen5.destroy).place(x=462,y=210)

        
def ok_add():
    global screen4
    global gen_key

    if len(ent2scr3.get().split()) and len(ent3scr3.get().split()) > 0:
        data_of_passwords, len_of_pass = Password_Details()
        for rec in data_of_passwords:
            if ent3scr3.get() == rec[3]:
                messagebox.showwarning('Duplicate Details', "A password has already been stored for these details. Please provide a different detail for your password.", parent=screen3)
                break

        else:
            screen4 = Toplevel(mainscreen)
            screen4.geometry('770x500')

            gen_key = Fernet.generate_key()
            key = Fernet(gen_key)

            encrypt_data = key.encrypt(ent2scr3.get().encode())

            cur.execute(f"INSERT INTO PASSWORDS(PASS_ID,ENCRYPT_PASS,PASS_DETAILS) VALUES({ent1scr3.get()},'{encrypt_data.decode()}','{ent3scr3.get()}');")
            mycon.commit()

            Label(screen4,text='The Encrypted form of your Password:',font=('Courier New Bold',18),wraplength=400).place(x=200,y=20)
            Label(screen4,text='The Key to Decrypt your Password:',font=('Courier New Bold',18),wraplength=400).place(x=200,y=200)

            text_enpass = Text(screen4,wrap=CHAR,bd=5,height=4,width=80,font=('Arial',12))
            text_key = Text(screen4,wrap=CHAR,bd=5,height=4,width=80,font=('Arial',12))

            text_enpass.place(x=20,y=90)
            text_key.place(x=20,y=270)
            screen4.focus()
            
            text_key.insert(END,gen_key.decode())
            text_enpass.insert(END,encrypt_data.decode())

            Button(screen4,text='OK',font=('Malgun Gothic Bold',18),padx=152,pady=10,borderwidth=5,command=ok_dontsave).place(x=20,y=400)
            Button(screen4,text='Save',font=('Malgun Gothic Bold',18),padx=135,pady=10,borderwidth=5,command=saveto_acc).place(x=400,y=400)
    else:
        messagebox.showerror('No Password to Encrpyt','You need to fill the details to continue',parent=screen3)


def add_recs():
    global screen3
    global ent1scr3
    global ent2scr3
    global ent3scr3

    screen3 = Toplevel(mainscreen,bg='#A2A2D0')
    screen3.geometry('600x520')

    Label(screen3,text='Details',font=('Constantia Bold',30),bg='#A2A2D0').place(x=230,y=20)

    Label(screen3,text='Sl. No.',font=('Sitka Subheading Bold',20),bg='#A2A2D0').place(x=255,y=100)
    Label(screen3,text='Password',font=('Sitka Subheading Bold',20),bg='#A2A2D0').place(x=235,y=200)
    Label(screen3,text='Details about the Password',font=('Sitka Subheading Bold',20),bg='#A2A2D0').place(x=130,y=300)

    ent1scr3 = Entry(screen3,font=('Arial 14'),width=30,border=10)
    ent2scr3 = Entry(screen3,font=('Arial 14'),width=30,border=10)
    ent3scr3 = Entry(screen3,font=('Arial 14'),width=30,border=10)

    ent1scr3.place(x=130,y=150)
    ent2scr3.place(x=130,y=250)
    ent3scr3.place(x=130,y=350)

    ent2scr3.focus()
    ent2scr3.bind('<Return>', lambda x: ent3scr3.focus())
    ent3scr3.bind('<Return>', lambda x: ok_add())

    data, total_data = Password_Details()
    if (total_data+1) < 10:
        ent1scr3.insert(0,f"0{total_data + 1}")
    elif (total_data+1) >= 10:
        ent1scr3.insert(0,f"{total_data + 1}")
    
    Button(screen3,text='OK',font=('Malgun Gothic Bold',18),padx=104,pady=3,borderwidth=8,command=ok_add).place(x=20,y=430)
    Button(screen3,text='Cancel',font=('Malgun Gothic Bold',18),padx=80,pady=3,borderwidth=8,command=screen3.destroy).place(x=312,y=430)


def del_Pass():
    global del_ent1
    global del_ent2
    global del_scr2
    global show_pass_delscr2
   
    del_scr2 = Toplevel(mainscreen)
    del_scr2.geometry('626x300')

    Label(del_scr2,text='Account Details',font=('Bahnschrift',20),).place(x=210,y=20)
    Label(del_scr2,text='Account Name:',font=('Bahnschrift',14)).place(x=20,y=80)
    Label(del_scr2,text='Account Password:',font=('Bahnschrift',14)).place(x=20,y=120)

    del_ent1 = Entry(del_scr2,width=30,border=10,font=('Arial 14'))
    del_ent2 = Entry(del_scr2,width=30,border=10,font=('Arial 14'), show='*')
                                                                                         
    del_ent1.place(x=250,y=80)
    del_ent2.place(x=250,y=120)

    del_ent1.focus()
    del_ent1.bind('<Return>', func=lambda x: del_ent2.focus())
    del_ent2.bind('<Return>', func=lambda x: del_display_pass())

    show_pass_delscr2 = Button(del_scr2, text='Show Password*', font=('Arial', 8), padx=126, pady=2, borderwidth=1,
     command=lambda: show_pass(entry_wid=del_ent2, button_text=show_pass_delscr2, show_x_coords=126, hide_x_coords=128))
    show_pass_delscr2.place(x=250, y=160)

    Button(del_scr2,text='OK',font=('Malgun Gothic Bold',18),padx=110,pady=10,borderwidth=5,command=del_display_pass).place(x=20,y=200)
    Button(del_scr2,text='Cancel',font=('Malgun Gothic Bold',18),padx=90,pady=10,borderwidth=5,command=del_scr2.destroy).place(x=320,y=200)


def Update_Pass_ID():
    cur.execute('SELECT * FROM PASSWORDS;')
    Old_Data = cur.fetchall()

    NEW_ID = 1
    for pass_Id in Old_Data:
        cur.execute(f'UPDATE PASSWORDS SET PASS_ID = {NEW_ID} WHERE PASS_ID = {pass_Id[0]};')
        mycon.commit()

        NEW_ID += 1


def display_keys():
    pass


def Send_Email(reciever, screen):
    global otp

    messagebox.showinfo(title='OTP is being sent...', 
                message="Please wait...", parent=screen)

    random_num = random.randrange(start=100000, stop=999999)
    num_list = [num for num in str(random_num)]
    otp = ' '.join(num_list)

    subject = 'OTP from Password Manager'
    body = f'OTP: {otp}'

    sender = 'pythonwithemail@gmail.com'
    sender_pass = 'mccpvtbkfersehzk'

    email = EmailMessage()
    email['From'] = sender
    email['To'] = reciever
    email['subject'] = subject
    email.set_content(body)

    email_to_sent = email.as_string()

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as server:
        server.starttls()
        server.login(user=sender, password=sender_pass)
        server.sendmail(from_addr=sender, to_addrs=reciever, msg=email_to_sent)

    messagebox.showinfo('OTP Sent', 'A 6-digit OTP has been sent to your email.', parent=screen)
    

def del_specific_rec():
    rec_index = del_display_tree.focus()
    selected_rec_value = del_display_tree.item(rec_index,'values')

    warning = messagebox.askyesno('Password will be deleted', 
                                'Are you sure you want to delete this password?', parent=del_display_scr)
    if warning == True:
        cur.execute(F"DELETE FROM PASSWORDS WHERE PASS_ID = {selected_rec_value[0]};")
        mycon.commit()

        del_display_tree.delete(rec_index)

        cur.execute(F'''SELECT P.PASS_ID, P.ENCRYPT_PASS, P.PASS_DETAILS, 
                        P.ACC_NO, A.ACC_NAME, A.ACC_PASS 
                        FROM PASSWORDS P, ACCOUNTS A 
                        WHERE A.ACC_ID = P.ACC_NO AND 
                        (A.ACC_NAME = '{acc_name}' AND 
                        A.ACC_PASS = '{acc_pass}');''')
        recs = cur.fetchall()
        
        Update_Pass_ID()

        tree_children = del_display_tree.get_children()
        for row in tree_children:
            del_display_tree.delete(row)

        tree_id = 1
        for each_rec in recs:
            if tree_id % 2 == 0:
                del_display_tree.insert(parent='', index='end', iid=tree_id, values=each_rec, tags='evenrow')
            else:
                del_display_tree.insert(parent='', index='end', iid=tree_id, values=each_rec, tags='oddrow')
            tree_id += 1
            
        messagebox.showinfo('Password Deleted', 'Selected Password has been successfully deleted.', 
                            parent=del_display_scr)

   
def text_wrap(str_1,length=35):
    return ('\n'.join(textwrap.wrap(str_1,length)))


acc_name = ''
acc_pass = ''
def del_display_pass():
    global acc_name
    global acc_pass
    global del_display_scr

    acc_name = del_ent1.get()
    acc_pass = del_ent2.get()

    cur.execute('SELECT * FROM ACCOUNTS;')
    acc_check = cur.fetchall()

    for i in acc_check:
        if i[1] == del_ent1.get() and i[2] == del_ent2.get():

            cur.execute(f'SELECT * FROM PASSWORDS WHERE ACC_NO = {i[0]};')
            all_pass = cur.fetchall()

            if len(all_pass) == 0:
                messagebox.showinfo('No Passwords',"Your account is empty",parent=del_scr2)
                break
            else:
                del_scr2.destroy()
                del_display_scr = Toplevel(mainscreen)
                del_display_scr.geometry('805x490')

                frame1 = Frame(del_display_scr,width=600,height=600)
                frame1.pack(side=TOP)

                frame2 = Frame(del_display_scr,width=1000,height=180)
                frame2.pack(anchor='w')

                Button(frame2,text='Delete',font=('Malgun Gothic Bold',18),padx=155,pady=10,borderwidth=5,command=del_specific_rec).place(x=5,y=10)
                Button(frame2,text='Cancel',font=('Malgun Gothic Bold',18),padx=140,pady=10,borderwidth=5,command=del_display_scr.destroy).place(x=418,y=10)

                # Widgets in Frame 1
                scrollx = Scrollbar(frame1,orient=HORIZONTAL)
                scrolly = Scrollbar(frame1,orient=VERTICAL)
                
                style = Style()
                style.configure('Treeview',
                rowheight=34,
                font=('Corbel',14),
                foreground='black',
                background='silver',
                fieldbackground="blue")

                style.map('Treeview',background=[('selected','#000000')])
                style.configure('Treeview.Heading',font=('Corbel Bold',20,'bold'))

                global del_display_tree

                del_display_tree = Treeview(frame1,height=10,selectmode='browse',yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)

                del_display_tree.tag_configure('oddrow',background='white')
                del_display_tree.tag_configure('evenrow',background='lightblue')

                scrollx.configure(command=del_display_tree.xview)
                scrolly.configure(command=del_display_tree.yview)

                del_display_tree['columns'] = ('Password ID','Key','Encrypted Password','Password Details','Account No')

                scrollx.pack(side=BOTTOM,fill=X)
                scrolly.pack(side=RIGHT,fill=Y)

                del_display_tree.pack()

                del_display_tree.heading('#0',text='')
                del_display_tree.heading('#1',text='Password ID',anchor='c')
                del_display_tree.heading('#2',text='Key',anchor='c')
                del_display_tree.heading('#3',text='Encrypted Password',anchor='c')
                del_display_tree.heading('#4',text='Password Details',anchor='c')
                del_display_tree.heading('#5',text='Account Number',anchor='c')

                del_display_tree.column('#0',width=0,minwidth=0,stretch=NO)
                del_display_tree.column('#1',width=220,minwidth=0,stretch=False,anchor='c')
                del_display_tree.column('#2',width=160,minwidth=0,anchor='c',stretch=False)
                del_display_tree.column('#3',width=400,minwidth=0,anchor='c',stretch=NO)
                del_display_tree.column('#4',width=270,minwidth=0,anchor='c',stretch=NO)
                del_display_tree.column('#5',width=270,minwidth=0,anchor='c',stretch=False)

            
                for num in range(len(all_pass)):
                    if num % 2 == 0:
                        del_display_tree.insert(parent='',index='end',iid=num,values=(all_pass[num][0],'',all_pass[num][2],all_pass[num][3],all_pass[num][4]),tags=('evenrow',))
                    else:
                        del_display_tree.insert(parent='',index='end',iid=num,values=(all_pass[num][0],'',all_pass[num][2],all_pass[num][3],all_pass[num][4]),tags=('oddrow',))

                messagebox.showinfo('Updated Passwords IDs',"Password IDs have been updated.",parent=del_display_scr)
                break
    else:
        for j in acc_check:
            if j[1] == del_ent1.get() and j[2] != del_ent2.get():
                messagebox.showwarning('Wrong Password','You have entered the wrong password',parent=del_scr2)
                break
        else:
            messagebox.showerror('Error',"Account doesn't exist",parent=del_scr2)
            del_ent1.focus()


def del_Acc():
    global acc_to_del_ent
    global acc_to_del_pass_ent
    global acc_del_win

    Data, No_of_Data = Account_Details()

    if No_of_Data > 0:

        acc_del_win = Toplevel(master=mainscreen)
        acc_del_win.title('Delete Account')
        acc_del_win.geometry('730x312')

        Label(acc_del_win, text='Please fill the following details:', font=('Bahnschrift',20)).place(x=200, y=10)

        Label(acc_del_win, text='Account Name:', font=('Bahnschrift',16)).place(x=30, y=70)
        Label(acc_del_win, text='Account Password:', font=('Bahnschrift',16)).place(x=30, y=115)

        acc_to_del_ent = Entry(acc_del_win, width=30, border=8, font=('Arial 14'))
        acc_to_del_pass_ent = Entry(acc_del_win, width=30, border=8, font=('Arial 14'), show='*')

        acc_to_del_ent.place(x=350, y=70)
        acc_to_del_pass_ent.place(x=350, y=115)

        acc_to_del_ent.focus()
        acc_to_del_ent.bind('<Return>', lambda x: acc_to_del_pass_ent.focus())
        acc_to_del_pass_ent.bind('<Return>', lambda x: delete_account())

        bttn_pass_reveal = Button(acc_del_win, text='Show Password*', font=('Arial', 8), 
                padx=128, pady=2, borderwidth=1, 
                command=lambda: show_pass(entry_wid=acc_to_del_pass_ent,
                                            button_text=bttn_pass_reveal, show_x_coords=127, hide_x_coords=131))
        bttn_pass_reveal.place(x=350, y=150)

        Button(acc_del_win, text='Ok', font=('Malgun Gothic Bold', 18), padx=135, pady=10, borderwidth=4, command=delete_account).place(x=30, y=200)
        Button(acc_del_win, text='Cancel', font=('Malgun Gothic Bold', 18), padx=115, pady=10, borderwidth=4, command=acc_del_win.destroy).place(x=370, y=200)
    else:
        messagebox.showwarning('Zero Accounts', 'You do not have any account created to delete yet.', 
                                parent=del_scr1)


def delete_account():
    global acc_name
    global acc_pass
    global otp_screen
    global start_time
    global entry_otp

    acc_name = acc_to_del_ent.get()
    acc_pass = acc_to_del_pass_ent.get()

    cur.execute('SELECT * FROM ACCOUNTS;')
    pass_details = cur.fetchall()

    if len(acc_name) and len(acc_pass) <= 0:
        messagebox.showinfo('Empty Details', "Please fill in all the details and then press 'Ok'.",
        parent=acc_del_win)
    else:
        for rec in pass_details:
            if rec[1] == acc_name and rec[2] == acc_pass:
                Send_Email(reciever=rec[3], screen=acc_del_win)

                otp_screen = Toplevel(mainscreen)
                otp_screen.title('OTP')
                otp_screen.geometry('370x158')

                start_time = time.ctime()[14:16]

                Label(otp_screen, text='Enter the OTP here:', font=('Arial', 12)).place(x=20, y=30)
                time_left = Label(otp_screen, text=f'OTP will expire in 1 min', font=('Arial', 10))

                entry_otp = Entry(otp_screen, width=24, borderwidth=3, font=('Arial 10'))
                
                entry_otp.place(x=170, y=34)
                time_left.place(x=20, y=50)

                entry_otp.focus()
                entry_otp.bind('<Return>', lambda x: otp_check())

                Button(otp_screen, text='Ok', font=('Arial',16, 'bold'), padx=140, pady=5, border=3, command=otp_check).place(x=20, y= 80)


def otp_check():
    end_time = time.ctime()[14:16]
    otp_to_check = ''.join(otp.split())

    if int(end_time) - int(start_time) > 1:
        entry_otp.config(state=DISABLED)
        messagebox.showerror('Ran out of time', 
                            "Your OTP has expired. You can retry the process from the beginning.", parent=otp_screen) 
    else:
        if otp_to_check == entry_otp.get():
            otp_screen.destroy()

            confirm_delete = messagebox.askyesnocancel('Account Delete Final Confirmation', 
            "If you delete an account, all the passwords stored in the account will also be permanently deleted.Are you sure you want to continue?", parent=acc_del_win)

            if confirm_delete == True:
                cur.execute(f"SELECT ACC_ID FROM ACCOUNTS WHERE ACC_NAME = '{acc_to_del_ent.get()}';")
                acc_id = cur.fetchone()

                cur.execute(f'''DELETE FROM PASSWORDS WHERE ACC_NO = {acc_id[0]};''')
                mycon.commit()

                cur.execute(f"DELETE FROM ACCOUNTS WHERE ACC_NAME = '{acc_to_del_ent.get()}';")
                mycon.commit()

                Update_Pass_ID()

                acc_to_del_ent.delete(0, END)
                acc_to_del_pass_ent.delete(0, END)
                acc_to_del_ent.focus()

                messagebox.showinfo('Account Deleted.', "Account has been deleted successfully.", parent=acc_del_win)
        else:
            messagebox.showerror('Wrong OTP', "Please re-check and enter the right OTP to continue the process.", parent=otp_screen)


def delete_recs():
    global del_scr1

    del_scr1 = Toplevel(mainscreen)
    del_scr1.geometry('480x330')

    Button(del_scr1,text='Delete Password',font=('Malgun Gothic Bold',18),padx=44,pady=10,borderwidth=5,command=del_Pass).place(x=80,y=60)
    Button(del_scr1,text='Delete Account',font=('Malgun Gothic Bold',18),padx=50,pady=10,borderwidth=5,command=del_Acc).place(x=80,y=160)


def update_password():
    pass

def view_passwords():
    pass

def open_screen2():
    global screen2
    screen2 = Toplevel(mainscreen,bg='#F4BBFF')
    screen2.geometry('698x432')

    Label(screen2,text='Password Manager',font=('Georgia Bold',40),bg='#F4BBFF').place(x=95,y=30)

    Button(screen2,text='Add',font=('Malgun Gothic Bold',18),padx=122,pady=8,borderwidth=5,command=add_recs).place(x=20,y=130)
    Button(screen2,text='Delete',font=('Malgun Gothic Bold',18),padx=110,pady=8,borderwidth=5,command=delete_recs).place(x=20,y=230)
    Button(screen2,text='Update',font=('Malgun Gothic Bold',18),padx=102,pady=8,borderwidth=5, command=update_password).place(x=355,y=130)
    Button(screen2,text='View',font=('Malgun Gothic Bold',18),padx=120,pady=8,borderwidth=5, command=view_passwords).place(x=355,y=230)
    Button(screen2,text='Exit',font=('Malgun Gothic Bold',18),padx=294,pady=8,borderwidth=5,command=mainscreen.destroy).place(x=20,y=330)

    # Button(screen2,text='Trials',font=('Arial',30),padx=30,pady=10,command=create_new_acc).place(x=50,y=100)
    # screen2.attributes('-fullscreen',True)


text1 = 'Password Manager \n\n\n\n\n\n Click Anywhere to Continue' 
Button(mainscreen,text=text1,font=('Candara Bold',35),bg='#D19FE8',fg='#3B444B',padx=600,pady=600,command=open_screen2).pack()

# mainscreen.attributes('-fullscreen',True)

mainscreen.mainloop()