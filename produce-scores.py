import collections
import csv
from typing import DefaultDict, List

from utils import jinja_env

__version__ = "2024-02"

quality_indices: DefaultDict[str, List[float]] = collections.defaultdict(list)
difficulty_indices: DefaultDict[str, List[float]] = collections.defaultdict(list)
quality_avgs: DefaultDict[str, float] = collections.defaultdict(float)
difficulty_avgs: DefaultDict[str, float] = collections.defaultdict(float)
slugs = {}
authors = {}


def avg(x) -> float:
    if len(x) == 0:
        return 0
    else:
        return sum(x) / len(x)


QUALITY_SCALE = ["UNSUITABLE", "MEDIOCRE", "ACCEPTABLE", "NICE", "EXCELLENT"]
QUALITY_WEIGHTS = [-0.75, -0.5, 0, 1, 1.5]

DIFFICULTY_SCALE = ["IMO1", "IMO1,IMO2", "IMO2", "IMO2,IMO3", "IMO3"]
DIFFICULTY_WEIGHTS = [1, 1.5, 2, 2.5, 3]


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
                r = r.replace(" ", "").upper()
                if r in DIFFICULTY_SCALE:
                    difficulty_indices[p].append(DIFFICULTY_SCALE.index(r))

with open("output/authors.tsv") as f:
    for line in f:
        p, author, slug, filename, *_ = line.strip().split("\t")
        authors[p] = author
        slugs[p] = slug
        quality_avgs[p] = avg([QUALITY_WEIGHTS[i] for i in quality_indices[p]])
        difficulty_avgs[p] = avg([DIFFICULTY_WEIGHTS[i] for i in difficulty_indices[p]])


def get_color_string(x, scale_min, scale_max, color_min, color_max):
    m = (scale_max + scale_min) / 2
    a = min(int(100 * 2 * abs(x - m) / (scale_max - scale_min)), 100)
    color = color_min if x < m else color_max
    return r"\rowcolor{%s!%d}" % (color, a) + "\n"


quality_color_strings = {
    key: get_color_string(
        quality_avgs[key], QUALITY_WEIGHTS[0], QUALITY_WEIGHTS[-1], "Salmon", "green"
    ).strip()
    for key in quality_avgs
}

difficulty_color_strings = {
    key: get_color_string(
        difficulty_avgs[key],
        DIFFICULTY_WEIGHTS[0],
        DIFFICULTY_WEIGHTS[-1],
        "cyan",
        "orange",
    ).strip()
    for key in difficulty_avgs
}


def serialized(key):
    return {
        "key": key,
        "quality": quality_indices[key],
        "difficulty": difficulty_indices[key],
        "quality_avg": quality_avgs[key],
        "difficulty_avg": difficulty_avgs[key],
        "quality_color": quality_color_strings[key],
        "difficulty_color": difficulty_color_strings[key],
        "slug": slugs[key],
        "overall_popularity_key": (-quality_avgs[key], key),
        "subject_popularity_key": (key[0], -quality_avgs[key], key),
        "overall_difficulty_key": (-difficulty_avgs[key], key),
        "subject_difficulty_key": (key[0], -difficulty_avgs[key], key),
        "table_text": "%0.2f\t%0.2f\t%s\t%s"
        % (difficulty_avgs[key], quality_avgs[key], key[2:], key[0]),
    }


problems = [serialized(key) for key in quality_indices]

filtered_problems = [
    serialized(key) for key in quality_indices if quality_avgs[key] >= 0
]

with open("final-report/table.txt", "w") as f:
    if len(difficulty_indices) > 0 or len(quality_indices) > 0:
        env = jinja_env()
        template = env.get_template("table.txt.jinja")
        f.write(
            template.render(
                problems=problems,
                filtered_problems=filtered_problems,
            )
        )
    else:
        f.write("No ratings to display here yet\n")

with open("output/summary.csv", "w") as f:
    for p in sorted(quality_indices.keys()):
        qs = ",".join(
            str(quality_indices[p].count(x)) for x in range(len(QUALITY_WEIGHTS))
        )
        ds = ",".join(
            str(difficulty_indices[p].count(x)) for x in range(len(DIFFICULTY_WEIGHTS))
        )
        print(f'{p},"{slugs[p]}","{authors[p]}",{qs},{ds}', file=f)
