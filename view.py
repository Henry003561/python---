import pymysql
import tkinter
from pymysql import cursors
from selenium import webdriver
from tkinter import Frame, ttk

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
        self.root = tkinter.Tk()
        self.root.geometry('800x700')
        self.root.title('图书管理系统')
    
    def get_detail_page(self, ISBN):
        self.bro = webdriver.Firefox(executable_path='D:\python39\geckodriver.exe')
        self.bro.get(url='http://opac.nlc.cn/F/B2LYQVUJH7V1LX1Q879MVTBI6FSA3XR8QTFMLLTCE1I6DSNA8G-84640?func=file&file_name=login-session')
        isbn_option = self.bro.find_element_by_xpath('/html/body/div[4]/form/div[1]/table//tr/td[1]/span[2]/select/option[16]')
        isbn_option.click()
        isbn_research = self.bro.find_element_by_xpath('//*[@id="reqterm"]')
        isbn_research.send_keys(ISBN)
        isbn_click = self.bro.find_element_by_xpath('/html/body/div[4]/form/div[2]/input')
        isbn_click.click()
        self.author = self.bro.find_element_by_xpath('/html/body/div[6]/table[2]//tr/td/div[3]/table//tr[13]/td[2]/a').getText()
        self.publishtime = self.bro.find_element_by_xpath('/html/body/div[6]/table[2]//tr/td/div[3]/table//tr[5]/td[2]/a').getText()
        self.publishtime = self.publishtime.split(',')[-1]
        self.type = self.bro.find_element_by_xpath('/html/body/div[6]/table[2]//tr/td/div[3]/table//tr[11]/td[2]/a').getText()
        self.type = self.type.split('--')[1]
        number = 1
        try:
            self.cursor.execute(u'select bookName from booklist where ISBN="%s"'%str(ISBN))
            bookName = self.cursor.fetchall()
            bookName = bookName[0][0]
        except Exception as e:
            self.conn.rollback()
        if self.Title == bookName:
            try:
                self.cursor.execute(u'select number from booklist where ISBN="%s"'%str(ISBN))
                Number = self.cursor.fetchall()
                Number = Number[0][0]
                number = Number+number
                self.cursor.execute(u'update booklist set number=%d where ISBN="%s"'%(number, str(ISBN)))
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
        self.root.quit()
        self.root1 = Frame(self.root)
        ISBN_name = tkinter.Label(self.root1, text='ISBN')
        ISBN_name.pack(side=tkinter.LEFT)
        ISBN_entry = tkinter.Entry(self.root1)
        ISBN_entry.pack(side=tkinter.RIGHT)
        Title_name = tkinter.Label(self.root1, text='Title')
        Title_name.pack(side=tkinter.LEFT)
        Title_entry = tkinter.Entry(self.root1)
        Title_entry.pack(side=tkinter.RIGHT)
        self.ISBN = self.ISBN_entry.get()
        self.Title = self.Title_entry.get()
        self.insert_exit_Button = tkinter.Button(self.root1, text='退出', command=self.exit_insert)
        self.insert_exit_Button.pack(side=tkinter.LEFT)
        self.insertButton = tkinter.Button(self.root1, text='录入', command=self.get_detail_page(self.ISBN))
        self.insertButton.pack(side=tkinter.RIGHT)
        self.root1.mainloop()
    
    def exit_insert(self):
        self.root1.quit()
        self.bms_in()
    
    def get_select(self, ISBN):
        try:
            self.cursor.execute(u'select * from booklist where ISBN="%s"'%str(ISBN))
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
        self.root.quit()
        self.root2 = tkinter.Frame(self.root)
        ISBN_name = tkinter.Label(self.root2, text='ISBN')
        ISBN_name.pack(side=tkinter.LEFT)
        ISBN_entry = tkinter.Entry(self.root2)
        ISBN_entry.pack(side=tkinter.RIGHT)
        self.isbn = ISBN_entry.get()
        self.select_exit_Button = tkinter.Button(self.root2, text='退出', command=self.exit_select())
        self.select_exit_Button.pack(side=tkinter.LEFT)
        self.selectbutton = tkinter.Button(self.root2, text='查询', command=self.get_select(self.isbn))
        self.selectbutton.pack(side=tkinter.RIGHT)
        self.root2.mainloop()
    
    def exit_select(self):
        self.root2.quit()
        self.bms_in()
    
    def bms_in(self):
        selectButton = tkinter.Button(self.root, text='查询', command=self.book_select)
        selectButton.pack(side=tkinter.LEFT)
        insertButton = tkinter.Button(self.root, text='录入', command=self.book_insert)
        insertButton.pack(side=tkinter.RIGHT)
        self.root.mainloop()

if __name__ == '__main__':
    bms = Bms()
    bms.bms_in()
# TODO重构代码
