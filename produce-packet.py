#!/usr/bin/python3

__version__ = "2024-02"

import yaml

from utils import all_problems, jinja_env

with open("data.yaml") as f:
    problem_files = yaml.load(f, Loader=yaml.FullLoader)["packet"]

total_problems = 0

problems = all_problems()
unique_authors = set()
for subject, problem_list in problems.items():
    total_problems += len(problem_list)
    for problem in problem_list:
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
    f.write(template.render(problems=problems, total_problems=total_problems))

with open("output/form-script.js", "w") as f:
    template = env.get_template("form-script.js.jinja")
    f.write(template.render(problems=problems))
