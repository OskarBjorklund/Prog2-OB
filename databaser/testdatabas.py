import mysql.connector
import tkinter as tk

mydb = mysql.connector.connect(
  host="localhost",
  user="root",  # s"tandardanvändarnamn för XAMPP
  password="",  # dito lösenord (en tom sträng)
  database="forum"  # byt namn om din databas heter något annat
)

class Gui:
  def __init__(self):

    self.root = tk.Tk()

    self.l1 = tk.Label(self.root, text = "Name:")
    self.l2 = tk.Label(self.root, text = "Password:")

    self.l1.grid(row = 0, column = 0, sticky = "W", pady = 2)
    self.l2.grid(row = 1, column = 0, sticky = "W", pady = 2)

    self.e1 = tk.Entry(self.root)
    self.e2 = tk.Entry(self.root)

    self.e1.grid(row = 0, column = 1, pady = 2)
    self.e2.grid(row = 1, column = 1, pady = 2)

    self.bt = tk.Button(self.root, text = "Confirm", command = self.send_info)
    
    self.bt.grid(row = 4, column = 0, columnspan = 2)

    self.bt2 = tk.Button(self.root, text = "Read", command = self.find_info)
    
    self.bt2.grid(row = 5, column = 0, columnspan = 2)

    self.root.mainloop()

  def send_info(self):
    mycursor = mydb.cursor()
    print("Uppkopplad till databasen!")
    sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
    val = (self.e1.get(), self.e2.get())
    print(val)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

  def find_info(self):
    mycursor = mydb.cursor()
    # Läsa från databasen
    mycursor.execute("SELECT * FROM user")
    myresult = mycursor.fetchall()
    for x in myresult:
      per = list(x)
    print(per)
    


gui = Gui()