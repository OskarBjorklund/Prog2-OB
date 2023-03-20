import mysql.connector
import tkinter as tk

mydb = mysql.connector.connect(
  host="localhost",
  user="root",  # s"tandardanvändarnamn för XAMPP
  password="",  # dito lösenord (en tom sträng)
  database="co"  # byt namn om din databas heter något annat
)
mycursor = mydb.cursor()
print("Uppkopplad till databasen!")

# Skriva till databasen
sql = "INSERT INTO users (name, address, city, country) VALUES (%s, %s, %s, %s)"
val = ("Karl Rosengren", "Slånbärsstigen 19", "Åkersberga", "Sweden")
#mycursor.execute(sql, val)
#mydb.commit()
print(mycursor.rowcount, "record inserted.")

# Läsa från databasen
mycursor.execute("SELECT * FROM users")
myresult = mycursor.fetchall()
for x in myresult:
  print(x)

class Gui:
  def __init__(self):
    self.window = tk.Tk()

    self.textbox1 = tk.Text(self.window, font=("Arial", 16))
    self.textbox1.grid(row=0, column=1)

    self.textbox2 = tk.Text(self.window, font=("Arial", 16))
    self.textbox2.grid(row=1, column=1)

    self.textbox3 = tk.Text(self.window, font=("Arial", 16))
    self.textbox3.grid(row=2, column=1)

    self.textbox4 = tk.Text(self.window, font=("Arial", 16))
    self.textbox4.grid(row=3, column=1)

    self.textbox5 = tk.Text(self.window, font=("Arial", 16))
    self.textbox5.grid(row=4, column=1)

    self.window.mainloop()

gui = Gui()