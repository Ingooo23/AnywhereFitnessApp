from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import random
import ast
import os
from datetime import datetime

app = Tk()
app.title("AnywhereFitness")
app.geometry("800x600")
app.resizable(False, False)

bg_img_raw = Image.open("AnywhereFitness.png")
background_image = ImageTk.PhotoImage(bg_img_raw)

def add_background(frame):
    bg = Label(frame, image=background_image)
    bg.place(x=0, y=0, relwidth=1, relheight=1)
    bg.lower()

BG_COLOR = "#004aad"
FG_COLOR = "white"

btn_style = {
    "bg": "white",
    "fg": "black",
    "relief": "flat",
    "font": ("Arial", 14),
    "width": 20
}

entry_style = {
    "bg": "white",
    "fg": "black",
    "insertbackground": FG_COLOR,
    "relief": "flat",
    "font": ("Arial", 14),
    "width": 20
}

label_style = {
    "bg": BG_COLOR,
    "fg": FG_COLOR
}


current_user_id = None
file_path = "ID_List.txt"

gym_data = {
    "North": {"capacity": 50, "inside": {}},
    "South": {"capacity": 30, "inside": {}},
    "East": {"capacity": 100, "inside": {}}
}

gym_machines = {
    "North": {"bench press": 3, "lat pulldown": 2, "leg press": 2, "treadmill": 5, "rowing machine": 2},
    "South": {"bench press": 2, "pull-up bar": 3, "leg extension": 2, "treadmill": 3, "chest fly": 1},
    "East": {"bench press": 4, "seated row": 3, "leg curl": 2, "elliptical": 2, "dumbbells": 10}
}

muscle_groups = {
    "Chest": ["bench press", "chest fly", "dumbbells"],
    "Back": ["lat pulldown", "seated row", "pull-up bar", "rowing machine"],
    "Legs": ["leg press", "leg extension", "leg curl"],
    "Cardio": ["treadmill", "rowing machine", "elliptical"]
}

reservations = []



trainers = {
    "North": [
        {"name": "Maps", "specialties": ["Lose Weight", "Cardio"], "available_times": [(14, 18)]},
        {"name": "Foco", "specialties": ["Strength Training", "Bodybuilding"], "available_times": [(10, 16)]},
        {"name": "Mix", "specialties": ["Strength Training", "Bodybuilding", "Cardio", "Lose Weight"], "available_times": [(7, 18)]}
    ],
    "South": [
        {"name": "Rovic", "specialties": ["Mobility", "Lose Weight"], "available_times": [(7, 13)]},
        {"name": "Derek", "specialties": ["Strength Training"], "available_times": [(12, 19)]},
        {"name": "Inigo", "specialties": ["Cardio", "Endurance"], "available_times": [(8, 16)]}
    ],
    "East": [
        {"name": "Tynic", "specialties": ["Lose weight", "Strength training"], "available_times": [(6, 12)]},
        {"name": "Libuano", "specialties": ["Cardio", "Endurance"], "available_times": [(10, 14)]},
                {"name": "Keel", "specialties": ["Mobility", "Cardio", "Lose Weight"], "available_times": [(12, 14)]}
    ]
}

def is_available_later(trainer):
    now = datetime.now().hour
    for start, end in trainer["available_times"]:
        if end > now:
            return True
    return False

def get_available_trainers(branch, goal):
    branch_trainers = trainers.get(branch, [])
    return [t["name"] for t in branch_trainers if goal in t["specialties"] and is_available_later(t)]

def schedule_session(branch, coach_name, desired_hour):
    for trainer in trainers.get(branch, []):
        if trainer["name"].lower() == coach_name.lower():
            for start, end in trainer["available_times"]:
                if start <= desired_hour < end:
                    return f"✅ Session booked with {coach_name} at {branch} at {desired_hour}:00."
            return f"⛔ {coach_name} is not available at {desired_hour}:00 in {branch}."
    return f"❌ Coach {coach_name} not found in {branch}."

def get_user_booking(branch, trainer, hour):
    for r in reservations:
        if r["user_id"] == current_user_id and r["branch"] == branch and r["trainer"] == trainer and r["hour"] == hour:
            return r
    return None



def create_frame():
    f = Frame(app, width=800, height=600, bg=BG_COLOR)
    f.place(x=0, y=0)
    add_background(f)
    return f


mainmenu = create_frame()
signup = create_frame()
login = create_frame()
member = create_frame()
capacity_page = create_frame()
machine_page = create_frame()
coach_page = create_frame()



def save_users(users):
    with open(file_path, "w") as f:
        for user in users:
            f.write(f"{user}\n")

def load_users():
    try:
        with open(file_path, "r") as f:
            return [ast.literal_eval(line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        return []

def save_gym_capacity_data():
    with open("GymCapacityList.txt", "w") as f:
        for branch in gym_data:
            ids_inside = list(gym_data[branch]["inside"].keys())
            f.write(f"{branch}: {ids_inside}\n")

def load_gym_capacity_data():
    if not os.path.exists("GymCapacityList.txt"):
        return
    with open("GymCapacityList.txt", "r") as f:
        for line in f:
            if ':' in line:
                branch, ids = line.strip().split(":", 1)
                ids_list = ast.literal_eval(ids.strip())
                gym_data[branch.capitalize()]["inside"] = {str(i): True for i in ids_list}

def get_machines_for_muscles(branch, selected_muscle):
    available = gym_machines.get(branch, {})
    result = {}
    machines = muscle_groups.get(selected_muscle, [])
    for machine in machines:
        if machine in available:
            result[machine] = available[machine]
    return result


Label(mainmenu, text="Welcome to the AnywhereFitness App", font=("Arial", 26), **label_style).place(relx=0.5, rely=0.23, anchor="center")
Button(mainmenu, text="Sign Up", command=lambda: signup.tkraise(), **btn_style).place(relx=0.5, rely=0.4, anchor="center")
Button(mainmenu, text="Log In", command=lambda: login.tkraise(), **btn_style).place(relx=0.5, rely=0.5, anchor="center")


Label(signup, text="Sign Up Page", font=("Arial", 24), **label_style).place(relx=0.5, rely=0.2, anchor="center")
Label(signup, text="Choose Your Password", **label_style).place(relx=0.5, rely=0.3, anchor="center")
signup_pw_entry = Entry(signup, show="*", **entry_style)
signup_pw_entry.place(relx=0.5, rely=0.35, anchor="center")

def register_user():
    password = signup_pw_entry.get()
    users = load_users()
    existing_ids = {user["id"] for user in users}
    while True:
        user_id = random.randint(10000, 19999)
        if user_id not in existing_ids:
            break
    new_user = {"id": user_id, "password": password}
    users.append(new_user)
    save_users(users)
    messagebox.showinfo("Registration Complete", f"Your ID: {user_id}")
    login.tkraise()

Button(signup, text="Register", command=register_user, **btn_style).place(relx=0.5, rely=0.45, anchor="center")
Button(signup, text="Go Back", command=lambda: mainmenu.tkraise(), **btn_style).place(relx=0.5, rely=0.525, anchor="center")


Label(login, text="Login Page", font=("Arial", 20), **label_style).place(relx=0.5, rely=0.2, anchor="center")

id_entry = Entry(login, **entry_style)
id_entry.place(relx=0.5, rely=0.3, anchor="center")
id_entry.insert(0, "Enter ID")
def clear_id_placeholder(event):
    if id_entry.get() == "Enter ID":
        id_entry.delete(0, END)

id_entry.bind("<FocusIn>", clear_id_placeholder)

pw_entry = Entry(login, show="*", **entry_style)
pw_entry.place(relx=0.5, rely=0.35, anchor="center")

def clear_pw_placeholder(event):
    if pw_entry.get() == "Password":
        pw_entry.delete(0, END)
        pw_entry.config(show="*")

def restore_pw_placeholder(event):
    if pw_entry.get() == "":
        pw_entry.insert(0, "Password")
        pw_entry.config(show="")

pw_entry.insert(0, "Password")
pw_entry.config(show="")
pw_entry.bind("<FocusIn>", clear_pw_placeholder)
pw_entry.bind("<FocusOut>", restore_pw_placeholder)


def submit_login():
    global current_user_id
    user_id = id_entry.get()
    password = pw_entry.get()
    users = load_users()
    for user in users:
        if str(user["id"]) == user_id and str(user["password"]) == password:
            current_user_id = user_id
            messagebox.showinfo("Login Success", f"Logged in as {user_id}")
            member.tkraise()
            return
    messagebox.showerror("Login Failed", "Invalid ID or Password")

Button(login, text="Submit", command=submit_login, **btn_style).place(relx=0.5, rely=0.45, anchor="center")
Button(login, text="Go Back", command=lambda: mainmenu.tkraise(), **btn_style).place(relx=0.5, rely=0.525, anchor="center")


Label(member, text="Member Dashboard", font=("Arial", 24), **label_style).place(relx=0.5, rely=0.2, anchor="center")
Button(member, text="View Gym Capacity", command=lambda: [capacity_page.tkraise(), show_capacity(branch_var.get())], **btn_style).place(relx=0.5, rely=0.35, anchor="center")
Button(member, text="View Machines", command=lambda: machine_page.tkraise(), **btn_style).place(relx=0.5, rely=0.45, anchor="center")
Button(member, text="Book a Coach", command=lambda: [coach_page.tkraise(), build_schedule_table()], **btn_style).place(relx=0.5, rely=0.55, anchor="center")
Button(member, text="Log Out", command=lambda: mainmenu.tkraise(), **btn_style).place(relx=0.5, rely=0.65, anchor="center")



Label(capacity_page, text="Gym Capacity Tracker", font=("Arial", 20), **label_style).place(relx=0.5, rely=0.15, anchor="center")
Label(capacity_page, text="Select Branch:", **label_style).place(relx=0.5, rely=0.25, anchor="center")

branch_var = StringVar(value="North")
OptionMenu(capacity_page, branch_var, "North", "South", "East").place(relx=0.5, rely=0.3, anchor="center")

label_result = Label(capacity_page, text="", font=("Arial", 14), **label_style)
label_result.place(relx=0.5, rely=0.45, anchor="center")


Button(capacity_page, text="Tap In", width=10, command=lambda: tap_in_out(branch_var.get(), "in")).place(relx=0.6, rely=0.37, anchor="center")
Button(capacity_page, text="Tap Out", width=10, command=lambda: tap_in_out(branch_var.get(), "out")).place(relx=0.4, rely=0.37, anchor="center")


Button(capacity_page, text="Back", command=lambda: member.tkraise(), **btn_style).place(relx=0.5, rely=0.55, anchor="center")


def show_capacity(branch):
    branch = branch.capitalize()
    current = sum(1 for _ in gym_data[branch]["inside"])
    capacity = gym_data[branch]["capacity"]
    percent = (current / capacity) * 100
    label_result.config(text=f"{branch.title()} Branch:\nCurrent: {current} / Max: {capacity} ({percent:.0f}% full)")


def tap_in_out(branch, action):
    global current_user_id
    branch = branch.capitalize()
    if branch not in gym_data or not current_user_id:
        messagebox.showerror("Error", "Invalid branch or not logged in.")
        return
    cid = str(current_user_id)
    if action == "in":
        gym_data[branch]["inside"][cid] = True
    elif action == "out" and cid in gym_data[branch]["inside"]:
        del gym_data[branch]["inside"][cid]
    save_gym_capacity_data()
    show_capacity(branch)


Label(machine_page, text="Machine Availability", font=("Arial", 20), **label_style).place(relx=0.5, rely=0.2, anchor="center")
Label(machine_page, text="Select Branch:", **label_style).place(relx=0.5, rely=0.27, anchor="center")
machine_branch_var = StringVar(value="North")
machine_branch_var.trace("w", lambda *args: show_machines())
OptionMenu(machine_page, machine_branch_var, "North", "South", "East").place(relx=0.5, rely=0.32, anchor="center")

Label(machine_page, text="Select Muscle Group:", **label_style).place(relx=0.5, rely=0.37, anchor="center")
muscle_var = StringVar(value="Chest")
muscle_var.trace("w", lambda *args: show_machines())
OptionMenu(machine_page, muscle_var, "Chest", "Back", "Legs", "Cardio").place(relx=0.5, rely=0.42, anchor="center")

machine_output_frame = Frame(machine_page, bg="#004aad")



left_frame = Frame(machine_output_frame, bg="#004aad")
left_frame.grid(row=0, column=0, padx=50, sticky="n")

machine_result_left = Label(left_frame, text="", bg="#004aad", fg="white", font=("Arial", 12), justify=LEFT)


right_frame = Frame(machine_output_frame, bg="#004aad")
right_frame.grid(row=0, column=1, padx=50, sticky="n")

machine_result_right = Label(right_frame, text="", bg="#004aad", fg="white", font=("Arial", 12), justify=LEFT)

all_machines_label = Label(left_frame, text="All Machines", font=("Arial", 14, "bold"), bg="#004aad", fg="white")
recommended_label = Label(right_frame, text="Recommended Machines", font=("Arial", 14, "bold"), bg="#004aad", fg="white")

def show_machines():
    branch = machine_branch_var.get()
    muscle = muscle_var.get()

    all_machines = gym_machines.get(branch, {})
    filtered_machines = get_machines_for_muscles(branch, muscle)

    left_text = f"{branch.title()} Branch:\n"
    if all_machines:
        for m, qty in all_machines.items():
            left_text += f"- {m}: {qty} available\n"
    else:
        left_text += "No machines available."

    right_text = f"For {muscle.title()}:\n"
    if filtered_machines:
        for m, qty in filtered_machines.items():
            right_text += f"- {m}: {qty} available\n"
    else:
        right_text += "None available."

    machine_result_left.config(text=left_text)
    machine_result_right.config(text=right_text)


    machine_output_frame.place(relx=0.5, rely=0.56, anchor="center")


    all_machines_label.pack(anchor="w")
    recommended_label.pack(anchor="w")
    machine_result_left.pack(anchor="w")
    machine_result_right.pack(anchor="w")


Button(machine_page, text="Back", command=lambda: member.tkraise(), **btn_style).place(relx=0.5, rely=0.8, anchor="center")



Label(coach_page, text="Coach Booking", font=("Arial", 24), **label_style).place(relx=0.5, rely=0.1, anchor="center")

Label(coach_page, text="Select Branch:", **label_style).place(relx=0.3, rely=0.175, anchor="e")
coach_branch_var = StringVar(value="North")
def refresh_goal_options(branch):
    branch_trainers = trainers.get(branch, [])
    all_specialties = set()
    for trainer in branch_trainers:
        all_specialties.update(trainer["specialties"])


    goal_menu["menu"].delete(0, "end")
    for specialty in sorted(all_specialties):
        goal_menu["menu"].add_command(label=specialty, command=lambda v=specialty: on_goal_select(v))

    if all_specialties:
        goal_var.set(sorted(all_specialties)[0])
    else:
        goal_var.set("")

def on_branch_select(*args):
    branch = coach_branch_var.get()
    refresh_goal_options(branch)
    build_schedule_table()

def on_goal_select(selected_goal):
    goal_var.set(selected_goal)
    build_schedule_table()

coach_branch_var = StringVar(value="North")
coach_branch_var.trace("w", on_branch_select)

branch_menu = OptionMenu(coach_page, coach_branch_var, "North", "South", "East")
branch_menu.place(relx=0.3, rely=0.175, anchor="w")


Label(coach_page, text="Select Fitness Goal:", **label_style).place(relx=0.625, rely=0.175, anchor="e")
goal_var = StringVar()
goal_menu = OptionMenu(coach_page, goal_var, "")
goal_menu.place(relx=0.625, rely=0.175, anchor="w")

available_label = Label(coach_page, text="", font=("Arial", 12), **label_style)
available_label.place(relx=0.5, rely=0.45, anchor="center")

schedule_frame = Frame(coach_page, bg="white")
schedule_frame.place(relx=0.5, rely=0.52, anchor="center")

selected_slot = {
    "branch": None,
    "trainer": None,
    "hour": None,
    "widget": None 
}

def cell_click(event, hour, trainer_name, cell):
    if selected_slot["widget"]:
        prev = selected_slot["widget"]
        prev_bg = prev.default_bg if hasattr(prev, "default_bg") else "green"
        prev.config(bg=prev_bg)

    selected_slot["hour"] = hour
    selected_slot["trainer"] = trainer_name
    selected_slot["widget"] = cell

    cell.default_bg = cell.cget("bg")
    cell.config(bg="gold")


def build_schedule_table():
    for widget in schedule_frame.winfo_children():
        widget.destroy()
    selected_slot["trainer"] = selected_slot["hour"] = selected_slot["widget"] = None

    branch = coach_branch_var.get()
    selected_slot["branch"] = branch
    goal = goal_var.get()
    all_trainers = trainers.get(branch, [])
    trainers_list = [t for t in all_trainers if goal in t["specialties"]]

    if not trainers_list:
        Label(schedule_frame, text="No trainers for this branch.", **label_style).pack()
        return

    hours = list(range(6, 19))

    ttk.Label(schedule_frame, text="Time", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
    for col, trainer in enumerate(trainers_list, start=1):
        name = trainer["name"]
        specialties = ", ".join(trainer["specialties"])
        ttk.Label(schedule_frame, text=f"{name}\n({specialties})", font=("Arial", 10), justify="center", background="lightblue").grid(row=0, column=col, padx=5, pady=5)


    for row, hour in enumerate(hours, start=1):
        ttk.Label(schedule_frame, text=f"{hour}:00", font=("Arial", 10)).grid(row=row, column=0, padx=5, pady=2)

        for col, trainer in enumerate(trainers_list, start=1):
            trainer_name = trainer["name"]
            available = any(start <= hour < end for start, end in trainer["available_times"])

            booked = None
            slot_reservations = [
                r for r in reservations
                if r["branch"] == branch and r["trainer"] == trainer_name and r["hour"] == hour
            ]
            count = len(slot_reservations)

            if count >= 4:
                label = Label(schedule_frame, text="Full", bg="gray", fg="white", width=9)
            elif available:
                if any(r["user_id"] == current_user_id for r in slot_reservations):
                    label = Label(schedule_frame, text="Reserved", bg="blue", fg="white", width=9)
                    label.bind("<Button-1>", lambda e, h=hour, t=trainer_name, w=label:
                            prompt_cancel(get_user_booking(branch, trainer_name, hour), w))
                else:
                    label = Label(schedule_frame, text="Available", bg="green", fg="white", width=9)
                    label.bind("<Button-1>", lambda e, h=hour, t=trainer_name, w=label:
                            cell_click(e, h, t, w))
            else:
                label = Label(schedule_frame, text="Unavailable", bg="grey", fg="white", width=9)

            label.grid(row=row, column=col, padx=5, pady=2, sticky="nsew")

def prompt_cancel(booking, widget):
    confirm = messagebox.askyesno("Cancel Booking", f"Cancel booking with {booking['trainer']} at {booking['hour']}:00?")
    if confirm:
        reservations.remove(booking)

        try:
            with open("Schedule.txt", "w") as f:
                for r in reservations:
                    f.write(str(r) + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update file: {e}")
            return

        widget.config(bg="green", text="Available")
        widget.default_bg = "green"
        widget.bind("<Button-1>", lambda e, h=booking["hour"], t=booking["trainer"], w=widget: cell_click(e, h, t, w))

        messagebox.showinfo("Cancelled", "Reservation cancelled.")

def book_selected_slot():
    b = selected_slot["branch"]
    t = selected_slot["trainer"]
    h = selected_slot["hour"]
    g = goal_var.get()
    w = selected_slot["widget"]

    if not all([b, t, h is not None, g]):
        messagebox.showerror("Error", "Please select an available time slot and goal.")
        return


    for r in reservations:
        if (r["user_id"] == current_user_id and
            r["branch"] == b and
            r["trainer"] == t and
            r["hour"] == h):
            messagebox.showerror("Already Booked", "You have already reserved this slot.")
            return

    booking = {
        "user_id": current_user_id,
        "branch": b,
        "trainer": t,
        "hour": h,
        "goal": g
    }

    slot_count = sum(1 for r in reservations if r["branch"] == b and r["trainer"] == t and r["hour"] == h)
    if slot_count >= 4:
        messagebox.showerror("Slot Full", "This slot is already fully booked (4 people max).")
        return

    reservations.append(booking)

    try:
        with open("Schedule.txt", "a") as f:
            f.write(str(booking) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save booking: {e}")
        return

    messagebox.showinfo("Booking Confirmed", schedule_session(b, t, h))


    w.config(bg="blue", text="Reserved")
    w.bind("<Button-1>", lambda e: prompt_cancel(booking, w))
    selected_slot["widget"] = None 



Button(coach_page, text="Book Selected Slot", command=book_selected_slot, **btn_style).place(relx=0.5, rely=0.88, anchor="center")


Button(coach_page, text="Back", command=lambda: member.tkraise(), **btn_style).place(relx=0.5, rely=0.94, anchor="center")


def load_reservations():
    if os.path.exists("Schedule.txt"):
        with open("Schedule.txt", "r") as f:
            for line in f:
                try:
                    booking = ast.literal_eval(line.strip())
                    reservations.append(booking)
                except:
                    continue

refresh_goal_options(coach_branch_var.get())
build_schedule_table()

show_machines()
load_gym_capacity_data()
load_reservations()
mainmenu.tkraise()
app.mainloop()
