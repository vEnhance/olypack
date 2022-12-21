#!/usr/bin/python3

__version__ = "2021-10"

import yaml

with open("data.yaml") as f:
    problems = yaml.load(f, Loader=yaml.FullLoader)["packet"]

total_problems = sum(len(x) for x in problems.values())

with open("tex/data-probs.tex", "w") as pf, open("tex/data-solns.tex", "w") as sf, open(
    "tex/data-index.tex", "w"
) as xf, open("output/authors.tsv", "w") as af:
    n = 0

    if total_problems > 0:
        print(r"\begin{description}[itemsep=2pt]", file=xf)

    for subject, dir_items in problems.items():
        print(r"\section{" + subject + "}", file=pf)
        print(r"\section{" + subject + "}", file=sf)
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
                sol = sol.strip()
                assert len(author) < 100, "Author name %s too long" % author
            pnum = f"{letter}-{n:02d}"
            print(r"\renewcommand{\theprob}{%s}" % (pnum), file=pf)
            print(r"\begin{prob}", file=pf)
            print(prob, file=pf)
            print(r"\end{prob}", file=pf)
            print("\n", file=pf)

            print(r"\subsection{Solution %s (%s)}" % (pnum, desc), file=sf)
            print(prob, file=sf)
            print("\n" * 2 + r"\bigskip\hrulebar\bigskip" + "\n" * 2, file=sf)
            print(sol, file=sf)
            print(r"\newpage", file=sf)

            print("\t".join([pnum, author, desc, prob_source]), file=af)
            print(r"\item[%s] %s" % (pnum, desc), file=xf)
        print(r"\newpage", file=pf)
    if total_problems > 0:
        print(r"\end{description}", file=xf)
