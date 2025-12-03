from tkinter import *
from tkinter import messagebox
from random import *
import json
import pyclip

FONT = ("Arial", 12, "normal")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def gen_pass():
    password_letters = [choice(letters) for item in range(randint(8, 10))]
    password_symbols = [choice(symbols) for item in range(randint(2, 4))]
    password_numbers = [choice(numbers) for item in range(randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = ''.join(password_list)

    print(password)
    input_password.delete(0, END)
    input_password.insert(0, password)
    pyclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def write_to_json_file(data_variable):
    with open('data.json', 'w') as file:
        json.dump(data_variable, file, indent=4)


def save_data():
    user = input_user.get()
    password1 = input_password.get()
    website = input_website.get()
    website = website.capitalize()

    if len(user) == 0 or len(password1) == 0 or len(website) == 0:
        messagebox.showerror(title="Error", message="Please fill all fields")
    else:
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"Details:\nEmail:  "
                                               f"{user}\n,Password: {password1}\n"
                                               f"Are you sure you want to save")

        if is_ok:
            new_data = {
                website: {
                    'email': user,
                    'password': password1,
                }
            }
            try:
                with open('data.json', 'r') as file:
                    data = json.load(file)  # Reading old data
            except FileNotFoundError:
                write_to_json_file(new_data)
            else:
                data.update(new_data)  # Updating old data with new data
                write_to_json_file(data)  # Saving the updated data
            finally:
                input_website.delete(0, END)
                input_password.delete(0, END)


# ---------------------------- Search ------------------------------- #
def search():
    website = input_website.get()
    website = website.capitalize()
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="File not found !")
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=website, message=f'Email : {email}\nPassword : {password}')
        else:
            messagebox.showerror(title="Error", message='Data Not Found !')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(window, width=200, height=200)
image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image)
canvas.grid(row=0, column=1)

# Labels
label_website = Label(text="Website:", font=FONT)
label_website.grid(row=1, column=0)

label_user = Label(text="Username/Email:", font=FONT)
label_user.grid(row=2, column=0)

label_password = Label(text="Password:", font=FONT)
label_password.grid(row=3, column=0)

# Inputs
input_website = Entry(width=35)
input_website.focus()
input_website.grid(row=1, column=1)

input_user = Entry(width=55)
input_user.insert(0, "example@gmail.com")
# input_password = Entry(width=35)
input_user.grid(row=2, column=1, columnspan=2)

input_password = Entry(width=35)
input_password.grid(row=3, column=1)

# Buttons
button_search = Button(text='Search', width=15, command=search)
button_search.grid(row=1, column=2)

button_gen_pass = Button(text='Generate Password', width=15, command=gen_pass)
button_gen_pass.grid(row=3, column=2)

button_add = Button(text='Add', width=46, command=save_data)
button_add.grid(row=4, column=1, columnspan=2)

window.mainloop()
