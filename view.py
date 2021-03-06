import pymysql
import tkinter
from pymysql import cursors
from selenium import webdriver
from tkinter import ttk
from selenium.webdriver import FirefoxProfile
from tkinter import messagebox

class Bms:
    def __init__(self):
        self.conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        password='hwh003561',
        database='bms1',
        charset='utf8'
        )
        self.cursor = self.conn.cursor(cursor=cursors.DictCursor) 
        
    
    def get_insert(self):
        option = FirefoxProfile()
        option.set_preference('dom.webdriver.enabled', False)
        self.bro = webdriver.Firefox(executable_path='D:\python39\geckodriver.exe', firefox_profile=option)
        self.bro.get(url='http://opac.nlc.cn/F/B2LYQVUJH7V1LX1Q879MVTBI6FSA3XR8QTFMLLTCE1I6DSNA8G-84640?func=file&file_name=login-session')
        isbn_option = self.bro.find_element_by_xpath('/html/body/div[4]/form/div[1]/table/tbody/tr/td[1]/span[2]/select/option[16]')
        isbn_option.click()
        isbn_research = self.bro.find_element_by_xpath('//*[@id="reqterm"]')
        isbn_research.send_keys(self.ISBN)
        isbn_click = self.bro.find_element_by_xpath('/html/body/div[4]/form/div[2]/input')
        isbn_click.click()
        self.author = self.bro.find_element_by_xpath()
        self.author = self.author.text
        self.publishtime = self.bro.find_element_by_xpath('/html/body/div[6]/table[2]/tr/td/div[3]/table/tr[5]/td[2]/a').gettext()
        self.publishtime = self.publishtime.split(',')[-1]
        self.type = self.bro.find_element_by_xpath('/html/body/div[6]/table[2]/tr/td/div[3]/table/tr[11]/td[2]/a').gettext()
        self.bro.quit()
        number = 1
        try:
            self.cursor.execute(u'select bookName from booklist where ISBN="%s"'%str(self.ISBN))
            bookName = self.cursor.fetchall()
            bookName = bookName[0][0]
        except Exception as e:
            self.conn.rollback()
        if self.Title == bookName:
            try:
                self.cursor.execute(u'select number from booklist where ISBN="%s"'%str(self.ISBN))
                Number = self.cursor.fetchall()
                Number = Number[0][0]
                number = Number+number
                self.cursor.execute(u'update booklist set number=%d where ISBN="%s"'%(number, str(self.ISBN)))
                self.conn.commit()
            except Exception as e:
                self.conn.rollback()
            
        else:
            try:
                self.cursor.execute(u'insert into booklist values("%s", "%s", "%s", "%s", "%s", %d)'%(str(self.ISBN), self.Title, self.publishtime, self.author, self.type, number))
                self.conn.commit()
            except Exception as e:
                self.conn.rollback()

    def book_insert(self):
        self.root1 = tkinter.Tk()
        self.root1.title('????????????')
        self.root1.geometry('700x800')
        ISBN_name = tkinter.Label(self.root1, text='ISBN')
        ISBN_name.grid(row=0, column=0)
        ISBN_entry = tkinter.Entry(self.root1)
        ISBN_entry.grid(row=0, column=1)
        Title_name = tkinter.Label(self.root1, text='Title')
        Title_name.grid(row=1, column=0)
        Title_entry = tkinter.Entry(self.root1)
        Title_entry.grid(row=1, column=1)
        self.ISBN = ISBN_entry.get()
        self.Title = Title_entry.get()
        self.insert_exit_Button = tkinter.Button(self.root1, text='??????', command=self.exit_insert)
        self.insert_exit_Button.grid(row=2, column=0)
        self.insertButton = tkinter.Button(self.root1, text='??????', command=self.get_insert)
        self.insertButton.grid(row=2, column=1)
        self.root1.mainloop()
    
    def exit_insert(self):
        self.root1.quit()
        self.bms_in()
    
    def get_select(self):
        try:
            self.cursor.execute(u'select * from booklist where ISBN="%s" or bookName="%s"'%str(self.isbn, self.book))
            self.conn.commit()
            result = self.cursor.fetchall()
            number = 0
            tree = ttk.Treeview(self.root2)
            tree['columns'] = ['ISBN', 'bookName', 'publishtime', 'author', 'type', 'number']
            tree.pack()
            tree.heading('ISBN', text='ISBN')
            tree.heading('bookName', text='bookName')
            tree.heading('publishtime', text='publishtime')
            tree.heading('author', text='author')
            tree.heading('type', text='type')
            tree.heading('number', text='number')
            for res in result:
                tree.insert('', text=str(number+1), values=res)
                number += 1
        except Exception as e:
            self.conn.rollback()
    
    def book_select(self):
        self.root2 = tkinter.Tk()
        self.root2.title('????????????')
        ISBN_name = tkinter.Label(self.root2, text='ISBN')
        ISBN_name.grid(row=0, column=0)
        ISBN_entry = tkinter.Entry(self.root2)
        ISBN_entry.grid(row=0, column=1)
        book_label = tkinter.Label(self.root2, text='bookName')
        book_label.grid(row=1, column=0)
        book_entry = tkinter.Entry(self.root2)
        book_entry.grid(row=1, column=1)
        self.isbn = ISBN_entry.get()
        self.book = book_entry.get()
        self.select_exit_Button = tkinter.Button(self.root2, text='??????', command=self.exit_select())
        self.select_exit_Button.grid(row=1, column=0)
        self.selectbutton = tkinter.Button(self.root2, text='??????', command=self.get_select(self.isbn))
        self.selectbutton.grid(row=1, column=1)
        self.root2.mainloop()
    
    def exit_select(self):
        self.root2.quit()
        self.bms_in()
    
    def adimit_bms_in(self):
        self.root = tkinter.Tk()
        self.root.title('???????????????')
        selectButton = tkinter.Button(self.root, text='??????', command=self.book_select)
        selectButton.pack(side=tkinter.LEFT)
        insertButton = tkinter.Button(self.root, text='??????', command=self.book_insert)
        insertButton.pack(side=tkinter.RIGHT)
        self.root.quit()
        self.root.mainloop()

    def login(self):
        self.root3 = tkinter.Tk()
        self.root3.title('????????????')
        username_Label = tkinter.Label(self.root3, text="username")
        username_Label.grid(row=0, column=0)
        username_Entry = tkinter.Entry(self.root3)
        username_Entry.grid(row=0,column=1)
        username = username_Entry.get()
        self.username = username
        Passord_label = tkinter.Label(self.root3, text='password')
        Passord_label.grid(row=1, column=0)
        passord_entry = tkinter.Entry(self.root3)
        passord_entry.grid(row=1, column=1)
        password = passord_entry.get()
        self.password = password
        login_exit_Button = tkinter.Button(self.root3, text='??????', command=self.exit_login)
        login_exit_Button.grid(row=2, column=0)

        def login_setting():
            try:
                self.cursor.execute(u'select username, password from userlist where username="%s"'%self.username)
                results = self.cursor.fetchall()
                userName = results[0][0]
                passWord = results[0][1]
            except Exception as e:
                self.conn.rollback()
            x = 0
            while x < 3:
                if self.username == 'root':
                    if password == 'hwh003561':
                        messagebox.showinfo(title='??????', message='????????????')
                        self.adimit_bms_in()
                        break
                    else:
                        messagebox.showwarning(title='??????', message="?????????????????????")
                elif self.username == userName or self.username==None:
                    if self.password == passWord:
                        messagebox.showinfo(title='??????', message='????????????')
                        self.book_select()
                        self.root3.quit()
                        break
                    else:
                        messagebox.showwarning(title='??????', message='?????????????????????')
                x += 1
                if x == 3:
                    self.exit_login()
        login_Button = tkinter.Button(self.root3, text='??????', command=login_setting)
        login_Button.grid(row=2,column=1)
        self.root3.mainloop()
    
    def bms_in(self):
        self.root5 = tkinter.Tk()
        self.root5.title('??????????????????')
        login_Button = tkinter.Button(self.root5, text='??????', command=self.login)
        login_Button.grid(row=0, column=0)
        setout_Button = tkinter.Button(self.root5, text='??????', command=self.setUp)
        setout_Button.grid(row=0, column=1)
        self.root5.quit()
        self.root5.mainloop()
    def exit_login(self):
        self.root3.quit()
        self.bms_in()
    def setUp(self):
        self.root4 = tkinter.Tk()
        self.root4.title('????????????')
        username_Label = tkinter.Label(self.root4, text='?????????')
        username_Label.grid(row=0, column=0)
        username_Entry = tkinter.Entry(self.root4)
        username_Entry.grid(row=0,column=1)
        password_Label = tkinter.Label(self.root4, text='??????')
        password_Label.grid(row=1,column=0)
        password_Entry = tkinter.Entry(self.root4)
        password_Label.grid(row=1,column=1)
        unit_Label = tkinter.Label(self.root4, text='??????')
        unit_Label.grid(row=2,column=0)
        unit_Entry = tkinter.Entry(self.root4)
        unit_Entry.grid(row=2, column=1)
        unit = unit_Entry.get()
        sex_Label = tkinter.Label(self.root4, text='??????')
        sex_Label.grid(row=3, column=0)
        sex_Entry = tkinter.Entry(self.root4)
        sex_Entry.grid(row=3, column=1)
        sex = sex_Entry.get()
        username = username_Entry.get()
        password = password_Entry.get()
        self.username = username
        self.password = password
        self.sex = sex
        self.unit = unit
        unit = unit_Entry.get()
        def setup_setting():
            try:
                self.cursor.execute(u'select username from userlist where username="%s"'%self.username)
                userName = self.cursor.fetchall()
                userName = userName[0][0]
            except Exception as e:
                self.conn.rollback()
            if self.username == userName:
                messagebox.showinfo(title='??????', message='?????????????????????')
            else:
                try:
                    self.cursor.execute(u'insert into userlist values("%s","%s","%s","%s")'%(username, password, sex, unit))
                    self.conn.commit()
                    self.exit_setup()
                except Exception as e:
                    self.conn.rollback()
        setup_Button = tkinter.Button(self.root4, text='??????', command=setup_setting)
        setup_Button.grid(row=4, column=0)
        exit_button = tkinter.Button(self.root4, text='??????')
        exit_button.grid(row=4, column=1)
        self.root4.mainloop()
    
    def exit_setup(self):
        self.root4.quit()
        self.bms_in()

if __name__ == '__main__':
    bms = Bms()
    bms.bms_in()
