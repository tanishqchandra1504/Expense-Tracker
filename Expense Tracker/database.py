import sqlite3
from datetime import datetime
# Date,time,week = datetime.now().strftime("%d %m %Y"),datetime.now().strftime("%H:%M:%S"),datetime.now().strftime("%V")
# print(Date,week,time)

def get_week_no(date):
    date=[int(x) for x in date.split(sep=' ')]
    days=0
    m=1
    while m<date[1]:
        if m in [1,3,5,7,8,10,12]:
            days+=31
            m+=1
        elif m in [4,6,9,11]:
            days+=30
            m+=1
        else:
            if date[2]%400==0 or (date[2]%4==0 and date[2]%100!=0):
                days+=29
            else:
                days+=28
            m+=1
    days+=date[0]
    return days//7

def ConnectToDatabase():
    conn=sqlite3.connect("expensetracker.db")
    c=conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS categories(category_name text,color text)" )
    c.execute("CREATE TABLE IF NOT EXISTS expenses(category_name text,amount real, Date text,Week INTEGER)" )
    return conn

def show_all_categories(conn):
    #conn=sqlite3.connect("")
    c=conn.cursor()
    c.execute("SELECT * FROM categories ")
    items=c.fetchall()
    return items

def insert_category(conn,cat : str, color:str):
    c=conn.cursor()
    c.execute("INSERT INTO categories VALUES (?,?)",(cat,color))
    conn.commit()

def delete_category(conn,cat:str,color,str):
    c=conn.cursor()
    c.execute("DELETE FROM categories WHERE category_name=(?) AND color=(?)",(cat,color))
    c.execute("DELETE FROM expenses WHERE category_name=(?)",cat)
    conn.commit()

def edit_category(conn,old_cat,new_cat):
    c=conn.cursor()
    c.execute("UPDATE categories SET category_name=(?),color=(?) WHERE category_name=(?) AND color=(?)",new_cat+old_cat)
    conn.commit()
#edit_category(ConnectToDatabase(),('ree','#0000FF'),('FREE','#000000'))

def show_daily_expense(conn,date:str):
    c=conn.cursor()
    c.execute("SELECT * FROM expenses WHERE Date=(?)",(date,))
    items=c.fetchall()
    return items

def show_weekly_expense(conn,Week:int):
    c=conn.cursor()
    c.execute("SELECT * FROM expenses WHERE Week=(?)",(Week,))
    items=c.fetchall()
    return items

def show_monthly_expense(conn,month:str):
    c=conn.cursor()
    c.execute("SELECT * FROM expenses WHERE SUBSTR(Date,4,2)=(?)",(month,))
    return c.fetchall()

def insert_expense(conn,data:tuple):
    # data=(category_name,amount,Date)
    data+=(get_week_no(data[2]),)
    c=conn.cursor()
    c.execute("INSERT INTO expenses VALUES(?,?,?,?)",data)
    conn.commit()
# insert_expense(ConnectToDatabase(),('cat1',23,Date))

def delete_expense(conn,data:tuple):
    # data = (category_name,amount,date)
    c=conn.cursor()
    c.execute("DELETE FROM expenses WHERE category_name=(?) AND amount=(?) AND Date=(?)",data)
    conn.commit()
# delete_expense(ConnectToDatabase(),('cat1',23,'08 04 2024'))

def edit_expense(conn,data_old:tuple,data_new:tuple):
    # data=(category_name,amount,Date)
    data_new+=tuple(get_week_no(data_new[2]))
    c=conn.cursor()
    c.execute("UPDATE expenses SET category_name=(?),amount=(?),Date=(?),Week=(?) WHERE category_name=(?) AND amount=(?) AND Date=(?)",data_new+data_old)
    conn.commmit()


# print(show_weekly_expense(ConnectToDatabase(),1))

