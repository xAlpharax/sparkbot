##############################################################################

import subprocess

def get_vitals():
    uptime = subprocess.getoutput("uptime | cut -c 2-")
    used_memory = subprocess.getoutput("free -h | awk '/Mem:/ { print $3 }'")
    total_memory = subprocess.getoutput("free -h | awk '/Mem:/ { print $2 }'")

    return f"`{uptime}\t\t{used_memory}/{total_memory}`"

##############################################################################
