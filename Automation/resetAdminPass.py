import subprocess
import re
import shutil
import os
import time

# Script created by Joseph Arias Aguero - TSE Level 3

# Define file paths
iris_users_file = "/tmp/iris_users"
backup_file = "/tmp/iris_users.bak"
output_file = "/tmp/output"
password_hash = "$2a$10$WLfGP/r6XqzMKxOPYuIkm.KnoilahWbwenY/SYCLmcmzFEl3NGR/K"

def run_command(command, timeout=120, interactive=False):
    """Executes a shell command with a timeout and handles interactive input."""
    try:
        with open(output_file, "w") as out_file:
            process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=out_file, stderr=out_file, universal_newlines=True)
            if interactive:
                stdout, stderr = process.communicate(input="y\n")  # Ensure 'y' is sent for confirmation
            else:
                start_time = time.time()
                while process.poll() is None:
                    if time.time() - start_time > timeout:
                        process.kill()
                        print("Error: Command timed out after {} seconds. Check {} for details.".format(timeout, output_file))
                        return None
                    time.sleep(1)
        if process.returncode != 0:
            print("Error executing command. Check {} for details.".format(output_file))
            return None
        return True
    except Exception as e:
        print("Exception running command {}: {}".format(command, e))
        return None

# Step 2: Dump the iris_users Proto to a file
print("Fetching iris_users proto...")
run_command("gt.sh fetch iris_users cohesity.iris.UsersProto > {}".format(iris_users_file))

# Verify that the file was created before proceeding
if not os.path.exists(iris_users_file):
    print("Error: {} was not created. Exiting...".format(iris_users_file))
    os._exit(1)

# Step 3: Backup the file
print("Creating backup...")
shutil.copy(iris_users_file, backup_file)

# Step 4-7: Edit the iris_users file
print("Editing iris_users file...")
try:
    with open(iris_users_file, "r") as file:
        lines = file.readlines()
    
    # Step 7: Remove first three lines
    lines = lines[3:]
    
    # Extract the correct version number from the last two lines
    version_number = None
    for line in reversed(lines):
        match = re.search(r'version:\s*(\d+)', line)
        if match:
            version_number = match.group(1)
            break
    
    # Remove the last two lines which contain metadata
    lines = lines[:-2]  # Remove the last two lines
    
    # Step 5-6: Modify admin entry
    updated_lines = []
    update_password = False
    modify_force_password = False
    for line in lines:
        if 'username: "admin"' in line:
            update_password = True
            modify_force_password = True
        if 'password:' in line and update_password:
            updated_lines.append('password: "{}"\n'.format(password_hash))
            update_password = False
        elif 'force_password_change:' in line and modify_force_password:
            updated_lines.append('force_password_change: true\n')
            modify_force_password = False
        else:
            updated_lines.append(line)
    
    # Write the updated content back to the file
    with open(iris_users_file, "w") as file:
        file.writelines(updated_lines)
    
    print("File modifications complete.")
    
except Exception as e:
    print("Error modifying file: {}".format(e))

# Step 9: Ask before updating Gandalf iris_users Key
if version_number:
    update_command = "gt.sh update iris_users {} cohesity.iris.UsersProto --input_file {}".format(version_number, iris_users_file)
    print("The following command will be executed:")
    print(update_command)
    try:
        # Ensure compatibility between Python 2 and 3
        user_input = raw_input("Do you want to update the Gandalf iris_users key? (yes/no): ") if hasattr(__builtins__, 'raw_input') else input("Do you want to update the Gandalf iris_users key? (yes/no): ")
    except NameError:
        user_input = input("Do you want to update the Gandalf iris_users key? (yes/no): ")
    user_input = user_input.strip().lower()
    if user_input == "yes":
        print("Executing update...")
        if run_command(update_command, timeout=120, interactive=True):
            print("Update complete.")
        else:
            print("Update failed or timed out. Check {} for details.".format(output_file))
            os._exit(1)
    else:
        print("Update skipped.")
else:
    print("Version number not found. Manual update required.")