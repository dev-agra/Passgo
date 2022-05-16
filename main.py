import tkinter as tk
from tkinter import messagebox, END
from random import choice, randint, shuffle
import pyperclip
import json

password_no = 0


def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    pass_letters = [choice(letters) for _ in range(randint(8, 10))]
    pass_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    pass_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = pass_letters + pass_numbers + pass_symbols
    shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)


def safe_data():
    global password_no
    password_no += 1
    website_data = website_entry.get()
    email_data = email_entry.get()
    password_data = password_entry.get()

    # Format of data, so it is easier to store in the .JSON file
    new_data = {
        website_data: {
            "email": email_data,
            "password": password_data,
        }
    }

    response = messagebox.askyesno(title=f"Confirm data", message=f"{website_data}\n{email_data}\n{password_data}")
    if response:
        if len(website_data) == 0 or len(password_data) == 0:
            messagebox.showinfo(title="Error", message="Required Fields left empty!")
        else:
            try:
                with open("data.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
    else:
        exit()


def search_password():
    website_data = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Website found!")
    else:
        if website_data in data:
            email_data = data[website_data]["email"]
            password_data = data[website_data]["password"]
            messagebox.showinfo(title=f'{website_data}',
                                message=f'email/username: {email_data}\npassword: {password_data}')
        else:
            messagebox.showinfo(title="Error", message="No Website found!")


# ----------------------------------------------------------------------------------------------------------------------#

window = tk.Tk()
window.title("Passgo")
window.config(padx=20, pady=20, bg='white')
window.minsize(640, 610)  # Window measurement

canvas = tk.Canvas(width=370, height=380, background='white', highlightthickness=0)  # Canvas Measurement
lock_image = tk.PhotoImage(file="lock3.png")
canvas.create_image(185, 200, image=lock_image)  # Handles position of the image within the canvas
canvas.grid(row=0, column=1)

website_label = tk.Label(text="Website:", font=("Bahnschrift", 15), bg='white')
website_label.grid(row=1, column=0)

email_label = tk.Label(text="Username:", font=("Bahnschrift", 15), bg='white', pady=5)
email_label.grid(row=2, column=0)

password_label = tk.Label(text="Password:", font=("Bahnschrift", 15), bg='white')
password_label.grid(row=3, column=0)

website_entry = tk.Entry(width=50)
website_entry.grid(row=1, column=1, columnspan=1)
website_entry.focus()

email_entry = tk.Entry(width=50)
email_entry.grid(row=2, column=1, columnspan=1)

password_entry = tk.Entry(width=50, fg='black')
password_entry.grid(row=3, column=1, columnspan=1)

search_button = tk.Button(text="Search", font=("courier", 12, 'bold'), fg='black', bg='white', command=search_password)
search_button.grid(row=1, column=2)

gen_pass_button = tk.Button(text="Generate", font=("courier", 12, 'bold'), fg='black', bg='white',
                            command=generate_password)
gen_pass_button.grid(row=3, column=2)

add_button = tk.Button(text="Add", font=("courier", 12, 'bold'), fg='black', bg='white', width=20, command=safe_data)
add_button.grid(row=4, column=1)

window.mainloop()
