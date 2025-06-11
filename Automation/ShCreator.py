import subprocess
import getpass
import sys

outputFile = "cluster_info.txt"
#Making compatible the Script with Py2 and Py3

def write_output(content):
    with (outputFile,'a') as f:
        f.write(content + "\n")



try:
    input_func = raw_input  # Python 2
except NameError:
    input_func = input      # Python 3

username = input_func("Iris_CLI Username: ")
password = getpass.getpass("Iris_CLI Password: ")

GetClusterInfo = [
    "iris_cli",
    "-username=" + username,
    "-password=" + password,
    "--skip_password_prompt=true",
    "cluster",
    "info",
    "show-stats=true"
]

try:
    process = subprocess.Popen(
        GetClusterInfo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    with open(outputFile, 'w') as f:
        f.write(stdout.decode("utf-8") if sys.version_info[0]>=3 else stdout)

    if stderr:
        print("Error running command: ")
        print(stderr.decode("utf-8") if sys.version_info[0] >= 3 else stderr)
except Exception as e:
    print("An error occured running the Script:")
    print(str(e))
    