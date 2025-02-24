# Randomly shuffles the packet order for each subject and renames files to include the shortlist number.
# Note: doesn't preserve comments in the yaml.
import random
import re
import subprocess

import yaml

with open("data.yaml", "r") as file:
    data = yaml.safe_load(file)

problem_id = 1
# regex to look for [letter][digit][digit] at the start
has_problem_id_pattern = re.compile(r"^[a-z]\d\d")

for subject in data["packet"]:
    random.shuffle(data["packet"][subject])
    for idx, location in enumerate(data["packet"][subject]):
        dir, old_filename = location.split("/")
        old_filename_without_id = old_filename
        if has_problem_id_pattern.match(old_filename):
            old_filename_without_id = old_filename[4:]
        new_filename = f"{subject[0].lower()}{problem_id:02d}-{old_filename_without_id}"
        data["packet"][subject][idx] = f"{dir}/{new_filename}"
        problem_id += 1
        subprocess.run(["mv", f"{dir}/{old_filename}", f"{dir}/{new_filename}"])


with open("data.yaml", "w") as file:
    yaml.safe_dump(data, file, indent=2)
