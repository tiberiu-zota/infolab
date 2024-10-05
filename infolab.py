import paramiko
from concurrent.futures import ThreadPoolExecutor

user = "cisco"
password = "password"
machines = ["192.168.0.174", "192.168.0.106"]

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
    background_image_path1 = "/opt/netacad-vm-background.jpg"
    background_image_path2 = "/opt/netacad-vm-background-datacenter-bg.jpg"
    # For Gnome
    bash_command = f"gsettings set org.gnome.desktop.background picture-uri 'file://{background_image_path2}'"
    # For MATE
    bash_command = f"gsettings set org.mate.background picture-filename {background_image_path1}"
    
    with ThreadPoolExecutor() as executor:
        executor.map(lambda machine: execute_on_remote(machine, bash_command), machines)

    return

def update_machines():
    update_command = f"echo '{password}' | sudo -S apt-get update && sudo -S apt-get upgrade -y"
    
    # Without threads
    # for machine in machines:
    #     print(f"Updating {machine}...")
    #     execute_on_remote(machine, update_command)
    # print("Updates complete on all machines.")
    
    print("Starting updates on all machines...")

    # With threads
    with ThreadPoolExecutor() as executor:
        executor.map(lambda machine: execute_on_remote(machine, update_command), machines)

    print("Updates initiated on all machines.")

def create_file():
    bash_command = "touch hello-testing"
    
    for machine in machines:
        execute_on_remote(machine, bash_command)

def display_menu():
    print("\n--- Management Menu ---")
    print("0. Exit")
    print("1. Change background on all machines")
    print("2. Update all machines")
    print("3. Create a file")
    
    choice = input("Enter your choice: ")
    return choice

# Main program loop
while True:
    choice = display_menu()
    
    if choice == "0":
        print("Exiting...")
        break
    elif choice == "1":
        change_background()
    elif choice == "2":
        update_machines()
    elif choice == "3":
        create_file()
    else:
        print("Invalid choice. Please try again.")