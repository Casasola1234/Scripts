import os
import subprocess
import re
import time
from datetime import datetime

OUTPUT_FILE = "/tmp/heliosOut.txt"
CONFIG_FILE = "/tmp/cluster_config"
GANDALF_OUTPUT = "/tmp/gandalf_output.txt"

def write_output(content):
    with open(OUTPUT_FILE, "a") as f:
        f.write(content + "\n")

def run_command(command):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        stdout = stdout.decode("utf-8").strip() if stdout else ""
        stderr = stderr.decode("utf-8").strip() if stderr else ""
        return stdout if stdout else "ERROR: " + stderr
    except Exception as e:
        return "ERROR: {}".format(str(e))

def fetch_cluster_config():
    run_command("cluster_config.sh fetch > /dev/null 2>&1")
    return os.path.exists(CONFIG_FILE)

def extract_config_section(start_pattern, end_pattern):
    if not os.path.exists(CONFIG_FILE):
        return ""
    with open(CONFIG_FILE, "r") as f:
        content = f.read()
    match = re.search('{}.*?{}'.format(start_pattern, end_pattern), content, re.DOTALL)
    return match.group(0) if match else ""

def extract_line(pattern):
    if not os.path.exists(CONFIG_FILE):
        return ""
    with open(CONFIG_FILE, "r") as f:
        for line in f:
            if re.search(pattern, line):
                return line.strip()
    return ""

def fetch_gandalf_data():
    return run_command("gt.sh fetch helios_agent_data cohesity.nexus.helios.conn.HeliosAgentConnInfoProto")

def convert_timestamps(log_data):
    timestamps = re.findall(r'\d{16}', log_data)
    converted = []
    for ts in timestamps:
        secs = int(ts[:10])
        human_date = datetime.utcfromtimestamp(secs).strftime('%Y-%m-%d %H:%M:%S UTC')
        converted.append("{} => time in secs: {} => {}".format(ts, secs, human_date))
    return "\n".join(converted)

# Start writing output
with open(OUTPUT_FILE, "w") as f:
    f.write("============================================\n")
    f.write(" Helios Cluster Investigation Report \n")
    f.write("============================================\n")
    f.write("Generated on: {}\n\n".format(datetime.now()))

write_output("Checking Cluster Configuration...")
if fetch_cluster_config():
    write_output("Cluster config fetched successfully.")
else:
    write_output("ERROR: Failed to fetch cluster config!")
    exit(1)

write_output("\n--------------------------------------------")
write_output("Checking MCM Configuration")
write_output("--------------------------------------------")
write_output(extract_config_section("mcm_config {", "}"))

write_output("\n--------------------------------------------")
write_output("Checking Eagle Agent Configuration")
write_output("--------------------------------------------")
write_output(extract_config_section("eagle_config {", "}"))

write_output("\n--------------------------------------------")
write_output("Checking Cluster Incarnation ID")
write_output("--------------------------------------------")
write_output(extract_line("cluster_incarnation_id:"))

write_output("\n--------------------------------------------")
write_output("Checking Eagle Agent State Collection")
write_output("--------------------------------------------")
gandalf_data = fetch_gandalf_data()
write_output(gandalf_data)

converted_timestamps = convert_timestamps(gandalf_data)
if converted_timestamps:
    write_output("\nConverted Timestamps:")
    write_output(converted_timestamps)

write_output("\n============================================")
write_output("Investigation Completed")
write_output("============================================")
print("____________________________________")
print("Output saved in /tmp/heliosOut.txt")
print("Run the below command to see the output:")
print("less /tmp/heliosOut.txt")
print("____________________________________")