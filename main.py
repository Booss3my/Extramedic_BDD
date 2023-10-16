import subprocess
from tqdm import tqdm
from src.config import * 
import os

#create output folder if it doesnt exist
if not os.path.exists(args.output_rpath):
    os.mkdir(args.output_rpath)

#scripts to run and their arguments
scripts_to_run = [
    {"script": os.path.join(Rpath,"src/new_profiles.py"), "args":arguments_list},
    {"script": os.path.join(Rpath,"src/removed_profils.py"), "args":arguments_list},
    {"script": os.path.join(Rpath,"src/changed_activity.py"), "args":arguments_list},
    {"script": os.path.join(Rpath,"src/changed_location.py"), "args":arguments_list},
    {"script": os.path.join(Rpath,"src/statistics.py"), "args":arguments_list}

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