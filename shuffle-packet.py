# Randomly shuffles the packet order for each subject.
# Note: doesn't preserve comments.
import random

import yaml

with open("data.yaml", "r") as file:
    data = yaml.safe_load(file)

for subject in data["packet"]:
    random.shuffle(data["packet"][subject])

with open("data.yaml", "w") as file:
    yaml.safe_dump(data, file, indent=2)
