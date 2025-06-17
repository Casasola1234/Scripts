import subprocess
import getpass
import sys

outputFile = "SH_Template.txt"
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
IssueSummary = input_func("Problem Description and Customer Impact: ")


GetClusterInfo = [
    "iris_cli",
    "-username=" + username,
    "-password=" + password,
    "--skip_password_prompt=true",
    "cluster",
    "info",
    "show-stats=true"
]

def run_command(command):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        stdout = stdout.decode("utf-8").strip() if stdout else ""
        stderr = stderr.decode("utf-8").strip() if stderr else ""
        return stdout if stdout else "ERROR: " + stderr
    except Exception as e:
        return "ERROR: {}".format(str(e))


def clusterInfo():
    run_command(f"iris_cli -username="+username,"-password= " + password, "--skip_password_prompt=true cluster info")

def gflagList():
    run_command(f"iris_cli -username="+username,"-password=" + password," cluster ls-gflags verbose=true")

def ServicesUptime():

    run_command("echo -e "\n\033[7m +++ BRIDGE +++ \033[0m\n" ; echo "" > /tmp/services.txt ; for host in $(hostips) ; do echo -e "${host} \t-\t $(elinks -dump-width 200 http:$host:11111 | head | grep Constituent.Uptime | sed 's/^[ \t]//; s/Constituent Uptime//')" ; done >> /tmp/services.txt && cat /tmp/services.txt | sort -k 4,4 -k 3,3n -r;echo -e "\n\033[7m +++ MAGNETO +++ \033[0m\n" ; echo "" > /tmp/services.txt ; for host in $(hostips) ; do echo -e "${host} \t-\t $(elinks -dump-width 200 http:$host:20000 | head | grep Constituent.Uptime | sed 's/^[ \t]//; s/Constituent Uptime//')" ; done >> /tmp/services.txt && cat /tmp/services.txt | sort -k 4,4 -k 3,3n -r;echo -e "\n\033[7m +++ BRIDGE PROXY +++ \033[0m\n" ; echo "" > /tmp/services.txt ; for host in $(hostips) ; do echo -e "${host} \t-\t $(elinks -dump-width 200 http:$host:11116 | head | grep Constituent.Uptime | sed 's/^[ \t]//; s/Constituent Uptime//')" ; done >> /tmp/services.txt && cat /tmp/services.txt | sort -k 4,4 -k 3,3n -r;echo -e "\n\033[7m +++  Storage Proxy +++ \033[0m\n" ; echo "" > /tmp/services.txt ; for host in $(hostips) ; do echo -e "${host} \t-\t $(elinks -dump-width 200 http:$host:20001 | head | grep Uptime | sed 's/^[ \t]//; s/Uptime//')" ; done >> /tmp/services.txt && cat /tmp/services.txt | sort -k 4,4 -k 3,3n -r;echo -e "\n\033[7m +++ SMB2Proxy +++ \033[0m\n" ; echo "" > /tmp/services.txt ; for host in $(hostips) ; do echo -e "${host} \t-\t $(elinks -dump-width 200 http:$host:20007 | head | grep Uptime | sed 's/^[ \t]//; s/Uptime//')" ; done >> /tmp/services.txt && cat /tmp/services.txt | sort -k 4,4 -k 3,3n -r;echo -e "\n\033[7m +++ Stats +++ \033[0m\n" ; echo "" > /tmp/services.txt ; for host in $(hostips) ; do echo -e "${host} \t-\t $(elinks -dump-width 200 http:$host:25566 | head | grep Constituent.Uptime | sed 's/^[ \t]//; s/Constituent Uptime//')" ; done >> /tmp/services.txt && cat /tmp/services.txt | sort -k 4,4 -k 3,3n -r;echo -e "\n\033[7m +++ YODA +++ \033[0m\n" ; echo "" > /tmp/services.txt ; for host in $(hostips) ; do echo -e "${host} \t-\t $(elinks -dump-width 200 http:$host:25999 | head | grep Constituent.Uptime | sed 's/^[ \t]//; s/Constituent Uptime//')" ; done >> /tmp/services.txt && cat /tmp/services.txt | sort -k 4,4 -k 3,3n -r;echo -e "\n\033[7m +++ Apollo +++ \033[0m\n" ; echo "" > /tmp/services.txt ; for host in $(hostips) ; do echo -e "${host} \t-\t $(elinks -dump-width 200 http:$host:24680 | head | grep Constituent.Uptime | sed 's/^[ \t]//; s/Constituent Uptime//')" ; done >> /tmp/services.txt && cat /tmp/services.txt | sort -k 4,4 -k 3,3n -r;echo -e "\n\033[7m +++ GANDALF +++ \033[0m\n" ; echo "" > /tmp/services.txt ; for host in $(hostips) ; do echo -e "${host} \t-\t $(elinks -dump-width 200 http:$host:22222 | head | grep Constituent.Uptime | sed 's/^[ \t]//; s/Constituent Uptime//')" ; done >> /tmp/services.txt && cat /tmp/services.txt | sort -k 4,4 -k 3,3n -r;echo -e "\n\033[7m +++ NewScribe +++ \033[0m\n" ; echo "" > /tmp/services.txt ; for host in $(hostips) ; do echo -e "${host} \t-\t $(elinks -dump-width 200 http:$host:12222 | head | grep Node.Uptime | sed 's/^[ \t]//; s/Node Uptime//')" ; done >> /tmp/services.txt && cat /tmp/services.txt | sort -k 4,4 -k 3,3n -r;echo -e "\n\033[7m +++ Groot +++ \033[0m\n" ; echo "" > /tmp/services.txt ; for host in $(hostips) ; do echo -e "${host} \t-\t $(elinks -dump-width 200 http:$host:26999 | head | grep Constituent.Uptime | sed 's/^[ \t]//; s/Constituent Uptime//')" ; done >> /tmp/services.txt && cat /tmp/services.txt | sort -k 4,4 -k 3,3n -r;echo -e "\n\033[7m +++ Alerts +++ \033[0m\n" ; echo "" > /tmp/services.txt ; for host in $(hostips) ; do echo -e "${host} \t-\t $(elinks -dump-width 200 http:$host:21111 | head | grep Constituent.Uptime | sed 's/^[ \t]//; s/Constituent Uptime//')" ; done >> /tmp/services.txt && cat /tmp/services.txt | sort -k 4,4 -k 3,3n -r;echo -e "\n\033[7m +++ KeyChain +++ \033[0m\n" ; echo "" > /tmp/services.txt ; for host in $(hostips) ; do echo -e "${host} \t-\t $(elinks -dump-width 200 http:$host:22000 | head | grep Constituent.Uptime | sed 's/^[ \t]*//; s/Constituent Uptime//')" ; done >> /tmp/services.txt && cat /tmp/services.txt | sort -k 4,4 -k 3,3n -r;echo -e "\n\033[7m +++ Yoda Agent +++ \033[0m\n";allssh.sh "links http:198.18.0.102:26662 | grep -i uptime"")


upgradeHistory = run_command("cat /home/cohesity/data/nexus/software_version_history.json")


#Create output with SH template

write_output("----\n")
write_output("h2.*Problem Description and Customer Impact:*\n")
write_output(IssueSummary)
write_output("\n----")
write_output("h2.*Analysis/Troubleshooting Performed:*\n")
write_output("\n")
write_output("----\n")
write_output("h2.*Screenshots/File Section:*\n")
write_output("\n")
write_output("----\n")
write_output("h2.*Logs related to the issue:*\n")
write_output("{code:java}\n")
write_output("{code}/n")
write_output("\n")
write_output("----\n")
write_output("h2.*Support Channel Information:*\n")
write_output("{code:java}\n")
write_output("{code}/n")
write_output("\n")
write_output("----\n")
write_output("h2.*Environmental Details:*\n")
write_output("h2.*Cluster Information:*\n")
write_output("{code:java}\n")
write_output(clusterInfo())
write_output("{code}\n")
write_output("\n")
write_output("----\n")
write_output("h3.*Update/Upgrade History:*\n")
write_output("{code:java}\n")
write_output(upgradeHistory)
write_output("{code}/n")
#Still lacks info, next 2 sprints will start testing.







