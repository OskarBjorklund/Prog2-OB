import mysql.connector
import tkinter as tk

mydb = mysql.connector.connect(
  host="localhost",
  user="root",  # s"tandardanvändarnamn för XAMPP
  password="",  # dito lösenord (en tom sträng)
  database="co"  # byt namn om din databas heter något annat
)

class Gui:
  def __init__(self):

    self.root = tk.Tk()

    self.l1 = tk.Label(self.root, text = "Name:")
    self.l2 = tk.Label(self.root, text = "Address:")
    self.l3 = tk.Label(self.root, text = "City:")
    self.l4 = tk.Label(self.root, text = "Country:")

    self.l1.grid(row = 0, column = 0, sticky = "W", pady = 2)
    self.l2.grid(row = 1, column = 0, sticky = "W", pady = 2)
    self.l3.grid(row = 2, column = 0, sticky = "W", pady = 2)
    self.l4.grid(row = 3, column = 0, sticky = "W", pady = 2)

    self.e1 = tk.Entry(self.root)
    self.e2 = tk.Entry(self.root)
    self.e3 = tk.Entry(self.root)
    self.e4 = tk.Entry(self.root)

    self.e1.grid(row = 0, column = 1, pady = 2)
    self.e2.grid(row = 1, column = 1, pady = 2)
    self.e3.grid(row = 2, column = 1, pady = 2)
    self.e4.grid(row = 3, column = 1, pady = 2)

    self.bt = tk.Button(self.root, text = "Confirm", command = self.send_info)
    
    self.bt.grid(row = 4, column = 0, columnspan = 2)

    self.root.mainloop()

  def send_info(self):
    mycursor = mydb.cursor()
    print("Uppkopplad till databasen!")
    sql = "INSERT INTO users (name, address, city, country) VALUES (%s, %s, %s, %s)"
    val = (self.e1.get(), self.e2.get(), self.e3.get(), self.e4.get())
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

    # Läsa från databasen
    mycursor.execute("SELECT * FROM users")
    myresult = mycursor.fetchall()
    for x in myresult:
      print(x)


gui = Gui()