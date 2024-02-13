#!/usr/bin/python3

__version__ = "2024-02"

import yaml
from jinja2 import Environment, FileSystemLoader

with open("data.yaml") as f:
    problems = yaml.load(f, Loader=yaml.FullLoader)["packet"]

total_problems = sum(len(x) for x in problems.values())
unique_authors = set()


def get_individual_authors(author_string: str) -> list[str]:
    author_string = author_string.replace(", and ", ", ")
    author_string = author_string.replace(" and ", ", ")
    return author_string.split(", ")

n = 0
problems = {}

for subject, dir_items in problems.items():
    problems[subject] = []
    for prob_source in dir_items:
        n += 1
        with open(prob_source) as g:
            text = "".join(g.readlines())
            stuff = text.split("\n---\n")
            try:
                metadata_raw, prob, sol = stuff[0:3]
            except ValueError:
                print(stuff)
                raise ValueError("Couldn't process " + prob_source)
            metadata_dict = yaml.load(metadata_raw, Loader=yaml.FullLoader)
            prob = prob.strip()
            author = metadata_dict.get("author")
            desc = metadata_dict.get("desc")
            letter = metadata_dict.get("letter", subject[0])
            prev_appear = metadata_dict.get("prev", "")
            sol = sol.strip()
            assert len(author) < 100, f"Author name {author} too long"
        pnum = f"{letter}-{n:02d}"
        pnum_no_dash = f"{letter}{n:02d}"

        for a in get_individual_authors(author):
            unique_authors.add(a)
        problems[subject].append({
            'prob_source': prob_source,
            'prob': prob.strip(),
            'sol': sol.strip(),
            'desc': desc,
            'pnum': pnum,
            'pnum_no_dash': pnum_no_dash,
            'prev_appear': prev_appear,
            'author': author,
        })

with open("output/uniqauthor.txt", "w") as f:
    print(",\n".join(sorted(unique_authors)), file=f)

env = Environment(loader=FileSystemLoader('olypack/jinja-templates'))


with open("tex/data-probs.tex", "w") as f:
    template = env.get_template('data-probs.tex.jinja')
    f.write(template.render(problems=problems))

with open("tex/data-solns.tex", "w") as f:
    template = env.get_template('data-solns.tex.jinja')
    f.write(template.render(problems=problems))

with open("tex/data-index.tex", "w") as f:
    template = env.get_template('data-index.tex.jinja')
    f.write(template.render(problems=problems, total_problems=total_problems))

with open("output/authors.tsv", "w") as f:
    template = env.get_template('authors.tsv.jinja')
    f.write(template.render(problems=problems))

with open("output/form-script.js", "w") as f:
    template = env.get_template('form-script.js.jinja')
    f.write(template.render(problems=problems))
