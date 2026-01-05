from tkinter import Tk,Label,Frame,Button,Entry,messagebox,simpledialog,filedialog
import time
from datetime import datetime
import Generator
import sqlite3
import EmailHandler
import TableCreator
import re
from PIL import Image,ImageTk
import os

TableCreator.create()

def update_time():
    curdate=time.strftime('%d-%b-%Y ⏱️ %r')
    date.configure(text=curdate)
    date.after(1000,update_time)  

def newuser_screen():

    def back():
        frm.destroy()
        newuser_screen()

    def reset_click():
         e_name.delete(0,'end')
         e_adhar.delete(0,'end')
         e_email.delete(0,'end')
         e_mob.delete(0,'end')
         e_name.focus()

    def createacn_db():
        name=e_name.get()
        email=e_email.get()
        adhar=e_adhar.get()
        mob=e_mob.get()

        if len(name)==0 or len(email)==0 or len(adhar)==0 or len(mob)==0:
            messagebox.showwarning('New User','Empty fields are not allowed')
            return
        
        match=re.fullmatch(r"[a-zA-Z0-1_.]+@[a-zA-Z]+\.[a-zA-Z]+",email)
        if match==None:
            messagebox.showwarning('New User','Invalid email')
            return
        
        match=re.fullmatch("[6-9][0-9]{9}",mob)
        if match==None:
            messagebox.showwarning('New User','Invalid Mobile No.')
            return 
        
        match=re.fullmatch("[0-9]{12}",adhar)
        if match==None:
            messagebox.showwarning('New User','Invalid Adhaar No.')
            return 

        bal=0
        opendate=datetime.now()
        pwd=Generator.generate_pass()
        query='''insert into accounts values(?,?,?,?,?,?,?,?)'''
        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        curobj.execute(query,(None,name,pwd,mob,email,adhar,bal,opendate))
        conobj.commit()
        conobj.close()

        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        query='''select max(acn) from accounts'''
        curobj.execute(query)
        tup=curobj.fetchone()
        conobj.close()
        EmailHandler.send_credentials(email,name,tup[0],pwd)
        messagebox.showinfo('Account Creation','Your account is opened. \n We have mailed your credentials to given email.')

    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.12,relwidth=1,relheight=.8)

    back_btn=Button(frm,text="Back",font=('arial',15,'bold'),bd=5,activebackground='blue',
                    activeforeground='white',bg='white',command=main_screen)
    back_btn.place(relx=0,rely=0)

    lbl_name=Label(frm,text='👤Name',font=('arial',15,'bold'),bg='pink',width=7)
    lbl_name.place(relx=.1,rely=.1)
    e_name=Entry(frm,font=('arial',15,'bold'),bd=5)
    e_name.place(relx=.2,rely=.1)
    e_name.focus()

    lbl_mob=Label(frm,text='📱Mob. No',font=('arial',15,'bold'),bg='pink',width=9)
    lbl_mob.place(relx=.5,rely=.1)
    e_mob=Entry(frm,font=('arial',15,'bold'),bd=5)
    e_mob.place(relx=.6,rely=.1)

    lbl_email=Label(frm,text='📧Email',font=('arial',15,'bold'),bg='pink',width=7)
    lbl_email.place(relx=.1,rely=.2)
    e_email=Entry(frm,font=('arial',15,'bold'),bd=5)
    e_email.place(relx=.2,rely=.2)

    lbl_adhar=Label(frm,text='💳Aadhar No.',font=('arial',15,'bold'),bg='pink',width=9)
    lbl_adhar.place(relx=.5,rely=.2)
    e_adhar=Entry(frm,font=('times new roman',16,'bold'),bd=5)
    e_adhar.place(relx=.6,rely=.2)

    sub_btn=Button(frm,text='Submit',font=('times new roman',20,'bold'),bd=5,width=8,
                activebackground='blue',activeforeground='white',command=createacn_db)
    sub_btn.place(relx=.3,rely=.5)

    res_btn=Button(frm,text='Reset',font=('times new roman',20,'bold'),bd=5,width=8,
                   activebackground='blue',activeforeground='white',command=reset_click)
    res_btn.place(relx=.5,rely=.5)

def wel_screen(acn=None):

    def logout_click():
        frm.destroy()
        main_screen()

    def check_screen():
            ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
            ifrm.configure(bg='white')
            ifrm.place(relx=.18,rely=.15,relwidth=.6,relheight=.7)

            lbl_check=Label(ifrm,text='Your Details',font=('times new roman',25,'bold'),
                            fg='dark blue',bg='white')
            lbl_check.pack()

            conobj=sqlite3.connect(database='mybank.sqlite')
            curobj=conobj.cursor()
            query='''select acn,bal,adhar,email,opendate from accounts where acn=?'''
            curobj.execute(query,(acn,))
            tup=curobj.fetchone()
            conobj.close()

            details=f'''
Account No.     =   {tup[0]}\n
Account Balance =   {tup[1]}\n
Adhar No.       =   {tup[2]}\n
Email           =   {tup[3]}\n
Open Date       =   {tup[4]}
'''
            lbl_details=Label(ifrm,text=details,font=('times new roman',16,'bold'),
                              bg='white',fg='blue')
            lbl_details.place(relx=.25,rely=.1)
    def update_screen():

            def update_db():
                name=e_name.get()
                email=e_email.get()
                mob=e_mob.get()
                pwd=e_pass.get()            

                if len(name)==0 or len(email)==0 or len(mob)==0 or len(pwd)==0:
                    messagebox.showwarning('Update Screen','Empty fields are not allowed')
                    return
                
                match=re.fullmatch("[a-zA-Z]+",name)
                if match==None:
                    messagebox.showwarning('Update screen','Invalid name')
                    return
        
                match=re.fullmatch(r"[a-zA-Z0-1_.]+@[a-zA-Z]+\.[a-zA-Z]+",email)
                if match==None:
                    messagebox.showwarning('Update screen','Invalid email')
                    return
        
                match=re.fullmatch("[6-9][0-9]{9}",mob)
                if match==None:
                    messagebox.showwarning('Update screen','Invalid Mobile No.')
                    return 
        
                match=re.fullmatch("[a-zA-Z0-1!@#$%&_]+",pwd)
                if match==None:
                    messagebox.showwarning('Update screen','Invalid Password')
                    return

                conobj=sqlite3.connect(database='mybank.sqlite')
                curobj=conobj.cursor()
                query='''update accounts set name=?,email=?,mob=?,pass=? where acn=?'''
                curobj.execute(query,(name,email,mob,pwd,acn))
                conobj.commit()
                conobj.close()
                messagebox.showinfo('Update Datails','Details Updated Successfully')
                wel_screen(acn)

            conobj=sqlite3.connect(database='mybank.sqlite')
            curobj=conobj.cursor()
            query='''select name,email,mob,pass from accounts where acn=?'''
            curobj.execute(query,(acn,))
            tup=curobj.fetchone()
            conobj.close()

            ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
            ifrm.configure(bg='white')
            ifrm.place(relx=.18,rely=.15,relwidth=.6,relheight=.7)

            lbl_update=Label(ifrm,text='Update Details',font=('times new roman',25,'bold'),
                             fg='dark blue',bg='white')
            lbl_update.pack()

            lbl_name=Label(ifrm,text='Name',font=('times new roman',15,'bold'),bg='red',fg='yellow')
            lbl_name.place(relx=.05,rely=.2)
            e_name=Entry(ifrm,font=('times new roman',15,'bold'),bd=5)
            e_name.place(relx=.15,rely=.2)

            lbl_mob=Label(ifrm,text='Mob.',font=('times new roman',15,'bold'),bg='red',fg='yellow')
            lbl_mob.place(relx=.55,rely=.2)
            e_mob=Entry(ifrm,font=('times new roman',15,'bold'),bd=5)
            e_mob.place(relx=.65,rely=.2)

            lbl_pass=Label(ifrm,text='Pass',font=('times new roman',15,'bold'),bg='red',fg='yellow')
            lbl_pass.place(relx=.05,rely=.4)
            e_pass=Entry(ifrm,font=('times new roman',15,'bold'),bd=5)
            e_pass.place(relx=.15,rely=.4)

            lbl_email=Label(ifrm,text='Email',font=('times new roman',15,'bold'),bg='red',fg='yellow')
            lbl_email.place(relx=.55,rely=.4)
            e_email=Entry(ifrm,font=('times new roman',15,'bold'),bd=5)
            e_email.place(relx=.65,rely=.4)

            sub_btn=Button(ifrm,text='Update',font=('times new roman',15,'bold'),bg='green',
                           fg='white',activebackground='white',activeforeground='black',bd=5,
                           command=update_db)
            sub_btn.place(relx=.4,rely=.6)

            e_name.insert(0,tup[0])
            e_email.insert(0,tup[1])
            e_mob.insert(0,tup[2])
            e_pass.insert(0,tup[3])

    def deposit_screen():
            
            def depo_db():
                amt=float(e_amt.get())
                conobj=sqlite3.connect(database='mybank.sqlite')
                curobj=conobj.cursor()
                query='''update accounts set bal=bal+? where acn=?'''
                curobj.execute(query,(amt,acn))
                conobj.commit()
                conobj.close()
                messagebox.showinfo('Deposit Balance',f'{amt} deposited successfully.')
                e_amt.delete(0,'end')
                e_amt.focus()

            ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
            ifrm.configure(bg='white')
            ifrm.place(relx=.18,rely=.15,relwidth=.6,relheight=.7)

            lbl_deposit=Label(ifrm,text='Deposit Amount',font=('times new roman',25,'bold'),
                              fg='dark blue',bg='white')
            lbl_deposit.pack()

            lbl_amt=Label(ifrm,text='Enter Amt.',font=('times new roman',20,'bold'),
                          bg='blue',fg='white')
            lbl_amt.place(relx=.15,rely=.3)
            e_amt=Entry(ifrm,font=('times new roman',20,'bold'),bd=5)
            e_amt.place(relx=.35,rely=.3)
            e_amt.focus()

            dep_btn=Button(ifrm,text='Deposit',font=('times new roman',20,'bold'),bg='green',
                           fg='black',activebackground='white',activeforeground='blue',bd=5,
                           command=depo_db)
            dep_btn.place(relx=.4,rely=.5)

    def withdraw_screen():
            
            def withdraw_db():
                amt=float(e_amt.get())
                conobj=sqlite3.connect('mybank.sqlite')
                curobj=conobj.cursor()
                query='''select bal,email,name from accounts where acn=?'''
                curobj.execute(query,(acn,))
                tup=curobj.fetchone()
                conobj.close()

                if tup[0]>=amt:
                    gen_otp=Generator.gen_otp()
                    EmailHandler.send_withdraw_otp(tup[1],tup[2],gen_otp,amt)
                    for i in range(3):
                        user_otp=simpledialog.askinteger('Withdraw OTP','Enter OTP')
                        if gen_otp==user_otp:
                            conobj=sqlite3.connect(database='mybank.sqlite')
                            curobj=conobj.cursor()
                            query='''update accounts set bal=bal-? where acn=?'''
                            curobj.execute(query,(amt,acn))
                            conobj.commit()
                            conobj.close()
                            messagebox.showinfo('Withdraw Amount',f'{amt} withdraw successfully.')
                            e_amt.delete(0,'end')
                            e_amt.focus()
                            break
                        else:
                            messagebox.showerror('Withdraw OTP','Invalid OTP')
                            withdraw_btn.configure(text='Resend OTP')
                else:
                     messagebox.showerror('Withdraw Amt',f'You dont have insufficient bal : {tup[0]}' )
                     
            ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
            ifrm.configure(bg='white')
            ifrm.place(relx=.18,rely=.15,relwidth=.6,relheight=.7)

            lbl_withdraw=Label(ifrm,text='Withdraw Amount',font=('times new roman',25,'bold'),
                               fg='dark blue',bg='white')
            lbl_withdraw.pack()

            lbl_amt=Label(ifrm,text='Enter Amt.',font=('times new roman',20,'bold'),
                          bg='blue',fg='white')
            lbl_amt.place(relx=.15,rely=.3)
            e_amt=Entry(ifrm,font=('times new roman',20,'bold'),bd=5)
            e_amt.place(relx=.35,rely=.3)
            e_amt.focus()

            withdraw_btn=Button(ifrm,text='Withdraw',font=('times new roman',20,'bold'),bg='green',
                           fg='black',activebackground='white',activeforeground='blue',bd=5,
                           command=withdraw_db)
            withdraw_btn.place(relx=.4,rely=.5)

    def transfer_screen():
            
            def trf_db():
                to_acn=int(e_toacn.get())
                amt=float(e_amt.get())
                conobj=sqlite3.connect(database='mybank.sqlite')
                curobj=conobj.cursor()
                query='''select * from accounts where acn=?'''
                curobj.execute(query,(to_acn,))
                tup=curobj.fetchone()
                conobj.close()

                if tup==None:
                     messagebox.showerror('Transfer Amt','Account number not exist')
                     return
                
                conobj=sqlite3.connect(database='mybank.sqlite')
                curobj=conobj.cursor()
                query='''select bal,email,name from accounts where acn=?'''
                curobj.execute(query,(acn,))
                tup=curobj.fetchone()
                conobj.close()

                if tup[0]>=amt:
                     gen_otp=Generator.gen_otp()
                     EmailHandler.send_transfer_otp(tup[1],tup[2],gen_otp,amt,to_acn)
                     for i in range(3):
                        user_otp=simpledialog.askinteger('Trf Amt','Enter OTP')
                        if gen_otp==user_otp:
                             conobj=sqlite3.connect(database='mybank.sqlite')
                             curobj=conobj.cursor()
                             query1='''update accounts set bal=bal-? where acn=?'''
                             query2='''update accounts set bal=bal+? where acn=?'''
                             curobj.execute(query1,(amt,acn))
                             curobj.execute(query2,(amt,to_acn))
                             conobj.commit()
                             conobj.close()
                             messagebox.showinfo('Trf Amt',f'{amt} transfer successfully.')
                             e_amt.delete(0,'end')
                             e_amt.focus()
                             break
                        else:
                             messagebox.showerror('Trf Amt','Invalid OTP')
                else:
                     messagebox.showerror('Trf Amt',f'Insufficient Balance : {tup[0]}')

            ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
            ifrm.configure(bg='white')
            ifrm.place(relx=.18,rely=.15,relwidth=.6,relheight=.7)

            lbl_transfer=Label(ifrm,text='Transfer Amount',font=('times new roman',25,'bold'),
                               fg='dark blue',bg='white')
            lbl_transfer.pack()

            lbl_toacn=Label(ifrm,text='Trf ACN',font=('times new roman',20,'bold'),bg='red',fg='yellow')
            lbl_toacn.place(relx=.15,rely=.2)
            e_toacn=Entry(ifrm,font=('times new roman',20,'bold'),bd=5)
            e_toacn.place(relx=.35,rely=.2)
            e_toacn.focus()

            lbl_amt=Label(ifrm,text='Enter Amt',font=('times new roman',20,'bold'),bg='red',fg='yellow')
            lbl_amt.place(relx=.15,rely=.4)
            e_amt=Entry(ifrm,font=('times new roman',20,'bold'),bd=5)
            e_amt.place(relx=.35,rely=.4)

            trf_btn=Button(ifrm,text='Transfer',font=('times new roman',20,'bold'),bg='green',fg='black',
                           activebackground='white',activeforeground='black',bd=5,
                           command=trf_db)
            trf_btn.place(relx=.4,rely=.6)

    conobj=sqlite3.connect(database='mybank.sqlite')
    curobj=conobj.cursor()
    query='select name from accounts where acn=?'
    curobj.execute(query,(acn,))
    tup=curobj.fetchone()
    conobj.close()

    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.12,relwidth=1,relheight=.8)

    wel_lbl=Label(frm,text=f"Welcome, {tup[0]}",font=('times new roman',20,'bold'),
                  bg='yellow',fg='red')
    wel_lbl.place(relx=.001,rely=0)

    logout_btn=Button(frm,text='Log Out',font=('times new roman',15,'bold'),activebackground='blue',
                                               activeforeground='white',width=6,
                                               bd=5,command=logout_click)
    logout_btn.place(relx=.93,rely=0)

    def update_pfp():
        name=filedialog.askopenfilename()
        os.rename(name,f"{acn}.jpg")
        img_pfp=Image.open(f"{acn}.jpg").resize((250,250))
        imgtk_pfp=ImageTk.PhotoImage(img_pfp,master=root)
        lbl_img_pfp=Label(frm,image=imgtk_pfp)
        lbl_img_pfp.place(relx=.79,rely=.1)
        lbl_img_pfp.image=imgtk_pfp
        
    if os.path.exists(f'{acn}.jpg'):
        img_pfp=Image.open(f"{acn}.jpg").resize((250,250))
    else:
        img_pfp=Image.open('default.jpeg').resize((250,250))

    imgtk_pfp=ImageTk.PhotoImage(img_pfp,master=root)
    lbl_img_pfp=Label(frm,image=imgtk_pfp)
    lbl_img_pfp.place(relx=.79,rely=.1)
    lbl_img_pfp.image=imgtk_pfp

    up_pfp=Button(frm,text='Update Profile',font=('times new roman',18,'bold'),bg='red',fg='yellow',
                    activebackground='white',activeforeground='black',bd=5,command=update_pfp)
    up_pfp.place(relx=.83,rely=.6)

    check_btn=Button(frm,text='Check Details',font=('times new roman',15,'bold'),
                     activebackground='blue',activeforeground='white',bd=5,width=15,command=check_screen)
    check_btn.place(relx=.001,rely=.15)

    update_btn=Button(frm,text='Update Details',font=('times new roman',15,'bold'),
                      activebackground='blue',activeforeground='white',
                      bd=5,width=15,command=update_screen)
    update_btn.place(relx=.001,rely=.3)

    deposit_btn=Button(frm,text='Deposit Amount',font=('times new roman',15,'bold'),
                       activebackground='blue',activeforeground='white',
                       bd=5,width=15,command=deposit_screen)
    deposit_btn.place(relx=.001,rely=.45)

    withdraw_btn=Button(frm,text='Withdraw Amount',font=('times new roman',15,'bold'),
                       activebackground='blue',activeforeground='white',
                       bd=5,width=15,command=withdraw_screen)
    withdraw_btn.place(relx=.001,rely=.6)

    transfer_btn=Button(frm,text='Transfer Amount',font=('times new roman',15,'bold'),
                       activebackground='blue',activeforeground='white',
                       bd=5,width=15,command=transfer_screen)
    transfer_btn.place(relx=.001,rely=.75)

def existuser_screen():

    def back():
        frm.destroy()
        main_screen()

    def reset_click():
         e_acn.delete(0,'end')
         e_pass.delete(0,'end')
         e_acn.focus()

    def wel_click():
        acn=e_acn.get()
        pwd=e_pass.get()

        if len(acn)==0 or len(pwd)==0:
            messagebox.showwarning('Exist User','Empty fields are not allowed')
            return
        
        match=re.fullmatch("[0-9]+",acn)
        if match==None:
            messagebox.showwarning('Exist User','Invalid Account No.')
            return
        
        match=re.fullmatch("[a-zA-Z0-1!@#$%&_]+",pwd)
        if match==None:
            messagebox.showwarning('New User','Invalid Password')
            return

        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where acn=? and pass=?'
        curobj.execute(query,(acn,pwd))
        tup=curobj.fetchone()
        conobj.close()

        if tup==None:
            messagebox.showerror('Login','Invalid acn or pass')
        else:
            acn=tup[0]
            frm.destroy()
            wel_screen(acn)

    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.12,relwidth=1,relheight=.8)

    back_btn=Button(frm,text='Back',font=('arial',15,'bold'),bd=5,activebackground='blue',
                    activeforeground='white',bg='white',command=main_screen)
    back_btn.place(relx=0,rely=0)

    lbl_acn=Label(frm,text='ACN',font=('times new roman',15,'bold'),bd=5,width=10,bg='pink')
    lbl_acn.place(relx=.3,rely=.1)
    
    e_acn=Entry(frm,font=('times new roman',15,'bold'),bd=5)
    e_acn.place(relx=.4,rely=.1)
    e_acn.focus()

    lbl_pass=Label(frm,text='Password',font=('times new roman',15,'bold'),bd=5,width=10,bg='pink')
    lbl_pass.place(relx=.3,rely=.2)

    e_pass=Entry(frm,font=('times new roman', 15,'bold'),bd=5,show='*')
    e_pass.place(relx=.4,rely=.2)

    ver_btn=Button(frm,text='Verify',font=('times new roman',15,'bold'),bd=5,width=15,
                   activebackground='blue',activeforeground='white',command=wel_click)
    ver_btn.place(relx=.3,rely=.4)

    res_btn=Button(frm,text='Reset',font=('times new roman',20,'bold'),bd=5,width=5,
                   activebackground='blue',activeforeground='white',command=reset_click)
    res_btn.place(relx=.43,rely=.5)

    fgt_btn=Button(frm,text='Forget Password',font=('times new roman',15,'bold'),bd=5,width=15,
                   activebackground='blue',activeforeground='white',command=fgt_screen)
    fgt_btn.place(relx=.5,rely=.4)

    def fgt_click():
        frm.destroy()
        fgt_screen()
    
def fgt_screen():

    def existuser_click():
        frm.destroy()
        existuser_screen()

    def reset_click():
         e_fgacn.delete(0,'end')
         e_fgtadr.delete(0,'end')
         otp_btn.configure(text='Send OTP')
         e_fgacn.focus()
    
    def send_otp():
        gen_otp=Generator.gen_otp()
        acn=e_fgacn.get()
        adr=e_fgtadr.get()

        if len(acn)==0 or len(adr)==0:
            messagebox.showwarning('Exist User','Empty fields are not allowed')
            return
        
        match=re.fullmatch("[0-9]+",acn)
        if match==None:
            messagebox.showwarning('Exist User','Invalid Account No.')
            return
        
        match=re.fullmatch("[0-9]{12}",adr)
        if match==None:
            messagebox.showwarning('New User','Invalid Adhaar No.')
            return

        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        query="select name,email,pass from accounts where acn=? and adhar=?"
        curobj.execute(query,(acn,adr))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror('Forgot Password','Record not found')
        else:
            EmailHandler.send_otp(tup[1],tup[0],gen_otp)
            for i in range(3):    
                user_otp=simpledialog.askinteger('Password recovery','Enter OTP')
                if gen_otp==user_otp:
                    messagebox.showinfo('Password recovery',f"Your Password = {tup[2]}")
                    break
                else:
                    messagebox.showerror("Password recovery","Incorrect OTP")
                    otp_btn.configure(text='Resend OTP')
                    
    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.12,relwidth=1,relheight=.8)

    back_btn=Button(frm,text='Back',font=('arial',15,'bold'),bd=5,activebackground='blue',
                    activeforeground='white',bg='white',command=existuser_click)
    back_btn.place(relx=0,rely=0)
        
    lbl_fgacn=Label(frm,text='ACN',font=('times new roman',15,'bold'),bg='pink')
    lbl_fgacn.place(relx=.3,rely=.1)
    e_fgacn=Entry(frm,font=('times new roman',15,'bold'),bd=5)
    e_fgacn.place(relx=.4,rely=.1)
    e_fgacn.focus()

    lbl_fgtadr=Label(frm,text='Aadhar',font=('times new roman',15,'bold'),bg='pink')
    lbl_fgtadr.place(relx=.3,rely=.2)
    e_fgtadr=Entry(frm,font=('times new roman',15,'bold'),bd=5)
    e_fgtadr.place(relx=.4,rely=.2)

    otp_btn=Button(frm,text='Send OTP',font=('times new roman',15,'bold'),bd=5,
                   activebackground='blue',activeforeground='white',width=10,command=send_otp)
    otp_btn.place(relx=.34,rely=.4)

    res_btn=Button(frm,text='Reset',font=('times new roman',15,'bold'),bd=5,width=10,
                   activebackground='blue',activeforeground='white',command=reset_click)
    res_btn.place(relx=.5,rely=.4)

def main_screen():

    def newuser_click():
        frm.destroy()
        newuser_screen()

    def existuser_click():
        frm.destroy()
        existuser_screen()

    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.12,relwidth=1,relheight=.8)

    wel_msg=Label(frm,text='🙏Welcome to SumJaiz Bank🙏',
                  font=('elephant',20,'bold','italic'),fg='red',bg='pink')
    wel_msg.place(relx=.3,rely=.05)

    newuser_btn=Button(frm,text="New User\nCreate Account",font=('arial',15,'bold'),bd=5,width=15,
                       activebackground='blue',activeforeground='white',bg='white',command=newuser_click)
    newuser_btn.place(relx=.27,rely=.3)

    existuser_btn=Button(frm,text="Existing User\n Log In",font=('arial',15,'bold'),bd=5,width=15,
                        activebackground='blue',activeforeground='white',bg='white',command=existuser_click)
    existuser_btn.place(relx=.55,rely=.3)

root=Tk()
root.state('zoomed')
root.resizable(width=False,height=False)
root.configure(bg='powder blue')

title=Label(root,text='BANKING SIMULATION',font=('arial',30,'bold','underline'),background='powder blue')
title.pack()

img1=Image.open('banklogo.png').resize((150,80))
img_tk1=ImageTk.PhotoImage(img1,master=root)
lbl_img1=Label(root,image=img_tk1)
lbl_img1.place(relx=0,rely=0)

img2=Image.open('banklogo1.png').resize((150,80))
img_tk2=ImageTk.PhotoImage(img2,master=root)
lbl_img2=Label(root,image=img_tk2)
lbl_img2.place(relx=.88,rely=0)

footer=Label(root,text='Developed by Sumit Jaiz \n 📱 9520244709',font=('arial',15,'bold'),
             background='powder blue')
footer.pack(side='bottom')
title.pack()

curdate=time.strftime("%d-%b-%Y ⏱️ %r")
date=Label(root,text=curdate,font=('arial',15,'bold'),background='powder blue')
date.pack()

update_time()

main_screen()
root.mainloop()