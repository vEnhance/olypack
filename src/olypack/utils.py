import collections
import csv
from pathlib import Path
from typing import Any, DefaultDict

import yaml
from jinja2 import Environment, FileSystemLoader

QUALITY_SCALE = ["UNSUITABLE", "MEDIOCRE", "ACCEPTABLE", "NICE", "EXCELLENT"]
QUALITY_WEIGHTS = [-0.75, -0.5, 0, 1, 1.5]

DIFFICULTY_SCALE = ["< IMO 1", "IMO 1", "IMO 1.5", "IMO 2", "IMO 2.5", "IMO 3", "> IMO 3"]
DIFFICULTY_WEIGHTS = [0.5, 1, 1.5, 2, 2.5, 3, 3.5]


def jinja_env():
    templates_dir = Path(__file__).parent / "jinja-templates"
    return Environment(loader=FileSystemLoader(str(templates_dir)))


def get_individual_authors(author_string: str) -> list[str]:
    author_string = author_string.replace(", and ", ", ")
    author_string = author_string.replace(" and ", ", ")
    return author_string.split(", ")


def remove_latex(text: str) -> str:
    DELETABLE_ENVIRONMENTS = [
        r"\begin{itemize}",
        r"\end{itemize}",
        r"\begin{enumerate}",
        r"\end{enumerate}",
        r"\begin{quote}",
        r"\end{quote}",
    ]

    result = ""
    for line in text.split("\n"):
        if line.strip() in DELETABLE_ENVIRONMENTS:
            result += "\n"
        elif line.strip().startswith(r"\ii"):
            result += line.lstrip().replace(r"\ii", "- ") + "\n"
        else:
            result += line.strip() + "\n"
    return result.strip()


def problem_data_from_filename(filename: str) -> dict[str, Any]:
    with open(filename) as g:
        text = g.read()
        stuff = text.split("\n---\n")
        try:
            metadata_raw, prob, sol = stuff[:3]
        except ValueError:
            print(stuff)
            raise ValueError("Couldn't process " + filename)
        metadata_dict = yaml.load(metadata_raw, Loader=yaml.FullLoader)
        prob = prob.strip()
        sol = sol.strip()
        comments = "" if len(stuff) < 4 else stuff[3].strip()
        author = metadata_dict.get("author")
        desc = metadata_dict.get("desc")
        prev_appear = metadata_dict.get("prev", "")
        assert len(author) < 100, f"Author name {author} too long"

    return {
        "prob_source": filename,
        "prob": prob,
        "sol": sol,
        "desc": desc,
        "prev_appear": prev_appear,
        "author": author,
        "split_authors": get_individual_authors(author),
        "comments": comments,
        "comments_no_latex": remove_latex(comments),
    }


def all_problems() -> dict[str, list[dict[str, Any]]]:
    with open("data.yaml") as f:
        problem_files = yaml.load(f, Loader=yaml.FullLoader)["packet"]

    with open("data.yaml") as f:
        chosen_files = yaml.load(f, Loader=yaml.FullLoader)["test"]
        chosen_files_list = [
            item for sublist in chosen_files.values() for item in sublist
        ]

    n = 0
    problems = {}
    for subject, dir_items in problem_files.items():
        problems[subject] = []
        for prob_source in dir_items:
            n += 1
            letter = subject[0]
            pnum = f"{letter}-{n:02d}"
            pnum_no_dash = f"{letter}{n:02d}"
            problems[subject].append(
                {
                    **problem_data_from_filename(prob_source),
                    "pnum": pnum,
                    "pnum_no_dash": pnum_no_dash,
                    "chosen": chosen_files_list.index(prob_source) + 1
                    if prob_source in chosen_files_list
                    else -1,
                }
            )
    return problems


def avg(x) -> float:
    if len(x) == 0:
        return 0
    else:
        return sum(x) / len(x)


def get_color_string(x, scale_min, scale_max, color_min, color_max):
    m = (scale_max + scale_min) / 2
    a = min(int(100 * 2 * abs(x - m) / (scale_max - scale_min)), 100)
    color = color_min if x < m else color_max
    return r"\rowcolor{%s!%d}" % (color, a) + "\n"


def all_problems_with_ratings() -> list[dict[str, Any]]:
    quality_indices: DefaultDict[str, list[float]] = collections.defaultdict(list)
    difficulty_indices: DefaultDict[str, list[float]] = collections.defaultdict(list)
    quality_avgs: DefaultDict[str, float] = collections.defaultdict(float)
    difficulty_avgs: DefaultDict[str, float] = collections.defaultdict(float)

    problems = [item for subject, items in all_problems().items() for item in items]
    all_keys = [problem["pnum"] for problem in problems]

    # Read data
    with open("ratings.tsv", "r") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            for key in row.keys():
                if key is None or row[key] is None:
                    continue
                if "quality rating" in key:
                    p = key[key.index("[") + 1 :]
                    p = p[: p.index(" ")]
                    r = row[key]
                    r = r.replace(" ", "").upper()
                    if r in QUALITY_SCALE:
                        quality_indices[p].append(QUALITY_SCALE.index(r))
                if "difficulty rating" in key:
                    p = key[key.index("[") + 1 :]
                    p = p[: p.index(" ")]
                    r = row[key]
                    if r in DIFFICULTY_SCALE:
                        difficulty_indices[p].append(DIFFICULTY_SCALE.index(r))

    for key in all_keys:
        quality_avgs[key] = avg([QUALITY_WEIGHTS[i] for i in quality_indices[key]])
        difficulty_avgs[key] = avg(
            [DIFFICULTY_WEIGHTS[i] for i in difficulty_indices[key]]
        )

    quality_color_strings = {
        key: get_color_string(
            quality_avgs[key],
            QUALITY_WEIGHTS[0],
            QUALITY_WEIGHTS[-1],
            "Salmon",
            "green",
        ).strip()
        for key in all_keys
    }

    difficulty_color_strings = {
        key: get_color_string(
            difficulty_avgs[key],
            DIFFICULTY_WEIGHTS[0],
            DIFFICULTY_WEIGHTS[-1],
            "cyan",
            "orange",
        ).strip()
        for key in all_keys
    }

    def rating_info(key):
        return {
            "quality": quality_indices[key],
            "difficulty": difficulty_indices[key],
            "quality_avg": quality_avgs[key],
            "difficulty_avg": difficulty_avgs[key],
            "quality_color": quality_color_strings[key],
            "difficulty_color": difficulty_color_strings[key],
            "overall_popularity_key": (-quality_avgs[key], key),
            "subject_popularity_key": (key[0], -quality_avgs[key], key),
            "overall_difficulty_key": (-difficulty_avgs[key], key),
            "subject_difficulty_key": (key[0], -difficulty_avgs[key], key),
        }

    for i in range(len(problems)):
        problems[i].update(rating_info(problems[i]["pnum"]))

    return problems


def chosen_problems() -> dict[str, list[dict[str, Any]]]:
    problems = all_problems_with_ratings()
    with open("data.yaml") as f:
        chosen_files = yaml.load(f, Loader=yaml.FullLoader)["test"]

    chosen_problems = {}
    for day, prob_list in chosen_files.items():
        chosen_problems[day] = []
        for chosen_filename in prob_list:
            for problem in problems:
                if problem["prob_source"] == chosen_filename:
                    chosen_problems[day].append(problem)
                    break
    return chosen_problems
