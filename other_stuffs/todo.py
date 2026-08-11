# to do list 
number=int(input("Enter the number of list do you have :"));
to_do_list=dict()
completed=list()
print("please enter priority wise\n")
for i in range(1,number+1):
    to_do_list[i]=input("Enter the number of list do you have :")
while(to_do_list!={}):
    try:
        priority=int(input("1:check left tasks list 2:check completed tasks 3:task completed"))
        if priority==1:
            print("tasks left :",to_do_list)
        elif priority==2:
            print("completed tasks :",completed)    
        elif priority==3:
            task_no=int(input("Enter the task number:"))
            try:
                completed.append(to_do_list[task_no])
                del to_do_list[task_no]
            except Exception:
                print(f"task number {task_no} is already completed ")
        else:
            print("Number not included in the menu") 
    except Exception:
        print("Invalid input, please enter a number")
print("well done now no task left")                       

