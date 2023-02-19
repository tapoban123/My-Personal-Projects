import tkinter as tkGUI
from tkinter import *
from tkinter import font 
import sqlite3
from tkinter import messagebox
from PIL import Image,ImageTk
import datetime


root = tkGUI.Tk()
root.title("Hotel Management System")
root.geometry('1200x780')
myfont = font.Font(size=20)
conn = sqlite3.connect("Hotel_Management_DB.db")
cursor = sqlite3.Cursor(conn)

cursor.execute('''create table if not exists hotel_mng_sys
(
    SL_NO int(5) PRIMARY KEY,
    NAME varchar(25),
    PH_NO int(15), 
    ADDRESS varchar(100), 
    ARRIVAL varchar(10),
    CHECK_IN varchar(8),
    CHECK_OUT varchar(8),
    CAR_NO int(10), 
    ROOM_NO int(5) 
); 
''')

# // cursor.execute("Drop table hotel_mng_sys;")

def next_entry(entry_widno):
    entry_wid_list[entry_widno].focus()


def newroot():
    global root2
    root2 = tkGUI.Toplevel(root,bg='#E9D66B')
    root2.title('Fill the Details')
    root2.geometry('850x752')

    global entrywid1
    global entrywid2
    global entrywid3
    global entrywid4
    global entrywid5
    global entrywid6
    global entrywid7
    global entrywid8
    global entrywid9
    global entry_wid_list

    Label(root2,text='Details of the Guest: ',font=('Calibri Bold',25),bg='#E9D66B',fg='#000000').place(x=10,y=10)
    Label(root2,text="Guest ID:",font=('Calibri',20),bg='#E9D66B',fg='#000000').place(x=10,y=50)
    Label(root2,text='Name:',font=('Calibri',20),bg='#E9D66B',fg='#000000').place(x=10,y=90)
    Label(root2,text='Phone No.:',font=('Calibri',20),bg='#E9D66B',fg='#000000').place(x=10,y=130)
    tkGUI.Label(root2,text='Address:',font=('Calibri',20),bg='#E9D66B',fg='#000000').place(x=10,y=170)
    tkGUI.Label(root2,text='Date of Arrival:',font=('Calibri',20),bg='#E9D66B',fg='#000000').place(x=10,y=210)
    tkGUI.Label(root2,text='Time of Checking In:',font=('Calibri',20),bg='#E9D66B',fg='#000000').place(x=10,y=250)
    Label(root2,text='Time of Checking Out:',font=('Calibri',20),bg='#E9D66B',fg='#000000').place(x=10,y=290)
    Label(root2,text='Car No:',font=('Calibri',20),bg='#E9D66B',fg='#000000').place(x=10,y=330)
    Label(root2,text='Room No:',font=('Calibri',20),bg='#E9D66B',fg='#000000').place(x=10,y=370)

    entrywid1 = Entry(root2,width=30,border=5,font=("Arial 14"),bg='#DCDCDC')
    entrywid2 = Entry(root2,width=30,border=5,font=('Arial 14'),bg='#DCDCDC')
    entrywid3 = Entry(root2,width=30,border=5,font=('Arial 14'),bg='#DCDCDC')
    entrywid4 = Entry(root2,width=30,border=5,font=('Arial 14'),bg='#DCDCDC')
    entrywid5 = Entry(root2,width=30,border=5,font=('Arial 14'),bg='#DCDCDC')
    entrywid6 = Entry(root2,width=30,border=5,font=('Arial 14'),bg='#DCDCDC')
    entrywid7 = Entry(root2,width=30,border=5,font=('Arial 14'),bg='#DCDCDC')
    entrywid8 = Entry(root2,width=30,border=5,font=('Arial 14'),bg='#DCDCDC')
    entrywid9 = Entry(root2,width=30,border=5,font=('Arial 14'),bg='#DCDCDC')

    entry_wid_list = [entrywid3,entrywid4,entrywid5,entrywid6,entrywid7,entrywid8,entrywid9]

    entrywid1.bind('<Return>',lambda e: entrywid2.focus())
    entrywid2.bind('<Return>',lambda e: next_entry(0))
    entrywid3.bind('<Return>',lambda e: next_entry(1))
    entrywid4.bind('<Return>',lambda e: next_entry(2))
    entrywid5.bind('<Return>',lambda e: next_entry(3))
    entrywid6.bind('<Return>',lambda e: next_entry(4))
    entrywid7.bind('<Return>',lambda e: next_entry(5))
    entrywid8.bind('<Return>',lambda e: next_entry(6))
    entrywid9.bind('<Return>',lambda e: add_info())

    cursor.execute('Select * from hotel_mng_sys;')
    all_data = cursor.fetchall()
    if len(all_data) == len(all_data) % 10:
        entrywid1.insert(0,f"0{len(all_data)+1}")
    else:
        entrywid1.insert(0,len(all_data)+1)

    date = datetime.datetime.now()
    entrywid5.insert(0,date.date())
    time = (str(date.time()))[0:8]
    entrywid6.insert(0,time)
    entrywid7.insert(0,'00:00:00')

    entrywid1.place(x=350,y=60)
    entrywid2.place(x=350,y=100)
    entrywid3.place(x=350,y=140)
    entrywid4.place(x=350,y=178)
    entrywid5.place(x=350,y=218)
    entrywid6.place(x=350,y=255)
    entrywid7.place(x=350,y=296)
    entrywid8.place(x=350,y=336)
    entrywid9.place(x=350,y=375)

    entrywid2.focus()

    Button(root2,text='Add',font=('Malgun Gothic Bold',18),bg='#F2F3F4',borderwidth=8,padx=96,pady=10,command=add_info).place(x=10,y=445)
    
    Button(root2,text='Edit',font=('Malgun Gothic Bold',18),bg='#F2F3F4',borderwidth=8,padx=100,pady=10,command=update_info).place(x=285,y=445)

    Button(root2,text="Delete",font=('Malgun Gothic Bold',18),fg='red',bg='#F2F3F4',borderwidth=8,padx=85,pady=10,command=delete_info).place(x=565,y=445)

    Button(root2,text='Show All Records',font=('Malgun Gothic Bold',18),bg='#F2F3F4',borderwidth=8,padx=93,pady=20,command=show_all_rec).place(x=10,y=540)

    Button(root2,text='Search Record',font=('Malgun Gothic Bold',18),bg='#F2F3F4',borderwidth=8,padx=105,pady=20,command=search_rec).place(x=435,y=540)

    Button(root2,text='Close',font=('Malgun Gothic Bold',18),bg='#F2F3F4',borderwidth=8,padx=369,pady=10,command=    root.quit).place(x=10,y=655)


def add_info():
    global entry_wid_dict
    entry_wid_dict = {'Slno':entrywid1.get(),'Name':entrywid2.get(),'Ph no':entrywid3.get(),'Address':entrywid4.get(),'Date of Arrival':entrywid5.get(),'Check in':entrywid6.get(),'Check out':entrywid7.get(),'Car no':entrywid8.get(),'Room no':entrywid9.get()}

    global name
    name = ''.join(entry_wid_dict['Name'].split())

    if entry_wid_dict['Room no'].isalnum() == name.isalnum() == entry_wid_dict['Ph no'].isalnum() ==  entry_wid_dict['Address'].isalnum() == entry_wid_dict['Date of Arrival'].isalnum() == entry_wid_dict['Check in'].isalnum() == entry_wid_dict['Check out'].isalnum() == entry_wid_dict['Car no'].isalnum() == False:
        messagebox.showwarning('Warning!',"Oops! Looks like you haven't filled all the necessary details.",parent=root2)
        
    else:
        cursor.execute(f"INSERT INTO hotel_mng_sys VALUES({entry_wid_dict['Slno'].strip()},'{entry_wid_dict['Name'].title().strip()}',{entry_wid_dict['Ph no'].strip()},'{entry_wid_dict['Address'].title().strip()}','{entry_wid_dict['Date of Arrival'].strip()}','{entry_wid_dict['Check in'].strip()}','{entry_wid_dict['Check out'].strip()}',{entry_wid_dict['Car no'].strip()},{entry_wid_dict['Room no'].strip()});")

        conn.commit()
        entrywid1.delete(0,END)
        entrywid2.delete(0,END)
        entrywid3.delete(0,END)
        entrywid4.delete(0,END)
        entrywid5.delete(0,END)
        entrywid6.delete(0,END)
        entrywid7.delete(0,END)
        entrywid8.delete(0,END)
        entrywid9.delete(0,END) 

        cursor.execute('Select * from hotel_mng_sys;')
        all_data = cursor.fetchall()
        if len(all_data) == len(all_data) % 10:
            entrywid1.insert(0,f"0{len(all_data)+1}")
        else:
            entrywid1.insert(0,len(all_data)+1)

        date2 = datetime.datetime.now()
        entrywid5.insert(0,date2.date())
        time2 = (str(date2.time()))[0:8]
        entrywid6.insert(0,time2)
        entrywid7.insert(0,'00:00:00')
        
        entrywid2.focus()


def update_info():
    global root7
    global entrywid1r7

    root7 = Toplevel(root,bg='#8A2BE2')
    root7.title('Update Record')
    root7.geometry('500x175')

    Label(root7,text="Fill the detail and press Enter or 'OK'",font=('Italic Bold',18),bg='#8A2BE2',fg='#E7FEFF').place(x=10,y=10)
    Label(root7,text='Enter Guest ID:',font=('Calibri Bold',14),bg='#8A2BE2',fg='#E7FEFF').place(x=10,y=54)

    entrywid1r7 = Entry(root7,width=18,border=5,font=('Arial 14'))
    entrywid1r7.place(x=200,y=54)

    entrywid1r7.focus()
    entrywid1r7.bind('<Return>',lambda e: ok_update())

    Button(root7,text='OK',font=('Malgun Gothic Bold',12),border=8,padx=215,pady=5,command=ok_update).place(x=10,y=100)


def ok_update():
    global entrywid2r7
    global entrywid3r7
    global entrywid4r7
    global entrywid5r7
    global entrywid6r7
    global entrywid7r7
    global entrywid8r7
    global entrywid9r7
    global update_rec

    if entrywid1r7.get().strip().isalnum() != True:
        messagebox.showwarning('No Value Entered','Enter a Value to view and edit the Records',parent=root7)
    elif entrywid1r7.get().strip().isalnum() == True:
        cursor.execute(f'SELECT * FROM hotel_mng_sys where SL_NO = {entrywid1r7.get()};')
        update_rec = cursor.fetchall()

        if update_rec == []:
            messagebox.showerror('Invalid Guest ID',f"Guest ID: {entrywid1r7.get()} doesnt't exist",parent=root7)
        else:
            for rec in update_rec:
                root7.geometry('500x600')

                Label(root7,text='Name:',font=('Calibri Bold',18),bg='#8A2BE2',fg='#E7FEFF').place(x=10,y=190)
                Label(root7,text='Phone Number:',font=('Calibri Bold',18),bg='#8A2BE2',fg='#E7FEFF').place(x=10,y=230)
                Label(root7,text='Address:',font=('Calibri Bold',18),bg='#8A2BE2',fg='#E7FEFF').place(x=10,y=270)
                Label(root7,text='Date of Arrival:',font=('Calibri Bold',18),bg='#8A2BE2',fg='#E7FEFF').place(x=10,y=310)
                Label(root7,text='Check In:',font=('Calibri Bold',18),bg='#8A2BE2',fg='#E7FEFF').place(x=10,y=350)
                Label(root7,text='Check Out:',font=('Calibri Bold',18),bg='#8A2BE2',fg='#E7FEFF').place(x=10,y=390)
                Label(root7,text='Car Number:',font=('Calibri Bold',18),bg='#8A2BE2',fg='#E7FEFF').place(x=10,y=430)
                Label(root7,text='Room Number:',font=('Calibri Bold',18),bg='#8A2BE2',fg='#E7FEFF').place(x=10,y=470)

                entrywid2r7 = Entry(root7,width=25,border=5,font=('Arial 14'))
                entrywid3r7 = Entry(root7,width=25,border=5,font=('Arial 14'))
                entrywid4r7 = Entry(root7,width=25,border=5,font=('Arial 14'))
                entrywid5r7 = Entry(root7,width=25,border=5,font=('Arial 14'))
                entrywid6r7 = Entry(root7,width=25,border=5,font=('Arial 14'))
                entrywid7r7 = Entry(root7,width=25,border=5,font=('Arial 14'))
                entrywid8r7 = Entry(root7,width=25,border=5,font=('Arial 14'))
                entrywid9r7 = Entry(root7,width=25,border=5,font=('Arial 14'))

                entrywid2r7.place(x=200,y=190)
                entrywid3r7.place(x=200,y=230)
                entrywid4r7.place(x=200,y=270)
                entrywid5r7.place(x=200,y=310)
                entrywid6r7.place(x=200,y=350)
                entrywid7r7.place(x=200,y=390)
                entrywid8r7.place(x=200,y=430)
                entrywid9r7.place(x=200,y=470)

                entrywid2r7.insert(0,f'{rec[1]}')
                entrywid3r7.insert(0,f"{rec[2]}")
                entrywid4r7.insert(0,f'{rec[3]}')
                entrywid5r7.insert(0,f'{rec[4]}')
                entrywid6r7.insert(0,f'{rec[5]}')
                entrywid7r7.insert(0,f'{rec[6]}')
                entrywid8r7.insert(0,f'{rec[7]}')
                entrywid9r7.insert(0,f'{rec[8]}')

                Button(root7,text='Update',font=('Malgun Gothic Bold',14),border=8,padx=192,pady=5,command=update_processing).place(x=10,y=520)


def update_processing():
    update_rec_dict = {'NAME':entrywid2r7.get().title(),'PH_NO':int(entrywid3r7.get()),'ADDRESS':entrywid4r7.get().title(),'ARRIVAL':entrywid5r7.get(),'CHECK_IN':entrywid6r7.get(),'CHECK_OUT':entrywid7r7.get(),'CAR_NO':int(entrywid8r7.get()),'ROOM_NO':int(entrywid9r7.get())}

    old_rec = 1
    for new_rec in update_rec_dict.keys():
        if update_rec[0][old_rec] != update_rec_dict[new_rec]:
            if type(update_rec[0][old_rec]) is int: 
                cursor.execute(f"UPDATE hotel_mng_sys set {new_rec} = {update_rec_dict[new_rec]} where SL_NO = {entrywid1r7.get()};")
                conn.commit()

            elif type(update_rec[0][old_rec]) is str:
                cursor.execute(f"UPDATE hotel_mng_sys set {new_rec} = '{(update_rec_dict[new_rec])}' WHERE SL_NO = {entrywid1r7.get()};")
                conn.commit()
        old_rec += 1
    root7.destroy()


def delete_info():
    global root3
    root3 = Toplevel(root)
    root3.title('Delete a Record')
    root3.geometry('780x400')

    Label(root3,text=string2,font=('Calibri Bold',25)).place(x=20,y=10)
    Label(root3,text='Name :',font=('Calibri',20)).place(x=20,y=60)
    Label(root3,text='Phone Number :',font=('Calibri',20)).place(x=20,y=100)
    Label(root3,text='Room No :',font=('Calibri',20)).place(x=20,y=140)

    global entrywid1r3
    global entrywid2r3
    global entrywid3r3

    entrywid1r3 = Entry(root3,width=30,border=5,font='Arial 14')
    entrywid2r3 = Entry(root3,width=30,border=5,font='Arial 14')
    entrywid3r3 = Entry(root3,width=30,border=5,font='Arial 14')

    entrywid1r3.focus()

    global entry_wid_delete_list
    entry_wid_delete_list = [entrywid2r3,entrywid3r3]

    entrywid1r3.bind('<Return>',lambda e: ok_delete())
    entrywid2r3.bind('<Return>',lambda e: ok_delete())
    entrywid3r3.bind('<Return>',lambda e: ok_delete())

    entrywid1r3.place(x=250,y=65)
    entrywid2r3.place(x=250,y=105)
    entrywid3r3.place(x=250,y=145)

    Button(root3,text='OK',font=('Malgun Gothic Bold',18),fg='#0F0F0F',borderwidth=8,padx=85,pady=20,command=ok_delete).place(x=100,y=250)
    Button(root3,text='Cancel',font=('Malgun Gothic Bold',18),fg='#0F0F0F',borderwidth=8,padx=60,pady=20,command=root3.destroy).place(x=450,y=250)


def show_all_rec():
    cursor.execute('SELECT * FROM hotel_mng_sys;')
    recs = cursor.fetchall()

    root4 = Toplevel(root)
    root4.title('Records')
    root4.geometry('1418x400')

    Button(root4,text='Close',font=('Malgun Gothic Bold',18),fg='#3B444B',padx=1000,pady=10,borderwidth=8,command=root4.destroy).pack()
    
    global frame
    frame = Frame(root4)
    frame.pack(fill=BOTH,expand=1)

    global my_canvas3
    my_canvas3 = Canvas(frame)
    my_canvas3.pack(fill=BOTH,expand=1)

    global scroll_bar3
    scroll_bar3 = Scrollbar(my_canvas3,orient=VERTICAL,command=my_canvas3.yview)
    scroll_bar3.pack(fill=Y,side=RIGHT)

    my_canvas3.configure(yscrollcommand=scroll_bar3.set)
    my_canvas3.bind('<Configure>',lambda e: my_canvas3.configure(scrollregion=my_canvas3.bbox('all')))

    global frame4
    frame4 = Frame(my_canvas3,bg='#89CFF0')
    my_canvas3.create_window((0,0),window=frame4,anchor='nw')

    countrow = 2
    countcol = 0
    Label(frame4,text=' Records',font=('Calibri Bold Italic Bold',40),bg='#89CFF0').grid(row=0,column=0,columnspan=2,sticky=NW)
    Label(frame4,text='Guest ID |',font=('Impact',25),bg='#89CFF0').grid(row=1,column=countcol,sticky=N)
    Label(frame4,text='Name               |',font=('Impact',25),bg='#89CFF0').grid(row=1,column=countcol+1,sticky=NW)
    Label(frame4,text='Phone Number |',font=('Impact',25),bg='#89CFF0').grid(row=1,column=countcol+2,sticky=NW)
    Label(frame4,text='Address      |',font=('Impact',25),bg='#89CFF0').grid(row=1,column=countcol+3,sticky=NW)
    Label(frame4,text='Arrival Date |',font=('Impact',25),bg='#89CFF0').grid(row=1,column=countcol+4,sticky=N)
    Label(frame4,text='Check In |',font=('Impact',25),bg='#89CFF0').grid(row=1,column=countcol+5,sticky=NW)
    Label(frame4,text='Check Out |',font=('Impact',25),bg='#89CFF0').grid(row=1,column=countcol+6,sticky=NW)
    Label(frame4,text='Car No |',font=('Impact',25),bg='#89CFF0').grid(row=1,column=countcol+7,sticky=NW)
    Label(frame4,text='Room No',font=('Impact',25),bg='#89CFF0').grid(row=1,column=countcol+8,sticky=NW)

    for row in recs: 
        Label(frame4,text=f"{row[0]}",font=('Calibri',18),bg='#89CFF0').grid(row=countrow,column=countcol,sticky=N)
        Label(frame4,text=f"{row[1]}",font=('Calibri',18),bg='#89CFF0',wraplength=180,justify=LEFT).grid(row=countrow,column=countcol+1,sticky=NW)
        Label(frame4,text=f" {row[2]}",font=('Calibri',20),bg='#89CFF0').grid(row=countrow,column=countcol+2,sticky=NW)
        Label(frame4,text=f"{row[3]}",font=('Calibri',20),bg='#89CFF0',wraplength=180,justify=LEFT).grid(row=countrow,column=countcol+3,sticky=NW)
        Label(frame4,text=f"{row[4]}",font=('Calibri',20),bg='#89CFF0').grid(row=countrow,column=countcol+4,sticky=NW)
        Label(frame4,text=f"{row[5]}",font=('Calibri',20),bg='#89CFF0').grid(row=countrow,column=countcol+5,sticky=NW)
        Label(frame4,text=f"{row[6]}",font=('Calibri',20),bg='#89CFF0').grid(row=countrow,column=countcol+6,sticky=NW)
        Label(frame4,text=f"{row[7]}",font=('Calibri',20),bg='#89CFF0').grid(row=countrow,column=countcol+7,sticky=NW)
        Label(frame4,text=f"{row[8]}",font=('Calibri',20),bg='#89CFF0').grid(row=countrow,column=countcol+8,sticky=NW)
        countrow += 1


def search_rec():
    global root5
    root5 = Toplevel(root)
    root5.title('Search Record')
    root5.geometry('700x500')
    Label(root5,text='Fill in any one of the following Details:',font=('Calibri Bold',30)).place(x=10,y=10)
    Label(root5,text="Enter Name:",font=('Calibri',20)).place(x=10,y=65)
    Label(root5,text='Enter Phone Number:',font=('Calibri',20)).place(x=10,y=105)
    Label(root5,text='Enter Room No.',font=('Calibri',20)).place(x=10,y=145)

    global entrywid1r5
    global entrywid2r5
    global entrywid3r5

    entrywid1r5 = Entry(root5,width=30,border=5,font='Arial 14')
    entrywid2r5 = Entry(root5,width=30,border=5,font='Arial 14')
    entrywid3r5 = Entry(root5,width=30,border=5,font='Arial 14')

    global entry_wid_search_list
    entry_wid_search_list = [entrywid2r5,entrywid3r5]

    entrywid1r5.focus()

    entrywid1r5.bind('<Return>',lambda e: search_this_rec())
    entrywid2r5.bind('<Return>',lambda e: search_this_rec())
    entrywid3r5.bind('<Return>',lambda e: search_this_rec())
    entrywid1r5.place(x=300,y=70)
    entrywid2r5.place(x=300,y=110)
    entrywid3r5.place(x=300,y=150)

    Button(root5,text='Search🔍',font=('Malgun Gothic Bold',18),padx=40,pady=10,borderwidth=8,command=search_this_rec).place(x=105,y=300)
    Button(root5,text='Cancel',font=('Malgun Gothic Bold',18),padx=50,pady=10,borderwidth=8,command=root5.destroy).place(x=390,y=300)


def search_this_rec():
    global frame2    
    global root6
    name = "".join(entrywid1r5.get().split()) # NOTE: entrywid1r5.get().split() = ['Tapoban',Ray']

    if name.isalnum() == True: 
        root6 = Toplevel(root)
        frame2 = LabelFrame(root6,border=20,padx=10,pady=10)
        frame2.pack(padx=10,pady=10)
        row_no = 2
        col_no = 0
        Label(frame2,text=f'Search Results of Name:{entrywid1r5.get()}',font=('Calibri Bold Italic Bold',40)).grid(row=0,column=0,columnspan=9,sticky=NW)
        Label(frame2,text='Guest ID |',font=('Impact',25)).grid(row=1,column=col_no,sticky=W)
        Label(frame2,text='Name |',font=('Impact',25)).grid(row=1,column=col_no+1,sticky=W)
        Label(frame2,text='Phone Number |',font=('Impact',25)).grid(row=1,column=col_no+2,sticky=W)
        Label(frame2,text='Address |',font=('Impact',25)).grid(row=1,column=col_no+3,sticky=W)
        Label(frame2,text='Arrival Date |',font=('Impact',25)).grid(row=1,column=col_no+4,sticky=W)
        Label(frame2,text='Check In |',font=('Impact',25)).grid(row=1,column=col_no+5,sticky=W)
        Label(frame2,text='Check Out |',font=('Impact',25)).grid(row=1,column=col_no+6,sticky=W)
        Label(frame2,text='Car No |',font=('Impact',25)).grid(row=1,column=col_no+7,sticky=W)
        Label(frame2,text='Room No',font=('Impact',25)).grid(row=1,column=col_no+8,sticky=W)

        Button(root6,text='Close',font=('Malgun Gothic Bold',18),padx=40,pady=10,borderwidth=8,command=root6.destroy).pack()

        name = entrywid1r5.get()
        cursor.execute(f"SELECT * FROM hotel_mng_sys WHERE NAME == '{entrywid1r5.get().title()}';")
        name_data = cursor.fetchall()
                    
        for info in name_data:
            Label(frame2,text=f"{info[0]}",font=('Calivri',20)).grid(row=row_no,column=col_no)
            Label(frame2,text=f"{info[1]}",font=('Calibri',20),wraplength=180,justify=LEFT).grid(row=row_no,column=col_no+1)
            Label(frame2,text=f'{info[2]}',font=('Calibri',20)).grid(row=row_no,column=col_no+2)
            Label(frame2,text=f"{info[3]}",font=('Calibri',20),wraplength=180,justify=LEFT).grid(row=row_no,column=col_no+3)
            Label(frame2,text=f"{info[4]}",font=('Calibri',20)).grid(row=row_no,column=col_no+4)
            Label(frame2,text=f"{info[5]}",font=('Calibri',20)).grid(row=row_no,column=col_no+5)
            Label(frame2,text=f"{info[6]}",font=('Calibri',20)).grid(row=row_no,column=col_no+6)
            Label(frame2,text=f"{info[7]}",font=('Calibri',20)).grid(row=row_no,column=col_no+7)
            Label(frame2,text=f"{info[8]}",font=('Calibri',20)).grid(row=row_no,column=col_no+8)
            row_no += 1

    elif entrywid2r5.get().isalnum() == True:
        root6 = Toplevel(root)
        frame2 = LabelFrame(root6,border=20,padx=10,pady=10)
        frame2.pack(padx=10,pady=10)
        row_no = 2
        col_no = 0
        Label(frame2,text=f'Search Results of Name:{entrywid1r5.get()}',font=('Calibri Bold Italic Bold',40)).grid(row=0,column=0,columnspan=9,sticky=NW)
        Label(frame2,text='Guest ID |',font=('Impact',25)).grid(row=1,column=col_no,sticky=W)
        Label(frame2,text='Name |',font=('Impact',25)).grid(row=1,column=col_no+1,sticky=W)
        Label(frame2,text='Phone Number |',font=('Impact',25)).grid(row=1,column=col_no+2,sticky=W)
        Label(frame2,text='Address |',font=('Impact',25)).grid(row=1,column=col_no+3,sticky=W)
        Label(frame2,text='Arrival Date |',font=('Impact',25)).grid(row=1,column=col_no+4,sticky=W)
        Label(frame2,text='Check In |',font=('Impact',25)).grid(row=1,column=col_no+5,sticky=W)
        Label(frame2,text='Check Out |',font=('Impact',25)).grid(row=1,column=col_no+6,sticky=W)
        Label(frame2,text='Car No |',font=('Impact',25)).grid(row=1,column=col_no+7,sticky=W)
        Label(frame2,text='Room No',font=('Impact',25)).grid(row=1,column=col_no+8,sticky=W)

        Button(root6,text='Close',font=('Malgun Gothic Bold',18),padx=40,pady=10,borderwidth=8,command=root6.destroy).pack()

        cursor.execute(f"SELECT * FROM hotel_mng_sys WHERE PH_NO = {entrywid2r5.get()};")
        ph_no_data = cursor.fetchall()
        for info1 in ph_no_data:
            Label(frame2,text=f"{info1[0]}",font=('Calivri',20)).grid(row=row_no,column=col_no)
            Label(frame2,text=f"{info1[1]}",font=('Calibri',20)).grid(row=row_no,column=col_no+1)
            Label(frame2,text=f'{info1[2]}',font=('Calibri',20)).grid(row=row_no,column=col_no+2)
            Label(frame2,text=f"{info1[3]}",font=('Calibri',20)).grid(row=row_no,column=col_no+3)
            Label(frame2,text=f"{info1[4]}",font=('Calibri',20)).grid(row=row_no,column=col_no+4)
            Label(frame2,text=f"{info1[5]}",font=('Calibri',20)).grid(row=row_no,column=col_no+5)
            Label(frame2,text=f"{info1[6]}",font=('Calibri',20)).grid(row=row_no,column=col_no+6)
            Label(frame2,text=f"{info1[7]}",font=('Calibri',20)).grid(row=row_no,column=col_no+7)
            Label(frame2,text=f"{info1[8]}",font=('Calibri',20)).grid(row=row_no,column=col_no+8)
            row_no += 1

    elif entrywid3r5.get().isalnum() == True:
        root6 = Toplevel(root)
        frame2 = LabelFrame(root6,border=20,padx=10,pady=10)
        frame2.pack(padx=10,pady=10)
        row_no = 2
        col_no = 0
        Label(frame2,text=f'Search Results of Name:{entrywid1r5.get()}',font=('Calibri Bold Italic Bold',40)).grid(row=0,column=0,columnspan=9,sticky=NW)
        Label(frame2,text='Guest ID |',font=('Impact',25)).grid(row=1,column=col_no,sticky=W)
        Label(frame2,text='Name |',font=('Impact',25)).grid(row=1,column=col_no+1,sticky=W)
        Label(frame2,text='Phone Number |',font=('Impact',25)).grid(row=1,column=col_no+2,sticky=W)
        Label(frame2,text='Address |',font=('Impact',25)).grid(row=1,column=col_no+3,sticky=W)
        Label(frame2,text='Arrival Date |',font=('Impact',25)).grid(row=1,column=col_no+4,sticky=W)
        Label(frame2,text='Check In |',font=('Impact',25)).grid(row=1,column=col_no+5,sticky=W)
        Label(frame2,text='Check Out |',font=('Impact',25)).grid(row=1,column=col_no+6,sticky=W)
        Label(frame2,text='Car No |',font=('Impact',25)).grid(row=1,column=col_no+7,sticky=W)
        Label(frame2,text='Room No',font=('Impact',25)).grid(row=1,column=col_no+8,sticky=W)

        Button(root6,text='Close',font=('Malgun Gothic Bold',18),padx=40,pady=10,borderwidth=8,command=root6.destroy).pack()

        cursor.execute(f"SELECT * FROM hotel_mng_sys WHERE ROOM_NO = {entrywid3r5.get()};")
        room_no_data = cursor.fetchall()
        for info2 in room_no_data:
            Label(frame2,text=f"{info2[0]}",font=('Calivri',20)).grid(row=row_no,column=col_no)
            Label(frame2,text=f"{info2[1]}",font=('Calibri',20)).grid(row=row_no,column=col_no+1)
            Label(frame2,text=f'{info2[2]}',font=('Calibri',20)).grid(row=row_no,column=col_no+2)
            Label(frame2,text=f"{info2[3]}",font=('Calibri',20)).grid(row=row_no,column=col_no+3)
            Label(frame2,text=f"{info2[4]}",font=('Calibri',20)).grid(row=row_no,column=col_no+4)
            Label(frame2,text=f"{info2[5]}",font=('Calibri',20)).grid(row=row_no,column=col_no+5)
            Label(frame2,text=f"{info2[6]}",font=('Calibri',20)).grid(row=row_no,column=col_no+6)
            Label(frame2,text=f"{info2[7]}",font=('Calibri',20)).grid(row=row_no,column=col_no+7)
            Label(frame2,text=f"{info2[8]}",font=('Calibri',20)).grid(row=row_no,column=col_no+8)
            row_no += 1
    else:
        messagebox.showerror('Error','You need to fill any one record to get search result',parent=root5)


def ok_delete():
    name2 = ''.join(entrywid1r3.get().split())

    if name2.isalnum() == True:
        response = messagebox.askyesno('Delete a Record',f'Are you sure you want to delete all details about {entrywid1r3.get()}?',parent=root3)
        if response == 1:
            cursor.execute(f"DELETE FROM hotel_mng_sys WHERE NAME = '{entrywid1r3.get().title()}';")
            conn.commit()
            entrywid1r3.delete(0,END)

            cursor.execute('SELECT * FROM hotel_mng_sys;')
            all_data = cursor.fetchall()
            sl_num = 1
            for rec in all_data:
                cursor.execute(F'UPDATE hotel_mng_sys SET SL_NO = {sl_num} WHERE NAME = "{rec[1]}";')
                conn.commit()
                sl_num += 1

            entrywid1.delete(0,END)

            cursor.execute('Select * from hotel_mng_sys;')
            all_data = cursor.fetchall()
            if len(all_data) == len(all_data) % 10:
                entrywid1.insert(0,f"0{len(all_data)+1}")
            else:
                entrywid1.insert(0,len(all_data)+1)

    elif entrywid2r3.get().isalnum() == True:
        response2 = messagebox.askyesno('Delete a Record',f'Are you sure you want to delete all details about guest having Phone Number: {entrywid2r3.get()}?',parent=root3)
        if response2 == 1:
            cursor.execute(f"DELETE FROM hotel_mng_sys WHERE PH_NO = {entrywid2r3.get()};")
            conn.commit()
            entrywid2r3.delete(0,END)

            cursor.execute('SELECT * FROM hotel_mng_sys;')
            all_data = cursor.fetchall()
            sl_num = 1
            for rec in all_data:
                cursor.execute(F'UPDATE hotel_mng_sys SET SL_NO = {sl_num} WHERE NAME = "{rec[1]}";')
                conn.commit()
                sl_num += 1

            entrywid1.delete(0,END)

            cursor.execute('Select * from hotel_mng_sys;')
            all_data = cursor.fetchall()
            if len(all_data) == len(all_data) % 10:
                entrywid1.insert(0,f"0{len(all_data)+1}")
            else:
                entrywid1.insert(0,len(all_data)+1)

    elif entrywid3r3.get().isalnum() == True:
        response3 = messagebox.askyesno('Delete a Record',f'Are you sure you want to delete all details about guest in Room Number: {entrywid3r3.get()}?',parent=root3)
        if response3 == 1: 
            cursor.execute(f"DELETE FROM hotel_mng_sys WHERE ROOM_NO = {entrywid3r3.get()};")
            conn.commit()
            entrywid3r3.delete(0,END)

            cursor.execute('SELECT * FROM hotel_mng_sys;')
            all_data = cursor.fetchall()
            sl_num = 1
            for rec in all_data:
                cursor.execute(F'UPDATE hotel_mng_sys SET SL_NO = {sl_num} WHERE NAME = "{rec[1]}";')
                conn.commit()
                sl_num += 1

            entrywid1.delete(0,END)

            cursor.execute('Select * from hotel_mng_sys;')
            all_data = cursor.fetchall()
            if len(all_data) == len(all_data) % 10:
                entrywid1.insert(0,f"0{len(all_data)+1}")
            else:
                entrywid1.insert(0,len(all_data)+1)
                
    else:
        messagebox.showwarning('No Record Deleted','You have to fill any one of the details to delete a record',parent=root3)

photo = Image.open('Hotel Mng pic.png')

my_img = photo.resize((1400,800))
pic = ImageTk.PhotoImage(my_img)

string2 = 'Fill in any one Detail Unique to the Particular Info:'

button1 = Button(root,image=pic,font=('Georgia Bold',20),padx=750,pady=450,bg='#6699CC',fg='#F8F8FF',command=newroot).pack()


root.mainloop()