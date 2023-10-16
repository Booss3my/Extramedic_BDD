import subprocess
from tqdm import tqdm
import time
from src.config import * 
import os
import sys

Rpath = os.path.dirname(__file__)
sys.path.append(Rpath)
sys.path.append(os.path.join(Rpath,"src"))


scripts_to_run = [
    {"script": os.path.join(Rpath,"src/new_profiles.py"), "args":arguments_list},
    {"script": os.path.join(Rpath,"src/removed_profiles.py"), "args":arguments_list},
    {"script": os.path.join(Rpath,"src/changed_activity.py"), "args":arguments_list},
    {"script": os.path.join(Rpath,"src/changed_location.py"), "args":arguments_list},

]

total_scripts = len(scripts_to_run)


def run_script(script, args):
    command = ["python", script] + args
    subprocess.run(command)

# Create a tqdm progress bar
with tqdm(total=total_scripts, unit="script", desc="Lancement des tâches") as pbar:
    for script_info in scripts_to_run:
        script = script_info["script"]
        args = script_info["args"]
        run_script(script, args)
        pbar.update(1)

print("All scripts have been executed.")