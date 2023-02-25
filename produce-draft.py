import os
import subprocess
import tempfile

import yaml

__version__ = "2020-05"

tmp_dir_path = tempfile.mkdtemp()
OUTPUT_PATH = "output/"

with open("password") as f:
    PASSWORD = f.readline().strip()

with open("data.yaml") as f:
    yaml_data = yaml.load(f, Loader=yaml.FullLoader)
    chosen_problems = yaml_data["chosen"]
    DRAFT_PATH = yaml_data["draft"]
    assert os.path.exists(DRAFT_PATH), DRAFT_PATH + " does not exist"

code_to_path = {}
with open("output/authors.tsv") as f:
    for line in f:
        code = line.strip().split("\t")[0]
        path = line.strip().split("\t")[-1]
        code_to_path[code] = path

N = 0
for n, day in chosen_problems.items():
    # Make problems
    problems_filename = "draft-problems-day%d.pdf" % n
    problems_tmp_path = os.path.join(tmp_dir_path, problems_filename)
    problems_enc_path = os.path.join(OUTPUT_PATH, problems_filename)
    subprocess.call(
        ["qpdf", "--empty", "--pages", DRAFT_PATH, str(n), "--", problems_tmp_path]
    )
    subprocess.call(
        [
            "qpdf",
            "--encrypt",
            PASSWORD,
            PASSWORD,
            "256",
            "--print=none",
            "--modify=none",
            "--",
            problems_tmp_path,
            problems_enc_path,
        ]
    )

    # Compile solutions
    raw_sol_tex_path = os.path.join(tmp_dir_path, "s%d.tex" % n)
    raw_sol_pdf_path = os.path.join(tmp_dir_path, "s%d.pdf" % n)
    with open(raw_sol_tex_path, "w") as f:
        print(r"\documentclass[11pt]{scrartcl}", file=f)
        print(r"\usepackage[sexy]{evan}", file=f)
        print(r"\title{Preliminary solutions to day %d}" % n, file=f)
        print(r"\author{Confidential}", file=f)
        print(r"\begin{document}", file=f)
        print(r"\maketitle", file=f)
        print(r"\tableofcontents", file=f)
        print(r"\newpage", file=f)
        print(r"\setcounter{section}{%d}" % N, file=f)
        print("\n", file=f)

        for code in day:
            problem_path = code_to_path[code]
            with open(problem_path) as g:
                text = "".join(g.readlines())
                stuff = text.split("\n---\n")
                try:
                    metadata_raw, prob, sol = stuff[0:3]
                except ValueError:
                    print(stuff)
                    raise ValueError(f"Couldn't process {problem_path}")
                prob = prob.strip()
                sol = sol.strip()
                metadata_dict = yaml.load(metadata_raw, Loader=yaml.FullLoader)
                desc = metadata_dict.get("desc")
            N += 1
            print(r"\section{%s}" % desc, file=f)
            print(prob, file=f)
            print("\n", file=f)
            print(r"\hrulebar", file=f)
            print("\n", file=f)
            print(sol, file=f)
            print(r"\newpage", file=f)
            print("\n", file=f)
        print(r"\end{document}", file=f)
    subprocess.call(["latexmk", "-cd", raw_sol_tex_path])

    # Make solutions
    solutions_filename = "draft-soln-day%d.pdf" % n
    solutions_tmp_path = raw_sol_pdf_path
    solutions_enc_path = os.path.join(OUTPUT_PATH, solutions_filename)
    subprocess.call(
        [
            "qpdf",
            "--encrypt",
            PASSWORD,
            PASSWORD,
            "256",
            "--print=none",
            "--modify=none",
            "--",
            solutions_tmp_path,
            solutions_enc_path,
        ]
    )
