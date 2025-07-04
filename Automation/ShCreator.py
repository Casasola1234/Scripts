import subprocess
import getpass
import datetime
import sys
import re

outputFile = "SH_Template.txt"

def write_output(content):
    with open(outputFile, 'a') as f:
        f.write(content + "\n")

try:
    input_func = raw_input  # Python 2
except NameError:
    input_func = input      # Python 3

username = input_func("Iris_CLI Username: ")
password = getpass.getpass("Iris_CLI Password: ")
IssueSummary = input_func("Problem Description and Customer Impact: ")

def run_command(command):
    try:
        if isinstance(command, list):
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        stdout, stderr = process.communicate()
        stdout = stdout.decode("utf-8").strip() if stdout else ""
        stderr = stderr.decode("utf-8").strip() if stderr else ""
        return stdout if stdout else "ERROR: " + stderr
    except Exception as e:
        return "ERROR: {}".format(str(e))

def clusterInfo():
    cmd = [
        "iris_cli",
        "-username=" + username,
        "-password=" + password,
        "--skip_password_prompt=true",
        "cluster",
        "info"
    ]
    return run_command(cmd)

def gflagList():
    cmd = [
        "iris_cli",
        "-username=" + username,
        "-password=" + password,
        "--skip_password_prompt=true",
        "cluster",
        "ls-gflags",
        "verbose=true"
    ]
    return run_command(cmd)

def fetchFatals():
    cmd = 'allssh.sh "ls -ltra /home/cohesity/logs/ | grep \'.*\\.FATAL\' | tail -3"'
    return run_command(cmd)

def get_host_ips():
    try:
        output = subprocess.check_output("hostips", shell=True).decode().strip()
        return output.split()
    except Exception as e:
        print("Error getting host IPs:", e)
        return []

def extract_uptime(html):
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
        uptime = extract_uptime(output)
        return uptime
    except Exception:
        return "ERROR"

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

def ServicesUptime():
    host_ips = get_host_ips()
    results = []
    for service_name, port in services.items():
        results.append(f"\n+++ {service_name} +++\n")
        for host in host_ips:
            uptime = query_service_uptime(host, port)
            results.append(f"{host} - {uptime}")
    return "\n".join(results)

upgradeHistory = run_command("cat /home/cohesity/data/nexus/software_version_history.json")

# Begin output generation

write_output("----")
write_output("h2.*Problem Description and Customer Impact:*")
write_output(IssueSummary)
write_output("----")
write_output("h2.*Analysis/Troubleshooting Performed:*")
write_output("")
write_output("----")
write_output("h2.*Screenshots/File Section:*")
write_output("")
write_output("----")
write_output("h2.*Logs related to the issue:*")
write_output("{code:java}")
write_output("{code}")
write_output("----")
write_output("h2.*Support Channel Information:*")
write_output("{code:java}")
write_output("{code}")
write_output("----")
write_output("h2.*Environmental Details:*")
write_output("h2.*Cluster Information:*")
write_output("{code:java}")
write_output(clusterInfo())
write_output("{code}")
write_output("----")
write_output("h3.*Update/Upgrade History:*")
write_output("{code:java}")
write_output(upgradeHistory)
write_output("{code}")
write_output("----")
write_output("h3.*Services Uptime*")
write_output("{code:java}")
write_output(ServicesUptime())
write_output("{code}")
write_output("----")
write_output("h3.*FATALS*")
write_output("{code:java}")
write_output(fetchFatals())
write_output("{code}")
write_output("----")
write_output("h3.*Gflag List*")
write_output("{code:java}")
write_output(gflagList())
write_output("{code}")
write_output("----")
write_output("h2.*Ask to CDP:*")











