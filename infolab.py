import paramiko
from concurrent.futures import ThreadPoolExecutor
from scp import SCPClient

user = "ael"
password = "98853442"

# Populate machines with the valid IP addr
machines = []
for i in range (102, 104): #TODO Set range here 102, 126
    # Aceste calculatoare nu merg
    if i == 113 or i == 122:
        continue
    ip_add = '10.10.10.' + str(i)
    machines.append(ip_add)

# Function to run a bash command on a remote machine
def execute_on_remote(host, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(host, username=user, password=password)
        stdin, stdout, stderr = client.exec_command(command)
        
        # Handle sudo password prompt
        if 'sudo' in command:
            stdin.write(password + '\n')
            stdin.flush()

        # Print the output and errors
        print(f"Output from {host}:")
        print(stdout.read().decode())
        print(stderr.read().decode())
    
    finally:
        client.close()

def change_background():
    background_image_path = "/usr/share/backgrounds/Clouds_by_Tibor_Mokanszki.jpg"
    # Gnome
    command = f"gsettings set org.gnome.desktop.background picture-uri 'file://{background_image_path}'"
    # MATE
    # command = f"gsettings set org.mate.background picture-filename {background_image_path}"
    with ThreadPoolExecutor() as executor:
        executor.map(lambda machine: execute_on_remote(machine, command), machines)
    return

# Function to copy the script to the remote machine and make it run at intervals
def change_background_regularly():
    #TODO 
    command = "touch hello-testing"
    for machine in machines:
        execute_on_remote(machine, command)

def update_machines():
    command = f"echo '{password}' | sudo -S apt-get update && sudo -S apt-get upgrade -y"
    
    # Without threads
    # for machine in machines:
    #     print(f"Updating {machine}...")
    #     execute_on_remote(machine, command)
    # print("Updates complete on all machines.")
    
    print("Starting updates on all machines...")
    
    # With threads
    with ThreadPoolExecutor() as executor:
        executor.map(lambda machine: execute_on_remote(machine, command), machines)
    print("Updates initiated on all machines.")

def create_file():
    command = "touch hello-testing"
    for machine in machines:
        execute_on_remote(machine, command)

def install_program():
    print("What program do you want to install?")
    program_name = input()
    command = f"echo '{password}' | sudo -S apt install '{program_name}' -y"
    print("Installation initiated on all machines.")
    with ThreadPoolExecutor() as executor:
        executor.map(lambda machine: execute_on_remote(machine, command), machines)


def remove_program():
    print("What program do you want to remove?")
    program_name = input()
    command = f"echo '{password}' | sudo -S apt remove '{program_name}' -y"
    with ThreadPoolExecutor() as executor:
        executor.map(lambda machine: execute_on_remote(machine, command), machines)

def display_menu():
    print("\n--- Management Menu ---")
    print("0. Exit")
    print("1. Change background on all machines")
    print("2. Update all machines")
    print("3. Install a program")
    print("4. Remove a program")
    print("99. Testing (create a file)")
    
    choice = int(input("Enter your choice: "))
    return choice

# Main program loop
while True:
    choice = display_menu()
    
    match choice:
        case 0:
            print("Exiting...")
            break
        case 1:
            change_background()
        case 2:
            update_machines()
        case 3:
            install_program()
        case 4:
            remove_program()
        case 99:
            create_file()
        case _:
            print("Invalid choice. Please try again.")