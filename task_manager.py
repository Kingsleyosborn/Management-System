# def write_user():
from datetime import datetime, timedelta
import calendar
def read_user():                                                         #for checking the user name and their password
    read_user = open("user.txt", "r+", encoding="utf-8")
    user_name = []                                                      # creat two empty list for name and password, all the name and password
    user_password = []                                                          # will be stored separated
    for data in read_user:
        data_list = data.split(", ")
        user_name.append(data_list[0].strip())
        user_password.append(data_list[1].strip())
    read_user.close()
    return user_name, user_password

def admin_menu():                                                       #There are two menu interface for user: one for admin; one for the other
    menu = input('Select one of the following Options below:\n'
                 'r - Registering a user\n'
                 'a - Adding a task\n'
                 'va - View all tasks\n'
                 'vm - View my task\n'
                 "gr - generate reports\n"
                 "de - display statistics\n"
                 'e - Exit: ').lower()
    return menu

def other_menu():
    menu = input('Select one of the following Options below:\n'
                 'a - Adding a task\n'
                 'va - View all tasks\n'
                 'vm - View my task\n'
                 'e - Exit: ').lower()
    return menu


def login_user(user, password):                                                          #to login in
    user_name, user_password = read_user()
    for time in range(len(user_name)):
        if user == user_name[time] and password == user_password[time]:
            return True

def reg_user():                                                                         #register user, if the new name is used already, the user needs to choose another one
    user_name, user_password = read_user()
    while True:
        new_username = input("Please enter a new username: ")
        new_password = input("Please enter a new password: ")
        confirm_password = input("Please enter a new password again for confirmation: ")
        for name in user_name:
            if name == new_username:
                print("The user name has been registered, please choose another one.")
                break

        if new_password == confirm_password and new_username != name:                    # if both passwords are matched, it will be written into the file
            with open("user.txt", "a") as user_doc:
                user_doc.write("\n" + new_username + ", " + new_password)
            print(f"{new_username} is now registered.")
            return

        elif new_password != confirm_password and new_username != name:                             # if they are not matched, error message will pop
            print(f"The password is not match, please reenter the info again.")
            continue

def add_task():
    new_user = input("Please enter the person whom the task is assigned to: ")                               # taking info from the user
    title_task = input("Please enter the title of the task: ")
    des_task = input("Please enter the description of the task: ")
    assign_date = input("Please enter today's date(dd mmm yyyy)eg 23 Nov 2025: ")                              #we assume the user input the date format correctly
    due_date = input("Please the due date of the take(dd mmm yyyy)eg 23 Nov 2025: ")
    completion = 'No'
    with open("tasks.txt", "a+") as task_doc:  # write the info into the file and using + ", " + to separate each input
        task_doc.write("\n" + new_user + ", " + title_task + ", " + des_task + ", "
                       + assign_date + ", " + due_date + ", " + completion)
    return


def count_task():                                                                           #to count how many tasks in total
    count_task = 0  # simple just count how many lines in each file
    with open("tasks.txt", "r+") as task_doc:
        lines = task_doc.readlines()
        for line in lines:
            count_task += 1
    return count_task

def view_all():                                                                             #to view all the tasks in the company
    with open("tasks.txt", "r+") as task_doc:
        lines = task_doc.readlines()
        print(f"Here are all the task: \n")
        for line in lines:
            line = line.strip()
            items = line.split(", ")
            tasks = items[1]
            print(tasks)
    print("\n")
    return

def view_mine():                                                      #to view the login person's task
    count_task = 0
    list_task = []
    with open("tasks.txt", "r+") as task_doc:
        lines = task_doc.readlines()
        print(f"Here are all the tasks for {user}: \n")
        for line in lines:
            items = line.split(", ")
            name = items[0]
            tasks = items[1]
            if name == user:
                list_task.append(tasks)
                count_task += 1
        if count_task > 0:                                                      #after view mine, if the user has task, the user can modify
            print(f"You have {count_task} tasks.")
        elif count_task == 0:                                                   #if the user do not have any task, back to the menu
            print("You have no task.")
            return
        select_task(list_task)
    return

def select_task(list_task):                                               #after selecting vm, the user can choose which task to modify
    for count, task in enumerate(list_task, start= 1):
        print(f"{count}: {task}")
    while True:
        try:
            task_num = int(input("Please select which task to modify or enter -1 back to main menu: "))
        except:
            print("Wrong input, try again.")
            continue
        for count, task in enumerate(list_task, start=1):
            if count == task_num:
                print(f"You have choose \"{list_task[task_num-1]}\"")
                option = input("Would you like to choose:\n 1: Mark as complete\n 2: Edit the task\n")
                if option == "1":                                       #if user choose to mark as complete, we do not need to check  it is completed or not
                    edit_task(1, list_task[task_num - 1])
                elif option == "2":                                     #call the function check_complete() to see whether the task is completed
                    if check_complete(list_task[task_num-1]) == True:
                        print("You cannot edit the task, because it is completed.")
                        break
                    elif check_complete(list_task[task_num-1]) == False:  #if the task is not completed, call edit_task to edit the choosen task
                        edit_task(2, list_task[task_num-1])

            elif task_num == -1:                                     #return to menu if the user input -1
                break
        break

def check_complete(choose_task):                                     #the function to check the task is completed or not
    file = open("tasks.txt", "r", encoding="utf-8")
    content = file.readlines()
    file.close()
    for line in content:
        items = line.split(", ")
        for item in items:
            if item == choose_task and items[5] == "No\n":
                return False
            elif item == choose_task and items[5] == "Yes\n":
                return True


'''
before allow the user to edit the task
input the correct date format so that w
e can use the datatime.today() to get the correct time
if the duedate is > Today's date,
we can edit the task. which means the task has not completed
then send a value to edit_task() function'''

def check_duedate(task = "check_all"):                                       #the function to check whether a task is past its duedate
    if task == "check_all":                                                  # to check how many task past the duedate already
        file = open("tasks.txt", "r", encoding="utf-8")
        content = file.readlines()
        file.close()
        count_due_task = 0
        for line in content:
            items = line.strip().split(", ")
            due_time = items[4]
            d_time = datetime.strptime(due_time,"%d %b %Y")
            today = datetime.today()
            if today > d_time and items[5] == "No": # task is overdued
                count_due_task += 1
        return count_due_task

    else:                                                          #to check how many duedate tasks for the specific user
        file = open("tasks.txt", "r", encoding="utf-8")
        content = file.readlines()
        file.close()
        count_due_task = 0
        for line in content:
            items = line.strip().split(", ")
            user = items[0]
            due_time = items[4]
            d_time = datetime.strptime(due_time,"%d %b %Y")
            today = datetime.today()
            if user == task and today > d_time and items[5] == "No": # task is overdued
                count_due_task += 1
        return count_due_task



'''In edit_task function, we open the '''
def edit_task(choice, choose_task):                                #to edit the task
    file = open("tasks.txt", "r+", encoding="utf-8")
    content = file.readlines()
    file.close()

    if choice == 1:                                                         #mark as complete
        print(choose_task)
        for line in content:
            items = line.split(", ")
            for item in items:
                if item == choose_task:
                    line_index = content.index(", ".join(items))
                    items[5] = "Yes\n"
                    line = ", ".join(items)
                    content[line_index] = line

        print(f"The task is now completed.")

        f = open("tasks.txt", "w")
        for line in content:
            f.write(line)
        f.close()

    elif choice == 2:                                       #only the user can change their own task
        choice_edit_name_or_date = int(input("Please choose one of the following options:\n"
                       "1: To change the name of this task is assigned to\n"
                       "2: The due date of this task\n: "))
        if choice_edit_name_or_date == 1:
            for line in content:
                items = line.split(", ")
                for item in items:
                    if item == choose_task:
                        line_index = content.index(", ".join(items))
                        items[0] = input("Please enter the name: ")
                        line = ", ".join(items)
                        content[line_index] = line

            print(f"The name is now updated.\n")

            f = open("tasks.txt", "w")
            for line in content:
                f.write(line)
            f.close()

        if choice_edit_name_or_date == 2:
            for line in content:
                items = line.split(", ")
                for item in items:
                    if item == choose_task:
                        line_index = content.index(", ".join(items))
                        items[4] = input("Please enter the new due date for this task: ")
                        line = ", ".join(items)
                        content[line_index] = line

            print(f"The duedate is now updated")
            f = open("tasks.txt", "w")
            for line in content:
                f.write(line)
            f.close()

def count_not_done_task():                   #check how many task is not done
    count = 0
    f = open("tasks.txt", "r+", encoding="utf-8")
    content = f.readlines()
    f.close()
    for line in content:
        items = line.strip().split(", ")
        if items[5] == "No":
            count += 1

    return count

def count_done_task():                  #check how many task is done
    count = 0
    f = open("tasks.txt", "r", encoding="utf-8")
    content = f.readlines()
    f.close()
    for line in content:
        items = line.strip().split(", ")
        if items[5] == "Yes":
            count += 1
    return count

def count_user():                  #count how many user
    count = 0
    f = open("user.txt", "r+", encoding="utf-8")
    content = f.readlines()
    f.close()
    for line in content:
        count += 1
    return count

def count_thing_in_name(name):                                        #for user_overview, for each user, it calls to this function and do all the check
    count_task = 0                                                    #then return the all the values for the user
    count_done = 0                                                    #then write (append) the file
    count_undone = 0                                                  #then another user name send to this function again then return new values
    f_2 = open("tasks.txt", "r", encoding='utf-8')
    task_content = f_2.readlines()
    f_2.close()
    for line in task_content:
        items = line.strip().split(", ")
        if name == items[0]:
            count_task += 1
            if name == items[0] and items[5] == "No":
                count_undone += 1
            elif name == items[0] and items[5] == "Yes":
                count_done += 1
    return count_task, count_done, count_undone, check_duedate(name)


def gen_report():                                                                                          #generate the report
    text_for_overview = f"The total number of tasks in total: {str(count_task())}\n" \
                        f"The total number of completed tasks: {str(count_done_task())}\n" \
                        f"The total number of uncompleted tasks: {str(count_not_done_task())}\n"\
                        f"The total number of tasks that haven’t been completed and that are overdue:{str(check_duedate())}\n"\
                        f"The percentage of tasks that are incomplete: {str(round((count_not_done_task()/count_task()), 2)*100)}%\n"\
                        f"The percentage of tasks that are overdue: {str(round((check_duedate()/count_task()),2)*100)}%."
    #print(text_for_overview)
    f = open("task_overview.txt", "w+")                                                                 #write the report of the task_overview
    f.write(text_for_overview)
    f.close()

                                                                                                  #write/generate report of the user_overview
    text_for_user_overview = f"The total number of users registered: {str(count_user())}\n" \
                             f"The total number of tasks in total: {str(count_task())}\n" \

    f_2 = open("user_overview.txt", "w+")
    f_2.write(text_for_user_overview)
    f_2.close()

    f_1 = open("user.txt", "r", encoding="utf-8")                                         #need to creat a user name list then got the values for each users
    user_file_content = f_1.readlines()
    f_1.close()
    user_name = []

    for line in user_file_content:
        items = line.strip().split(", ")
        name = items[0]
        user_name.append(name)
    # print(user_name)
    for name in user_name:                                                            #for each user , call the function count_thing_in_name
        count_task_user, count_done, count_undone, duedate_name = count_thing_in_name(name)
        # print(count_task_user, count_done, count_undone, duedate_name)
        text_for_each_user = f"The total number of tasks assigned to {name}: \n" \
                             f"The percentage of the total number of tasks that have been assigned to {name}: " \
                             f"{round(count_task_user/count_task(),2)*100}%\n" \
                             f"The percentage of the tasks assigned to {name} that have been completed: " \
                             f"{round(count_done/count_task(),2)*100}%\n" \
                             f"The percentage of the tasks assigned to {name} that must still be completed: " \
                             f"{round(count_undone/count_task(),2)*100}%\n" \
                             f"The percentage of the tasks assigned to {name} that have not yet been completed and are overdue: " \
                             f"{round(duedate_name/count_task(),2)*100}%\n"
        f_2 = open("user_overview.txt", "a+")
        f_2.write(text_for_each_user)
        f_2.close()

    print("task_overview and user_overview have been generated.")


def display_stat():                                              #if reports do not exist, it calls the function gen_report() to generate reports
    while True:                                                  #Also the statistic may not be most updated. you need to regenerate new reports if the reports exist
        try:
            f_1 = open("task_overview.txt", "r")
            task_content= f_1.readlines()
            f_1.close()
            for lines in task_content:
                print(lines)
            f_2 = open("user_overview.txt", "r")
            user_content = f_2.readlines()
            f_2.close()
            for lines in user_content:
                print(lines)
            break
        except:
            print("There are no report.\nNow we are generating the new reports.......")
            gen_report()





while True:                                                                         #The program starts here
    user = input("Please enter your login name: ")
    password = input("Please enter your password: ")
    login_user(user, password)
    if login_user(user, password) == True:
        print("You have logged in. Loading please wait...")
        print(f"Welcome {user}!")
        break
    else:
        print("Either your login name or password is not correct, please enter again.")

                                              #greeting
while True:
    if user == "admin":                                                 #the admin meau, r and s options are only in here
        menu_admin = admin_menu()
        menu = None
    else:
        menu = other_menu()
        menu_admin = None

    if menu_admin == 'r':
        reg_user()
    elif menu == 'a' or menu_admin == 'a':
        add_task()
        print("\n")
    elif menu == 'va' or menu_admin == 'va':                           #open the file and turn the lines into list and take position 1 which is the task out
        view_all()
    elif menu == 'vm' or menu_admin == 'vm':                        #if the user name is equal to the name in the task file, return the task info
        view_mine()
    elif menu_admin == 'gr':
        gen_report()
    elif menu_admin == 'de':
        display_stat()
    elif menu == 'e'or menu_admin == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice, Please Try again")

