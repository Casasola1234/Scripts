Warning: this code is provided on a best effort basis and is not in any way officially supported or sanctioned by Cohesity. The code is intentionally kept simple to retain value as example code. The code in this repository is provided as-is and the author accepts no liability for damages resulting from its use.

The Script Creates an output file called heliosOut.txt with the data needed on a SH for Helios Report issues, this code is not design to change Cluster configuration, is only to get relevant data to improve the SH creation structure.

Download and run the Sript using the below command:

curl -O https://raw.githubusercontent.com/Casasola1234/Scripts/refs/heads/main/Helios/heliosReport.py && chmod +x heliosReport.py

python3 heliosReport.py 

output file will be located as heliosOut.txt in /tmp.
