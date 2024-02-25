import os
import datetime

# Define global variables
users = {}
tasks = []

# Define the Task class
class Task:
    def __init__(self, username, title, description, due_date, completed=False):
        self.username = username
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed

    def __str__(self):
        status = "Completed" if self.completed else "Not Completed"
        return f"Title: {self.title}\nDescription: {self.description}\nDue Date: {self.due_date}\nStatus: {status}"

# Function to load user data from user.txt
def load_users():
    global users
    if os.path.exists("user.txt"):
        with open("user.txt", "r") as file:
            for line in file:
                username, password = line.strip().split(", ")
                users[username] = password
    return users
# Function to save user data to user.txt
def save_users():
    with open("user.txt", "w") as file:
        for username, password in users.items():
            file.write(f"{username}, {password}\n")

# Function to load task data from tasks.txt
def load_tasks():
    global tasks
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as file:
            for line in file:
                task_data = line.strip().split(", ")
                task = {
                    "assigned_user" : task_data[0],
                    "title" : task_data[1],
                    "description" : task_data[2],
                    "date_assigned" : task_data[3],
                    "due_date" : task_data[4],
                    "completed" : task_data[5]
                }
                tasks.append(task)
    return tasks

# Function to save task data to tasks.txt
def save_tasks():
    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(f"{task['assigned_user']}, {task['title']}, {task['description']}, {task['date_assigned']}, {task['due_date']}, {task['completed']}\n")

# Function to register a new user
def register_user():
    username = input("Enter a new username: ")
    if username in users:
        print("Username already exists. User registration failed.")
        return
    password = input("Enter a password: ")
    confirm_password = input("Confirm password: ")
    if password != confirm_password:
        print("Passwords do not match. User registration failed.")
        return
    users[username] = password
    save_users()
    print("User registration successful.")

#Function to login in 
def login():
    while True:
        username = input("Enter your username (or type 'r' to register): ")
        if username.lower() == "r":
            register_user()
            continue
        if username not in users:
            print("Username not found. Please try again or type 'r' to register.")
            continue
        password = input("Enter your password: ")
        if users[username] != password:
            print("Incorrect password. Try again.")
            continue
        return username
        
# Function to add a new task
def add_task():
    assigned_user = input("Enter the username of the person the task is assigned to: ")
    title = input("Enter the title of the task: ")
    description = input("Enter a description of the task: ")
    due_date = input("Enter the due date(YYYY-MM-DD) of the task: ")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    table = {
        "assigned_user" : assigned_user,
        "title" : title,
        "description" : description,
        "date_assigned" : current_date,
        "due_date" : due_date,
        "completed" : "No"
    }
    tasks.append(table)
    save_tasks()
    print("Task added successfully.")

# Function to view all tasks
def view_all_tasks():
    tasks = load_tasks()
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. Title: {task['title']}")
        print(f"    Assigned to: {task['assigned_user']}")
        print(f"    Description: {task['description']}")
        print(f"    Due Date: {task['due_date']}")
        print(f"    Status: {'Completed' if task['completed'] == 'Yes' else 'Not Completed'}")
        print()

# Function to view tasks assigned to the current user
def view_my_tasks(username, tasks):
    print("\nView My Tasks")
    user_tasks = [task for task in tasks if task["assigned_user"] == username]
    
    if not user_tasks:
        print("No tasks assigned to you.")
        return
     
    for idx, task in enumerate(user_tasks, 1):
        print(f"\nTask {idx}:")
        print(f"Title: {task['title']}")
        print(f"Description: {task['description']}")
        print(f"Due Date: {task['due_date']}")
        print(f"Completed: {'Completed' if task['completed'] == 'Yes' else 'Not Completed'}")
        
    selected_task = input("\nEnter the number of the task to perfrom an action (or -1 to return to the main menu): ")
    if selected_task.isdigit() and 1 <= int(selected_task) <= len(user_tasks):
        selected_task = int(selected_task) - 1
        task = user_tasks[selected_task]
        action = input("Select an action: (1) Mark as Complete, (2) Edit Task, or (3) Cancel: ")
        
        if action == "1":
            task['completed'] = 'Yes'
            print("Task Marked as Completed")
        elif action == "2":
            edit_task(task, selected_task)
        elif action == "3":
            print("Task not modified.")
        else:
            print("Invalid choice. Task not modified.")

#Function to mark tasks as complete 
def mark_test_complete(tasks, task_index):
    tasks[task_index][5] = "Yes"
    write_tasks(tasks)
    print("Task Marked as completed.")
    
#Function to edit a task, add a due date and a user
def edit_task(tasks, task_index):
    print("Select what you want to edit:")
    print("1. Assigned User")
    print("2. Due Date")
    edit_choice = input("Enter your choice:")

    if edit_choice == "1":
        new_user = input("Enter the new assigned user: ")
        tasks[task_index][0] = new_user
    elif edit_choice == "2":
        new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
        tasks[task_index][4] = new_due_date
    else:
        print("Invalid choice.")
        return
    
    write_tasks(tasks)
    print('Task edited successfully')
    
# Function to generate reports
def generate_reports(users, tasks):
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task['completed'] == "Yes")
    uncompleted_tasks = total_tasks - completed_tasks
    
    overdue_tasks = sum(1 for task in tasks if task_has_ovderdue(task))
    task_percentage_incomplete = (uncompleted_tasks / total_tasks) * 100 if total_tasks != 0 else 0
    task_percentage_overdue = (overdue_tasks / uncompleted_tasks) * 100 if uncompleted_tasks != 0 else 0

    print(f"Total Tasks: {total_tasks}")
    print(f"Completed Tasks: {completed_tasks}")
    print(f"Uncompleted Tasks: {uncompleted_tasks}")
    print(f"Overdue Tasks: {overdue_tasks}")
    print(f"Incomplete Percentage: {task_percentage_incomplete:.2f}%")
    print(f"Overdue Percentage: {task_percentage_overdue:.2f}%")
    
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(f"Total Tasks: {total_tasks}\n")
        task_overview_file.write(f"Completed Tasks: {completed_tasks}\n")
        task_overview_file.write(f"Uncompleted Tasks: {uncompleted_tasks}\n")
        task_overview_file.write(f"Overdue Tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Incomplete Percentage: {task_percentage_incomplete:.2f}%\n")
        task_overview_file.write(f"Overdue Percentage: {task_percentage_overdue:.2f}%\n")

    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(f"Total Users : {len(users)}\n")
        user_overview_file.write(f"Total Tasks : {total_tasks}\n")
        
        for username in users:
            user_tasks = [task for task in tasks if task['assigned_user'] == username]
            total_user_tasks = len(user_tasks)
            completed_user_tasks = sum(1 for task in user_tasks if task['completed'] == "Yes")
            user_percentage_completed = (completed_user_tasks / total_user_tasks) * 100 if total_user_tasks != 0 else 0
            user_overview_file.write(f"\nUser: {username}\n")
            user_overview_file.write(f"Total tasks assigned: {total_user_tasks}\n")
            user_overview_file.write(f"Percentage of Tasks Completed: {user_percentage_completed}%\n")

# Function to display statistics
def display_statistics():
    if os.path.exists("task_overview.txt") and os.path.exists("user_overview.txt"):
        with open("task_overview.txt", "r") as task_overview_file:
            print("Task Overview:")
            print(task_overview_file.read())
        
        with open("user_overview.txt", "r") as user_overview_file:
            print("User Overview:")
            print(user_overview_file.read())
    else:
        print("Overview files are absent. Generate reports first.")

#Function to let you edit a task to say its overdue when view_my_tasks
def task_has_ovderdue(task):
    if task.due_date != "None" and not task.completed:
        due_date = datetime.datetime.strptime(task.due_date, "%Y-%m-%d").date()
        today = datetime.date.today()
        return due_date < today
    return False

#Function to write a task to the task.txt file and stores it under your user login
def write_tasks(tasks):
    with open("tasks.txt", "w") as tasks_file:
        for task in tasks:
            tasks_file.write(",".join(task) + "\n")

# Main menu function
def main_menu():
    load_users()
    
    while True:
        print(("==== Login ===="))
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            username = input("Enter your username:")
            password = input("Enter your password:")
            if username in users and users[username] == password:
                print("login successful.")
                logged_in_menu(username)
            else:
                print("Invalid username or password. Please try again.")
        
        elif choice == "2":
            register_user()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Try again.")

def logged_in_menu(username):
    while True:
        print(f"==== Welcome, {username}")
        print(" ==== Task Manager ====")
        print("r - Register User")
        print("a - Add Task")
        print("va - View All Tasks")
        print("vm - View My Tasks")
        print("gr - Generate Reports")
        print("ds - Display Statistics")
        print("e - Exit")
        choice = input("Enter your choice: ")
        if choice == "r":
            register_user()
        elif choice == "a":
            add_task()
        elif choice == "va":
            view_all_tasks()
        elif choice == "vm":
            view_my_tasks(username, tasks)
        elif choice == "gr":
            generate_reports(users, tasks)
        elif choice == "ds":
            display_statistics()
        elif choice == "e":
            break
        else:
            print("Invalid choice. Please try again.")

# Main entry point of the program
if __name__ == "__main__":
    main_menu()