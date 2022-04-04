from tkinter import *  # Only the classes the imported using asterisk *
from tkinter import messagebox  # messagebox is not a class, so we have to import separately
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generatePassword():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    num_letters = random.randint(8, 10)
    num_symbols = random.randint(2, 4)
    num_numbers = random.randint(2, 4)

    sample_list = []

    for letter in range(num_letters):
        sample_list.append(random.choice(letters))

    for symbol in range(num_symbols):
        sample_list.append(random.choice(symbols))

    for number in range(num_numbers):
        sample_list.append(random.choice(numbers))

    random.shuffle(sample_list)
    generated_pass = ''.join(sample_list)
    my_password.delete(0, END)
    my_password.insert(0, generated_pass)
    pyperclip.copy(generated_pass)  # To copy the generated password to our clipboard automatically


# ---------------------------- SAVE PASSWORD ------------------------------- #
def saveItem():
    website = my_website_name.get().lower()
    email_username = my_email_username.get()
    password = my_password.get()
    new_data = {
        website: {
            "email": email_username,
            "password": password,
        }
    }

    if len(website) == 0 or len(email_username) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops!", message="You cannot keep any field empty. Please try again!")
    else:
        is_ok = messagebox.askokcancel(title="Confirmation",
                                       message=f"You entered the following information:\n"
                                               f"Website: {website.title()}\n"
                                               f"Email/Username: {email_username}\n"
                                               f"Password: {password}\n"
                                               f"Is it ok to save ?")
        if is_ok:
            try:
                with open(file="data.json", mode='r') as FILE:
                    data = json.load(FILE)  # Load returns json as a dictionary

            except FileNotFoundError:
                with open(file="data.json", mode="w") as FILE:
                    json.dump(new_data, FILE, indent=4)

            else:
                data.update(new_data)  # update is a method for dictionaries
                with open(file="data.json", mode='w') as FILE:
                    json.dump(data, FILE, indent=4)

            finally:
                my_website_name.delete(0, END)
                my_password.delete(0, END)
                messagebox.showinfo(title="Done", message="Details added successfully")


# -------------------------- SEARCH PASSWORD ----------------------------- #
def searchItem():
    website = my_website_name.get()
    try:
        with open(file="data.json", mode='r') as FILE:
            data = json.load(FILE)
    except FileNotFoundError:
        messagebox.showwarning(title="Oops!", message="No data file found! Try adding some data and then searching.")
    else:
        if website.lower() in data:
            email_username = data[website.lower()]["email"]
            password = data[website.lower()]["password"]
            messagebox.showinfo(title=website.title(), message=f"Website: {website.title()}\n"
                                                               f"Email/Username: {email_username}\n"
                                                               f"Password: {password}")
        else:
            messagebox.showwarning(title="Oops!", message="No credentials found for requested website.")


# ---------------------------- UI SETUP ------------------------------- #
my_window = Tk()
my_window.title("Password Manager")
my_window.config(padx=50, pady=50)

my_canvas = Canvas(width=200, height=200, highlightthickness=0)
my_photo_img = PhotoImage(file="logo.png")
my_canvas.create_image(100, 100, image=my_photo_img)

my_website_name_label = Label(text="Website:")
my_email_username_label = Label(text="Email/Username:")
my_password_label = Label(text="Password:")

my_website_name = Entry(width=20)
my_website_name.focus()  # To put the cursor on the website field immediately after the app starts
my_email_username = Entry(width=35)
my_email_username.insert(0, "aritrabose2003@gmail.com")  # To pre-populate the entry with a default string
my_password = Entry(width=20)

my_search_button = Button(text="Search", width=11, command=searchItem)
my_generate_button = Button(text="Generate Password", width=11, command=generatePassword)
my_add_button = Button(text="Add", width=33, command=saveItem)

my_canvas.grid(column=1, row=0, sticky="EW")

my_website_name_label.grid(column=0, row=1, sticky="EW")
my_email_username_label.grid(column=0, row=2, sticky="EW")
my_password_label.grid(column=0, row=3, sticky="EW")

my_website_name.grid(column=1, row=1, sticky="EW")
my_email_username.grid(column=1, row=2, columnspan=2, sticky="EW")
my_password.grid(column=1, row=3, sticky="EW")

my_search_button.grid(column=2, row=1, sticky="EW")
my_generate_button.grid(column=2, row=3, sticky="EW")
my_add_button.grid(column=1, row=4, columnspan=2, sticky="EW")

my_window.mainloop()
