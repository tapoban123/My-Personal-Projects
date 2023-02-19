from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3



root = Tk()
root.geometry('800x700')
root.title('Contact Manager')

conn = sqlite3.connect("Contacts_Mng.db")
cursor = conn.cursor()
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS CONTACT_RECS
    (
        CONTACT_ID int(5) PRIMARY KEY,
        CONTACT_FIRST_NAME VARCHAR(40) NOT NULL, 
        CONTACT_LAST_NAME VARCHAR(40) NOT NULL, 
        CONTACT_PH_NO INTEGER(15) NOT NULL,
        CONTACT_ADDRESS TEXT
    );
''')


class Codes_Used_Multiple_Times:
    def __init__(self):
        pass

    def Contacts_Treeview(self,frame,mode,records,height=7):
        global contacts_tree

        scroll_y = Scrollbar(frame,orient=VERTICAL)
        scroll_y.pack(side=RIGHT,fill=Y,expand=True)

        scroll_x = Scrollbar(frame,orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM,fill=X)

        style = ttk.Style()
        style.configure('Treeview',
        font=('Cambria',14),
        rowheight=40)
        style.configure('Treeview.Heading',font=('Constantia',18,'bold'))

        contacts_tree = ttk.Treeview(frame,height=height,selectmode=mode,yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)

        contacts_tree.tag_configure('oddrow',background='#F8F8FF')
        contacts_tree.tag_configure('evenrow',background='#9BDDFF')

        scroll_x.config(command=contacts_tree.xview)
        scroll_y.config(command=contacts_tree.yview)

        contacts_tree['columns'] = ('Contact ID','First Name','Last Name','Phone Number','Address')

        contacts_tree.heading('#0',text='')
        contacts_tree.heading('#1',text='Contact ID',anchor='c')
        contacts_tree.heading('#2',text='First Name',anchor='c')
        contacts_tree.heading('#3',text='Last Name',anchor='c')
        contacts_tree.heading('#4',text='Phone Number',anchor='c')
        contacts_tree.heading('#5',text='Address',anchor='c')

        contacts_tree.column('#0',width=0,minwidth=0,stretch=NO)
        contacts_tree.column('#1',width=150,minwidth=0,stretch=NO,anchor='c')
        contacts_tree.column('#2',width=200,minwidth=0,stretch=NO,anchor='c')
        contacts_tree.column('#3',width=240,minwidth=0,stretch=NO,anchor='c')
        contacts_tree.column('#4',width=260,minwidth=0,stretch=NO,anchor='c')
        contacts_tree.column('#5',width=400,minwidth=0,stretch=NO,anchor='c')

        tree_iid = 1
        for contact in records:
            if tree_iid % 2 == 0:
                contacts_tree.insert(parent='',index='end',iid=tree_iid,values=contact,tags='evenrow')
            else:
                contacts_tree.insert(parent='',index='end',iid=tree_iid,values=contact,tags='oddrow')
            tree_iid += 1

        contacts_tree.pack()

    def Edit_Frame2_UI(self,First_Edit):
        global ent_edit
        global edit_btn_close
        global edit_btn_edit
        global edit_lbl
        global edit_heading

        top_edit.geometry('800x526')

        if First_Edit == True:
            btn_update.place_forget()
            btn_close_2.place_forget()
            btn_edit_2.place_forget()
            lbl_heading_selectedcon.place_forget()
            lbl_con_id.place_forget()
            lbl_con_id_value.place_forget()
            lbl_fname.place_forget()
            lbl_lname.place_forget()
            lbl_phno.place_forget()
            lbl_address.place_forget()
            ent_edit_fname.place_forget()
            ent_edit_lname.place_forget()
            ent_edit_phno.place_forget()
            ent_edit_address.place_forget()

        edit_heading = Label(edit_frame2,text='Please fill the following detail or select the contact you want to edit',font=('Corbel',20,'bold'),bg='#99BADD',wraplength=640)
        edit_lbl = Label(edit_frame2,text='Enter Contact ID:',font=('Corbel',16,'bold'),bg='#99BADD')

        ent_edit = Entry(edit_frame2,width=30,borderwidth=5,font=('Arial 14'),bg='#DCDCDC')

        ent_edit.focus()
        ent_edit.bind('<Return>',lambda x: edit_specific_contact())

        edit_btn_close = Button(edit_frame2,text='Close',font=('Malgun Gothic Bold',18),padx=140,pady=10,borderwidth=5,bg='#E6E6FA',command=top_edit.destroy)
        edit_btn_edit = Button(edit_frame2,text='Edit',font=('Malgun Gothic Bold',18),padx=140,pady=10,borderwidth=5,bg='#E6E6FA',command=edit_specific_contact)

        edit_heading.place(x=100,y=10)
        edit_lbl.place(x=140,y=100)
        ent_edit.place(x=340,y=100)
        edit_btn_close.place(x=25,y=170)
        edit_btn_edit.place(x=420,y=170)

    def Edit_Contact_UI(self,*VALUES):
        global rec
        global lbl_heading_selectedcon
        global lbl_con_id
        global lbl_con_id_value
        global lbl_fname
        global lbl_lname
        global lbl_phno
        global lbl_address
        global ent_edit_fname
        global ent_edit_lname
        global ent_edit_phno
        global ent_edit_address
        global btn_update
        global btn_edit_2
        global btn_close_2

        top_edit.geometry('800x630')

        edit_lbl.place_forget()
        edit_heading.place_forget()
        ent_edit.place_forget()
        edit_btn_edit.place_forget()
        edit_btn_close.place_forget()

        btn_close_2 = Button(edit_frame2,text='Close',font=('Malgun Gothic Bold',14),padx=150,pady=3,borderwidth=3,bg='#E6E6FA',command=top_edit.destroy)
        btn_edit_2 = Button(edit_frame2,text='Edit',font=('Malgun Gothic Bold',14),padx=156,pady=3,borderwidth=3,bg='#E6E6FA',command=edit_specific_contact)

        btn_close_2.place(x=25,y=320)
        btn_edit_2.place(x=412,y=320)

        lbl_heading_selectedcon = Label(edit_frame2,text='Details of the Selected Contact',font=('Candara Bold',20),bg='#99BADD')
        lbl_con_id = Label(edit_frame2,text='Contact ID:',font=('Candara Bold',16),bg='#99BADD')
        lbl_con_id_value = Label(edit_frame2,text=f'{VALUES[0]}',font=('Arial',14),padx=160,relief=SUNKEN,bg='#DCDCDC',borderwidth=4)

        lbl_fname = Label(edit_frame2,text='First Name:',font=('Candara Bold',16),bg='#99BADD')
        lbl_lname = Label(edit_frame2,text='Last Name:',font=('Candara Bold',16),bg='#99BADD')
        lbl_phno = Label(edit_frame2,text='Phone Number:',font=('Candara Bold',16),bg='#99BADD')
        lbl_address = Label(edit_frame2,text='Address:',font=('Candara Bold',16),bg='#99BADD')

        ent_edit_fname = Entry(edit_frame2,width=30,borderwidth=4,font=('Arial 15'),bg='#DCDCDC')
        ent_edit_lname = Entry(edit_frame2,width=30,borderwidth=4,font=('Arial 15'),bg='#DCDCDC')
        ent_edit_phno = Entry(edit_frame2,width=30,borderwidth=4,font=('Arial 15'),bg='#DCDCDC')
        ent_edit_address = Entry(edit_frame2,width=30,borderwidth=4,font=('Arial 15'),bg='#DCDCDC')

        lbl_heading_selectedcon.place(x=220,y=10)
        lbl_con_id.place(x=100,y=70)
        lbl_con_id_value.place(x=350,y=70)
        lbl_fname.place(x=100,y=115)
        lbl_lname.place(x=100,y=145)
        lbl_phno.place(x=100,y=175)
        lbl_address.place(x=100,y=205)

        ent_edit_fname.place(x=350,y=115)
        ent_edit_lname.place(x=350,y=145)
        ent_edit_phno.place(x=350,y=175)
        ent_edit_address.place(x=350,y=205)

        ent_edit_fname.insert(0,VALUES[1])
        ent_edit_lname.insert(0,VALUES[2])
        ent_edit_phno.insert(0,VALUES[3])
        ent_edit_address.insert(0,VALUES[4])

        ent_edit_fname.focus()
        ent_edit_fname.bind('<Return>',lambda x: ent_edit_lname.focus())
        ent_edit_lname.bind('<Return>',lambda x: ent_edit_phno.focus())
        ent_edit_phno.bind('<Return>',lambda x: ent_edit_address.focus())
        ent_edit_address.bind('<Return>',lambda x: Update_with_new(VALUES[5]))

        btn_update = Button(edit_frame2,text='Update',font=('Malgun Gothic Bold',14),padx=334,pady=3,borderwidth=3,bg='#E6E6FA',command=lambda: Update_with_new(VALUES[5]))

        btn_update.place(x=25,y=260)

    def Del_Contact_Process(self):
        for contact in contacts_to_del:
            contacts_tree.delete(contact)

        con_index = 0
        for update in range(len(contacts_to_del)):
            cursor.execute(F'''DELETE FROM CONTACT_RECS WHERE CONTACT_ID = {contacts_to_del[con_index]};''')
            conn.commit()

            con_index += 1

        messagebox.showinfo('Contact Deleted',"The selected contact(s) have been deleted",parent=top_delete)

        cursor.execute('SELECT * FROM CONTACT_RECS;')
        ALL_CONTACTS_NEW = cursor.fetchall()

        NEW_ID = 1
        for rec in ALL_CONTACTS_NEW:
            cursor.execute(f"UPDATE CONTACT_RECS SET CONTACT_ID = {NEW_ID} WHERE CONTACT_ID =  {rec[0]}")
            conn.commit()

            NEW_ID += 1


Class_Instance = Codes_Used_Multiple_Times()


def first_UI_scr():
    global top

    top = Toplevel(root,bg='#F0DC82')
    top.geometry('700x400')
    top.title('Contact Manager')

    Label(top,text='Contact Manager',font=('Segoe UI Black',30),bg='#F0DC82').place(x=180,y=10)

    Button(top, text="Add Contact",font=('Malgun Gothic Bold',18),padx=52,pady=5,borderwidth=5,command=fill_details,bg='#F0EAD6').place(x=20,y=100)

    Button(top, text="Delete Contact",font=('Malgun Gothic Bold',18),padx=40,pady=5,borderwidth=5,command=delete_rec,bg='#F0EAD6').place(x=20,y=200)

    Button(top, text="Edit Contact",font=('Malgun Gothic Bold',18),padx=56,pady=5,borderwidth=5,command=edit_rec,bg='#F0EAD6').place(x=400,y=100)

    Button(top, text="View Contacts",font=('Malgun Gothic Bold',18),padx=45,pady=5,borderwidth=5,command=view_all,bg='#F0EAD6').place(x=400,y=200)

    Button(top,text='Exit',font=('Malgun Gothic Bold',18),padx=296,pady=5,borderwidth=5,command=lambda:root.destroy(),bg='#F0EAD6').place(x=20,y=300)


def add_details_to_db():
    if len(entry_fname.get()) == len(entry_lname.get()) == len(entry_phno.get()) == len(entry_address.get()) == 0:
        messagebox.showerror('Unfilled Contact Details',"You need to fill up the details first and then press 'Enter' or 'OK'",parent=top_add)
        entry_fname.focus()
    elif len(entry_phno.get()) == 0:
        messagebox.showerror('Empty Phone Number',"You must enter the Phone Number of the contact.",parent=top_add)
        entry_phno.focus()
    else:
        try:
            cursor.execute('SELECT * FROM CONTACT_RECS;')
            NO_OF_RECS = cursor.fetchall()

            entry_list = [entry_fname, entry_lname, entry_phno,entry_address]

            entry_list_values = {}

            for entry in entry_list:
                if len(entry.get()) == 0:
                    entry_list_values[entry] = 'NULL'
                else:
                    entry_list_values[entry] = entry.get().strip()

            cursor.execute(f"INSERT INTO CONTACT_RECS VALUES({len(NO_OF_RECS)+1},'{entry_list_values[entry_fname]}','{entry_list_values[entry_lname]}',{entry_list_values[entry_phno]},'{entry_list_values[entry_address]}');")
            conn.commit()

            entry_fname.delete(0,END)
            entry_lname.delete(0,END)
            entry_phno.delete(0,END)
            entry_address.delete(0,END)

            messagebox.showinfo('Contact Saved',"Contact has been saved. You can view, edit or delete the contact anytime you want.",parent=top_add)

            entry_fname.focus()
        except:
            messagebox.showerror('Invalid Data',"Please re-check the details you entered and then try again.",parent=top_add)


def  fill_details():
    global top_add
    global entry_fname
    global entry_lname
    global entry_phno
    global entry_address

    top_add = Toplevel(root,bg='#FBEC5D')
    top_add.title('Add a Contact')
    top_add.geometry('785x435')

    Label(top_add,text='Please fill the following Details',font=('Cambria Bold',25),bg='#FBEC5D').place(x=180,y=20)

    Label(top_add,text='First Name:',font=('Cambria',18),bg='#FBEC5D').place(x=50,y=100)
    Label(top_add,text='Last Name:',font=('Cambria',18),bg='#FBEC5D').place(x=50,y=140)
    Label(top_add,text='Phone Number:',font=('Cambria',18),bg='#FBEC5D').place(x=50,y=180)
    Label(top_add,text='Address:',font=('Cambria',18),bg='#FBEC5D').place(x=50,y=220)

    entry_fname = Entry(top_add,width=30,borderwidth=8,font=('Arial',15),bg='#DCDCDC')
    entry_lname = Entry(top_add,width=30,borderwidth=8,font=('Arial',15),bg='#DCDCDC')
    entry_phno = Entry(top_add,width=30,borderwidth=8,font=('Arial',15),bg='#DCDCDC')
    entry_address = Entry(top_add,width=30,borderwidth=8,font=('Arial',15),bg='#DCDCDC')

    entry_fname.place(x=390,y=100)
    entry_lname.place(x=390,y=140)
    entry_phno.place(x=390,y=180)
    entry_address.place(x=390,y=220)

    entry_fname.focus()
    entry_fname.bind('<Return>',lambda x: entry_lname.focus())
    entry_lname.bind('<Return>',lambda x: entry_phno.focus())
    entry_phno.bind('<Return>',lambda x: entry_address.focus())
    entry_address.bind('<Return>',lambda x: add_details_to_db())

    Button(top_add,text='Close',font=('Malgun Gothic Bold',18),padx=120,pady=10,borderwidth=5,bg='#EEE8AA',command=top_add.destroy).place(x=50,y=300)
    Button(top_add,text='OK',font=('Malgun Gothic Bold',18),padx=143,pady=10,borderwidth=5,bg='#EEE8AA',command=add_details_to_db).place(x=390,y=300)


def del_selected_contact():
    global contacts_to_del

    contacts_to_del = contacts_tree.selection()
    del_confirmation = lambda x: messagebox.askyesno("Delete Contact Confirmation",f"Are you sure you want to delete the selected {x}?",parent=top_delete)

    if len(contacts_to_del) > 1:
        if del_confirmation('contacts') == True:
            Class_Instance.Del_Contact_Process()

    elif len(contacts_to_del) == 1:
        if del_confirmation('contact') == True:
            Class_Instance.Del_Contact_Process()

    elif len(contacts_to_del) == 0:
        messagebox.showinfo('No Contact Selected',"You need to select the contact(s) you want to delete and then click the button.",parent=top_delete)


def delete_rec():
    global top_delete

    cursor.execute('SELECT * FROM CONTACT_RECS;')
    DEL_DATA = cursor.fetchall()

    if len(DEL_DATA) == 0:
        messagebox.showwarning('No Contact Present',"You cannot delete contact unless you add one.",parent=top)
    else:
        top_delete = Toplevel(root)
        top_delete.title('Delete Contact')
        top_delete.geometry('800x422')

        del_frame = Frame(top_delete,height=600,width=600)
        del_frame.pack(side=TOP)

        del_frame2 = Frame(top_delete,width=1000,height=600,bg='#99BADD')
        del_frame2.pack(side=TOP,anchor='w')

        Button(del_frame2,text='Delete Selected',font=('Malgun Gothic Bold',18),padx=105,pady=10,borderwidth=4,bg='#E6E6FA',command=del_selected_contact).place(x=5,y=10)
        Button(del_frame2,text='Close',font=('Malgun Gothic Bold',18),padx=145,pady=10,borderwidth=4,bg='#E6E6FA',command=top_delete.destroy).place(x=420,y=10)

        Class_Instance.Contacts_Treeview(del_frame,'extended',DEL_DATA)

        messagebox.showinfo('Contact ID(s) Updated','Contact ID(s) have been updated',parent=top_delete)


def Update_with_new(con_ID):
    try:
        cursor.execute(f'''UPDATE CONTACT_RECS SET 
        CONTACT_FIRST_NAME = '{ent_edit_fname.get().strip()}', 
        CONTACT_LAST_NAME = '{ent_edit_lname.get().strip()}',
        CONTACT_PH_NO = {ent_edit_phno.get()},
        CONTACT_ADDRESS = '{ent_edit_address.get().strip()}'
        WHERE CONTACT_ID = {con_ID}; ''')
        conn.commit()

        for all_recs in contacts_tree.get_children():
            contacts_tree.delete(all_recs)

        cursor.execute(f'SELECT * FROM CONTACT_RECS WHERE CONTACT_ID = {con_ID};')
        new_rec = cursor.fetchone()

        contacts_tree.insert(parent='',index='end',iid=1,values=new_rec)
        edited_iid = 2

        cursor.execute(F"SELECT * FROM CONTACT_RECS WHERE CONTACT_ID != {con_ID};")
        recs_edited  = cursor.fetchall()

        for row in recs_edited:
            if edited_iid % 2 == 0:
                contacts_tree.insert(parent='',index='end',iid=edited_iid,values=row,tags='evenrow')
            else:
                contacts_tree.insert(parent='',index='end',iid=edited_iid,values=row,tags='oddrow')
            edited_iid += 1

        messagebox.showinfo('Contact Updated',"Contact has been updated",parent=top_edit)

        Class_Instance.Edit_Frame2_UI(True)
    except:
        messagebox.showerror("Invalid Data","Please check the data you entered and then try again.",parent=top_edit)


def edit_specific_contact():
    global rec

    if len(contacts_tree.selection()) == 0 and len(ent_edit.get()) > 0:
        if ent_edit.get() in contacts_tree.get_children():
            cursor.execute(f'SELECT * FROM CONTACT_RECS WHERE CONTACT_ID = {ent_edit.get()};')
            user_wish_rec = cursor.fetchone()

            Class_Instance.Edit_Contact_UI(user_wish_rec[0],user_wish_rec[1],user_wish_rec[2],user_wish_rec[3],user_wish_rec[4],ent_edit.get())
        else:
            messagebox.showwarning('Contact Not Found',"Contact does not exist.",parent=top_edit)

    elif len(contacts_tree.selection()) > 0 and len(ent_edit.get()) == 0:
        rec_foci = contacts_tree.focus()
        rec = contacts_tree.item(rec_foci,'values')

        Class_Instance.Edit_Contact_UI(rec[0],rec[1],rec[2],rec[3],rec[4],rec[0])

    else:
        messagebox.showinfo('No Specific Contact Selected',"Please select a specific contact or enter the 'Contact ID' of the contact you want to edit and then click on 'Edit'.",parent=top_edit)


def edit_rec():
    global top_edit
    global edit_frame2
    global ent_edit
    global edit_btn_close
    global edit_btn_edit
    global edit_lbl
    global edit_heading

    cursor.execute('SELECT * FROM CONTACT_RECS;')
    EDIT_RECS = cursor.fetchall()

    if len(EDIT_RECS) == 0:
        messagebox.showwarning('No Contacts to Edit',"You cannot access this feature untill you add a contact.",parent=top)
    else:
        top_edit = Toplevel(root)
        top_edit.title('Edit a Contact')
        top_edit.geometry('800x526')

        edit_frame = Frame(top_edit,height=600,width=1000)
        edit_frame.pack(side=TOP)

        edit_frame2 = Frame(top_edit,width=1000,height=600,bg='#99BADD')
        edit_frame2.pack(side=TOP,anchor='w')

        Class_Instance.Edit_Frame2_UI(False)

        Class_Instance.Contacts_Treeview(edit_frame,'browse',EDIT_RECS,5)


def search_contact():
    try:
        if len(search_fname.get()) > 0 and (len(search_lname.get()) == len(search_phno.get()) == 0):
            cursor.execute(F"SELECT * FROM CONTACT_RECS WHERE CONTACT_FIRST_NAME LIKE '{search_fname.get().strip()}%';")
            fname_data = cursor.fetchall()

            for rec in contacts_tree.get_children():
                contacts_tree.delete(rec)

            fname_iid = 1
            for data in fname_data:
                if fname_iid % 2 == 0:
                    contacts_tree.insert(parent='',index='end',iid=fname_iid,values=data,tags='evenrow')
                else:
                    contacts_tree.insert(parent='',index='end',iid=fname_iid,values=data,tags='oddrow')
                fname_iid += 1

        elif len(search_lname.get()) > 0 and (len(search_fname.get()) == len(search_phno.get()) == 0):
            cursor.execute(F"SELECT * FROM CONTACT_RECS WHERE CONTACT_LAST_NAME LIKE '{search_lname.get().strip()}%';")
            lname_data = cursor.fetchall()

            for rec2 in contacts_tree.get_children():
                contacts_tree.delete(rec2)

            lname_iid = 1
            for data2 in lname_data:
                if lname_iid % 2 == 0:
                    contacts_tree.insert(parent='',index='end',iid=lname_iid,values=data2,tags='evenrow')
                else:
                    contacts_tree.insert(parent='',index='end',iid=lname_iid,values=data2,tags='oddrow')
                lname_iid += 1

        elif len(search_phno.get()) > 0 and (len(search_fname.get()) == len(search_lname.get()) == 0):
            cursor.execute(F"SELECT * FROM CONTACT_RECS WHERE CONTACT_PH_NO LIKE '{int(search_phno.get())}%';")
            phno_data = cursor.fetchall()

            for rec_phno in contacts_tree.get_children():
                contacts_tree.delete(rec_phno)

            phno_iid = 1
            for data3 in phno_data:
                if phno_iid % 2 == 0:
                    contacts_tree.insert(parent='',index='end',iid=phno_iid,values=data3,tags='evenrow')
                else:
                    contacts_tree.insert(parent='',index='end',iid=phno_iid,values=data3,tags='oddrow')
                phno_iid += 1

        elif (len(search_fname.get()) == len(search_lname.get()) == len(search_phno.get()) == 0):
            cursor.execute('SELECT * FROM CONTACT_RECS;')
            ALL_DATA = cursor.fetchall()

            for s_recs in contacts_tree.get_children():
                contacts_tree.delete(s_recs)

            all_iid = 1
            for all_recs in ALL_DATA:
                if all_iid  % 2 == 0:
                    contacts_tree.insert(parent='',index='end',iid=all_iid,values=all_recs,tags='evenrow')
                else:
                    contacts_tree.insert(parent='',index='end',iid=all_iid,values=all_recs,tags='oddrow')
                all_iid += 1

        elif (len(search_fname.get()) > 0 and len(search_lname.get())) > 0 and len(search_phno.get()) == 0:
            cursor.execute(F"SELECT * FROM CONTACT_RECS WHERE CONTACT_FIRST_NAME LIKE '{search_fname.get().strip()}%' and CONTACT_LAST_NAME LIKE '{search_lname.get().strip()}%';")
            fname_lname = cursor.fetchall()

            for recfl in contacts_tree.get_children():
                contacts_tree.delete(recfl)

            fl_iid = 1
            for data4 in fname_lname:
                if fl_iid % 2 == 0:
                    contacts_tree.insert(parent='',index='end',iid=fl_iid,values=data4,tags='evenrow')
                else:
                    contacts_tree.insert(parent='',index='end',iid=fl_iid,values=data4,tags='oddrow')
                fl_iid += 1

        elif len(search_fname.get()) == 0 and (len(search_lname.get()) > 0 and len(search_phno.get()) > 0):
            cursor.execute(f"SELECT * FROM CONTACT_RECS WHERE CONTACT_LAST_NAME LIKE '{search_lname.get().strip()}%' and CONTACT_PH_NO LIKE '{search_phno.get()}%';")
            phno_lname = cursor.fetchall()

            for recphl in contacts_tree.get_children():
                contacts_tree.delete(recphl)

            phl_iid = 1
            for data5 in phno_lname:
                if phl_iid % 2 == 0:
                    contacts_tree.insert(parent='',index='end',iid=phl_iid,values=data5,tags='evenrow')
                else:
                    contacts_tree.insert(parent='',index='end',iid=phl_iid,values=data5,tags='oddrow')
                phl_iid += 1

        elif len(search_fname.get()) > 0 and len(search_lname.get()) == 0 and len(search_phno.get()) > 0:
            cursor.execute(f"SELECT * FROM CONTACT_RECS WHERE CONTACT_FIRST_NAME LIKE '{search_fname.get().strip()}%' and CONTACT_PH_NO LIKE '{search_phno.get()}%';")
            fphno = cursor.fetchall()

            for fph in contacts_tree.get_children():
                contacts_tree.delete(fph)

            fph_iid = 1
            for data6 in fphno:
                if fph_iid % 2 == 0:
                    contacts_tree.insert(parent='',index='end',iid=fph_iid,values=data6,tags='evenrow')
                else:
                    contacts_tree.insert(parent='',index='end',iid=fph_iid,values=data6,tags='oddrow')
                fph_iid += 1

        elif len(search_fname.get()) > 0 and len(search_lname.get()) > 0 and len(search_phno.get()) > 0:
            cursor.execute(f"SELECT * FROM CONTACT_RECS WHERE CONTACT_FIRST_NAME LIKE '{search_fname.get().strip()}%' AND CONTACT_LAST_NAME LIKE '{search_lname.get().strip()}%' AND CONTACT_PH_NO LIKE '{search_phno.get()}%';")
            fname_lname_phno = cursor.fetchall()

            for flphno in contacts_tree.get_children():
                contacts_tree.delete(flphno)

            fname_lname_phno_iid = 1
            for data7 in fname_lname_phno:
                if fname_lname_phno_iid % 2 == 0:
                    contacts_tree.insert(parent='',index='end',iid=fname_lname_phno_iid,values=data7,tags='evenrow')
                else:
                    contacts_tree.insert(parent='',index='end',iid=fname_lname_phno_iid,values=data7,tags='oddrow')
                fname_lname_phno_iid += 1

    except:
        messagebox.showwarning('Wrong Search Details',"No Contact found by the search details you entered",parent=top_view_all)


def view_all():
    global search_fname
    global search_lname
    global search_phno
    global contacts_tree
    global top_view_all

    cursor.execute('SELECT * FROM CONTACT_RECS;')
    CONTACTS = cursor.fetchall()

    if len(CONTACTS) == 0:
        user_wish = messagebox.askyesno('No Contact to Display',"You do not have any contact recorded to display.Do you want ot add a contact now?",parent=top)
        if user_wish == True:
            fill_details()

    else:
        top_view_all = Toplevel(root,bg='#99BADD')
        top_view_all.title('All Contacts')
        top_view_all.geometry('780x670')

        frame1 = Frame(top_view_all,width=600)
        frame1.pack(side=TOP,anchor='n')

        frame2 = Frame(top_view_all,height=400,width=800,bg='#A1CAF1')
        frame2.pack(side=LEFT,anchor='e')

        Label(frame2,text='Search Record',font=('Calibri',20,'bold'),bg='#A1CAF1').place(x=320,y=5)
        Label(frame2,text='First Name:',font=('Calibri',16,'bold'),bg='#A1CAF1').place(x=60,y=70)
        Label(frame2,text='Last Name:',font=('Calibri',16,'bold'),bg='#A1CAF1').place(x=60,y=110)
        Label(frame2,text='Phone Number:',font=('Calibri',16,'bold'),bg='#A1CAF1').place(x=60,y=150)

        search_fname = Entry(frame2,width=30,borderwidth=8,font=('Arial 14'),bg='#DCDCDC')
        search_lname = Entry(frame2,width=30,borderwidth=8,font=('Arial 14'),bg='#DCDCDC')
        search_phno = Entry(frame2,width=30,borderwidth=8,font=('Arial 14'),bg='#DCDCDC')

        search_fname.place(x=340,y=70)
        search_lname.place(x=340,y=110)
        search_phno.place(x=340,y=150)

        search_fname.focus()
        search_fname.bind('<Return>',lambda x: search_lname.focus())
        search_lname.bind('<Return>',lambda x: search_phno.focus())
        search_phno.bind('<Return>',lambda x: search_contact())

        Button(frame2,text='Search',font=('Malgun Gothic Bold',18),padx=120,pady=10,borderwidth=4,bg='#E6E6FA',command=search_contact).place(x=30,y=230)
        Button(frame2,text='Close',font=('Malgun Gothic Bold',18),padx=130,pady=10,borderwidth=4,bg='#E6E6FA',command=top_view_all.destroy).place(x=400,y=230)

        Class_Instance.Contacts_Treeview(frame1,'none',CONTACTS)


text1 = "Contact Manager \n\n\n\n\n\n\nClick Anywhere to Continue"

myButton_begin = Button(root,text=text1,font=('Calibri',35),bg='#BF94E4',padx=600,pady=600,command=first_UI_scr)
myButton_begin.pack()

root.mainloop()
