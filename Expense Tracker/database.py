import sqlite3
import datetime
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
    c.execute("CREATE TABLE IF NOT EXISTS expenses(category_name text,color text,amount real, Date text,Week INTEGER)" )
    c.execute("CREATE TABLE IF NOT EXISTS username(name text)")
    return conn

def check_username():
    conn=ConnectToDatabase()
    c=conn.cursor()
    c.execute("SELECT * FROM username")
    items=c.fetchall()
    conn.close()
    if len(items)==0:
        return True
    else:
        return False

def submit_username(name):
    conn=ConnectToDatabase()
    c=conn.cursor()
    c.execute("INSERT INTO username VALUES(?)",(name,))
    conn.commit()
    conn.close()

def get_username():
    conn=ConnectToDatabase()
    c=conn.cursor()
    c.execute("SELECT * FROM username")
    name=c.fetchone()
    name=name[0]
    return name

def show_all_categories():
    conn=ConnectToDatabase()
    c=conn.cursor()
    c.execute("SELECT * FROM categories ")
    items=c.fetchall()
    conn.close()
    return items

def insert_category(cat : str, color:str):
    conn=ConnectToDatabase()
    c=conn.cursor()
    c.execute("INSERT INTO categories VALUES (?,?)",(cat,color))
    conn.commit()
    conn.close()

def delete_category(cat:str,color:str):
    conn=ConnectToDatabase()
    c=conn.cursor()
    c.execute("DELETE FROM categories WHERE category_name=(?) AND color=(?)",(cat,color))
    c.execute("DELETE FROM expenses WHERE category_name=(?)",(cat,))
    conn.commit()
    conn.close()

def edit_category(old_cat,new_cat):
    conn=ConnectToDatabase()
    #(categoryname,color)
    c=conn.cursor()
    c.execute("UPDATE categories SET category_name=(?),color=(?) WHERE category_name=(?) AND color=(?)",new_cat+old_cat)
    c.execute("UPDATE expenses SET category_name = (?) WHERE category_name=(?)",(new_cat[0],old_cat[0]))
    conn.commit()
    conn.close()
#edit_category(ConnectToDatabase(),('ree','#0000FF'),('FREE','#000000'))

def show_daily_expense(date:str):
    conn=ConnectToDatabase()
    c=conn.cursor()
    c.execute("SELECT * FROM expenses WHERE Date=(?) ORDER BY amount DESC",(date,))
    items=c.fetchall()
    conn.close()
    return items

def show_categorywise_daily_expense(date:str):
    conn=ConnectToDatabase()
    c=conn.cursor()
    c.execute("SELECT * FROM expenses WHERE Date=(?) ORDER BY amount DESC",(date,))
    items=c.fetchall()
    conn.close()
    cat_dict={}
    for cat,clr,amt,d,w in items:
        if cat in cat_dict:
            cat_dict[cat][0]+=amt
        else:
            cat_dict[cat]=[amt,clr]
    cat_dict=dict(sorted(cat_dict.items(),key=lambda x:x[1][0],reverse=True))
    return cat_dict

def show_weekly_expense(Week:int):
    conn=ConnectToDatabase()
    c=conn.cursor()
    c.execute("SELECT * FROM expenses WHERE Week=(?) ORDER BY amount DESC",(Week,))
    items=c.fetchall()
    conn.close()
    cat_dict={}
    for cat,clr,amt,d,w in items:
        if cat in cat_dict:
            cat_dict[cat][0]+=amt
        else:
            cat_dict[cat]=[amt,clr]
    cat_dict=dict(sorted(cat_dict.items(),key=lambda x:x[1][0],reverse=True))
    return cat_dict

def show_monthly_expense(monthyr:str):
    conn=ConnectToDatabase()
    # month=(mm,yyyy) or "mm yyyy"
    c=conn.cursor()
    c.execute("SELECT * FROM expenses WHERE SUBSTR(Date,4,7)=(?) ORDER BY amount DESC",(monthyr,))
    items=c.fetchall()
    conn.close()
    cat_dict={}
    for cat,clr,amt,d,w in items:
        if cat in cat_dict:
            cat_dict[cat][0]+=amt
        else:
            cat_dict[cat]=[amt,clr]
    cat_dict=dict(sorted(cat_dict.items(),key=lambda x:x[1][0],reverse=True))
    return cat_dict

def insert_expense(data:tuple):
    conn=ConnectToDatabase()
    # data=(category_name,clr,amount,Date)
    data+=(get_week_no(data[2]),)
    clr=get_category_color(data[0])
    data=data[:1]+(clr,)+data[1:]
    c=conn.cursor()
    c.execute("INSERT INTO expenses VALUES(?,?,?,?,?)",data)
    conn.commit()
    conn.close()
# insert_expense(ConnectToDatabase(),('cat1',23,Date))

def delete_expense(data:tuple):
    conn=ConnectToDatabase()
    # data = (category_name,amount,date)
    c=conn.cursor()
    c.execute("SELECT rowid FROM expenses WHERE category_name=(?) AND amount=(?) AND Date=(?) LIMIT 1",data)
    id=c.fetchone()
    id=id[0]
    c.execute("DELETE FROM expenses WHERE rowid=(?)",(id,))
    conn.commit()
    conn.close()
# delete_expense(ConnectToDatabase(),('cat1',23,'08 04 2024'))

def edit_expense(data_old:tuple,data_new:tuple):
    conn=ConnectToDatabase()
    # data=(category_name,amount,Date)
    c=conn.cursor()
    c.execute("SELECT ROWID FROM expenses WHERE category_name=(?) AND amount=(?) AND Date=(?) LIMIT 1",data_old)
    id=c.fetchone()
    c.execute("UPDATE expenses SET category_name=(?),amount=(?),Date=(?) WHERE ROWID=(?)",data_new+id)
    conn.commit()
    conn.close()

def get_category_color(cat:str):
    conn=ConnectToDatabase()
    c=conn.cursor()
    c.execute("SELECT color FROM categories WHERE category_name=(?)",(cat,))
    a=c.fetchone()
    # a=list(a)
    conn.close()
    a=a[0]
    return a
def change_weeks():
    conn=ConnectToDatabase()
    c=conn.cursor()
    c.execute("SELECT Date FROM expenses")
    dates=c.fetchall()
    dates=[x[0] for x in dates]
    # print(dates)
    for date in dates:
        weekno=get_week_no(date)
        # print(weekno)
        c.execute("UPDATE expenses SET week=(?) WHERE Date=(?)",(weekno,date))
        conn.commit()
    conn.close()

def input_colors():
    conn=ConnectToDatabase()
    c=conn.cursor()
    c.execute("SELECT category_name FROM expenses")
    categories=c.fetchall()
    categories=set(x[0] for x in categories)
    for cat in categories:
        clr=get_category_color(cat)
        c.execute("UPDATE expenses SET color=(?) WHERE category_name=(?)",(clr,cat))
    conn.commit()
    conn.close()

def sumofday(date):
    conn=ConnectToDatabase()
    c=conn.cursor()
    c.execute("SELECT amount FROM expenses WHERE Date=(?)",(date,))
    items=c.fetchall()
    conn.close()
    if len(items)==0:
        return False
    daysum=sum(x[0] for x in items)
    return daysum

def sumofweek(weekno):
    conn=ConnectToDatabase()
    c=conn.cursor()
    c.execute("SELECT amount FROM expenses WHERE Week=(?)",(weekno,))
    items=c.fetchall()
    conn.close()
    weeksum=sum(x[0] for x in items)
    return weeksum

def sumofmonth(month):
    conn=ConnectToDatabase()
    c=conn.cursor()
    c.execute("SELECT amount FROM expenses WHERE SUBSTR(Date,4,7)=(?)",(month,))
    items=c.fetchall()
    conn.close()
    monthsum=sum(x[0] for x in items)
    return monthsum
# input_colors()
# print(get_category_color(ConnectToDatabase(),"Cat1"))

# check_username(ConnectToDatabase())
# print(show_weekly_expense(ConnectToDatabase(),1))
