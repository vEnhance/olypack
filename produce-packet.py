#!/usr/bin/python3

__version__ = "2024-02"

import yaml
from utils import jinja_env, problem_data_from_filename

with open("data.yaml") as f:
    problem_files = yaml.load(f, Loader=yaml.FullLoader)["packet"]

total_problems = sum(len(x) for x in problem_files.values())
unique_authors = set()

n = 0
problems = {}

for subject, dir_items in problem_files.items():
    problems[subject] = []
    for prob_source in dir_items:
        n += 1
        letter = subject[0]
        pnum = f"{letter}-{n:02d}"
        pnum_no_dash = f"{letter}{n:02d}"
        problem_data_dict = problem_data_from_filename(prob_source)

        unique_authors.update(problem_data_dict["split_authors"])

        problem_data_dict["pnum"] = pnum
        problem_data_dict["pnum_no_dash"] = pnum_no_dash
        problems[subject].append(problem_data_dict)

with open("output/uniqauthor.txt", "w") as f:
    f.write(",\n".join(sorted(unique_authors)))

env = jinja_env()


with open("tex/data-probs.tex", "w") as f:
    template = env.get_template("data-probs.tex.jinja")
    f.write(template.render(problems=problems))

with open("tex/data-solns.tex", "w") as f:
    template = env.get_template("data-solns.tex.jinja")
    f.write(template.render(problems=problems))

with open("tex/data-index.tex", "w") as f:
    template = env.get_template("data-index.tex.jinja")
    f.write(template.render(problems=problems, total_problems=total_problems))

with open("output/authors.tsv", "w") as f:
    template = env.get_template("authors.tsv.jinja")
    f.write(template.render(problems=problems))

with open("output/form-script.js", "w") as f:
    template = env.get_template("form-script.js.jinja")
    f.write(template.render(problems=problems))
