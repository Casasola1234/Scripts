import subprocess
import getpass
import datetime
import sys
import re

outputFile = "SH_Template.txt"
#Making compatible the Script with Py2 and Py3

def write_output(content):
    with open(outputFile,'a') as f:
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



#Getting uptime of all services in all nodes.
# Define the services and their ports.
services = {
    "BRIDGE": 11111,
    "MAGNETO": 20000,
    "BRIDGE PROXY": 11116,
    "Storage Proxy": 20001,
    "SMB2Proxy": 20007,
    "Stats": 25566,
    "YODA": 25999,
    "Apollo": 24680,
    "GANDALF": 22222,
    "NewScribe": 12222,
    "Groot": 26999,
    "Alerts": 21111,
    "KeyChain": 22000,
}

def get_host_ips():
    try:
        output = subprocess.check_output("hostips", shell=True).decode().strip()
        return output.split()
    except Exception as e:
        print("Error getting host IPs:", e)
        return []

def extract_uptime(html):
    # Look for multiple uptime formats
    patterns = [
        r'Constituent\.? Uptime\s*[:\-]?\s*(.*)',
        r'Node\.? Uptime\s*[:\-]?\s*(.*)',
        r'Uptime\s*[:\-]?\s*(.*)'
    ]
    for pattern in patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return "N/A"

def query_service_uptime(host, port):
    url = f"http://{host}:{port}"
    try:
        output = subprocess.check_output(
            ["elinks", "-dump-width", "200", url],
            stderr=subprocess.DEVNULL
        ).decode()

        # DEBUG: Uncomment to inspect raw output for any specific host
        # if host == "172.27.136.32" and port == 11111:
        #     print(f"\n--- elinks output for {url} ---\n{output}\n---\n")

        uptime = extract_uptime(output)
        return uptime
    except Exception:
        return "ERROR"

def ServicesUptime():
    host_ips = get_host_ips()
    results = []

    for service_name, port in services.items():
        results.append(f"\n+++ {service_name} +++\n")
        for host in host_ips:
            uptime = query_service_uptime(host, port)
            results.append(f"{host} - {uptime}")

    return "\n".join(results)

def fetchFatals():
    cmd = 'allssh.sh "ls -ltra /home/cohesity/logs/ | grep \'.*\\.FATAL\' | tail -3"'
    run_command(cmd)


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
write_output("\n")
write_output("----\n")
write_output("h3.*Services Uptime*\n")
write_output("{code:java}\n")
write_output(ServicesUptime())
write_output("{code}\n")
write_output("----\n")
write_output("h3.*FATALS*\n")
write_output()
write_output("\n")
write_output("----\n")
write_output("h3.*CatFatals*\n")

write_output(ServicesUptime())

#Still lacks info, next 2 sprints will start testing.







