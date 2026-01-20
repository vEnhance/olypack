#!/usr/bin/python3


import os

from utils import all_problems, jinja_env, problem_data_from_filename

__version__ = "2024-08"

problems = all_problems()
unique_authors = set()

# We look at all the files in source/ so that we find authors who submitted but
# didn't have any problems included in the packet
problems_directory = "source/"
for filename in os.listdir(problems_directory):
    if filename.endswith(".tex"):
        filepath = os.path.join(problems_directory, filename)
        problem = problem_data_from_filename(filepath)
        unique_authors.update(problem["split_authors"])


with open("packet/uniqauthor.txt", "w") as f:
    f.write(",\n".join(sorted(unique_authors)))

env = jinja_env()


with open("packet/data-probs.tex", "w") as f:
    template = env.get_template("data-probs.tex.jinja")
    f.write(template.render(problems=problems))

with open("packet/data-solns.tex", "w") as f:
    template = env.get_template("data-solns.tex.jinja")
    f.write(template.render(problems=problems))

with open("packet/data-index.tex", "w") as f:
    template = env.get_template("data-index.tex.jinja")
    f.write(template.render(problems=problems))

with open("output/form-script.js", "w") as f:
    template = env.get_template("form-script.js.jinja")
    f.write(template.render(problems=problems))
