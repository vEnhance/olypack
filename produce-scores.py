import collections
import csv
from typing import DefaultDict, List
from jinja2 import Environment, FileSystemLoader

__version__ = "2023-02"

qualities: DefaultDict[str, List[float]] = collections.defaultdict(list)
difficulties: DefaultDict[str, List[float]] = collections.defaultdict(list)
slugs = {}
authors = {}


def avg(x) -> float:
    if len(x) == 0:
        return 0
    else:
        return sum(x) / len(x)


def format_avg(x, score_mapping: list[float], s: str):
    if len(x) == 0:
        return "---"
    else:
        return s % avg([score_mapping[i] for i in x])


QUALITY_SCALE = ["UNSUITABLE", "MEDIOCRE", "ACCEPTABLE", "NICE", "EXCELLENT"]
QUALITY_WEIGHTS = [-0.75, -0.5, 0, 1, 1.5]

DIFFICULTY_SCALE = ["IMO1", "IMO1,IMO2", "IMO2", "IMO2,IMO3", "IMO3"]
DIFFICULTY_WEIGHTS = [1, 1.5, 2, 2.5, 3]

def criteria(k):
    a = avg([QUALITY_WEIGHTS[i] for i in qualities[k]])
    return a is not None and a >= 0


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
                    qualities[p].append(QUALITY_SCALE.index(r))
            if "difficulty rating" in key:
                p = key[key.index("[") + 1 :]
                p = p[: p.index(" ")]
                r = row[key]
                r = r.replace(" ", "").upper()
                if r in DIFFICULTY_SCALE:
                    difficulties[p].append(DIFFICULTY_SCALE.index(r))

with open("output/authors.tsv") as f:
    for line in f:
        p, author, slug, filename, *_ = line.strip().split("\t")
        authors[p] = author
        slugs[p] = slug


def get_color_string(x, scale_min, scale_max, color_min, color_max):
    m = (scale_max + scale_min) / 2
    a = min(int(100 * 2 * abs(x - m) / (scale_max - scale_min)), 100)
    color = color_min if x < m else color_max
    return r"\rowcolor{%s!%d}" % (color, a) + "\n"


def get_label(key, slugged=False):
    if slugged:
        return r"{\scriptsize \textbf{%s} %s}" % (key, slugs.get(key, ""))
    else:
        return r"{\scriptsize \textbf{%s}}" % key


## Quality rating
def get_quality_row(key, data, slugged=True):
    a = avg(data)
    color_tex = get_color_string(a, QUALITY_WEIGHTS[0], QUALITY_WEIGHTS[-1], "Salmon", "green")
    row_tex = r"%s & %d & %d & %d & %d & %d & %s \\" % (
        get_label(key, slugged),
        data.count(0),
        data.count(1),
        data.count(2),
        data.count(3),
        data.count(4),
        format_avg(data, QUALITY_WEIGHTS, "$%+4.2f$"),
    )
    return color_tex + row_tex


def print_quality_table(d, sort_key=None, slugged=True):
    items = sorted(d.items(), key=sort_key)
    print(r"\begin{tabular}{lcccccr}")
    print(r"\toprule Prob & U & M & A & N & E & Avg \\ \midrule")
    for key, data in items:
        print(get_quality_row(key, data, slugged))
    print(r"\bottomrule")
    print(r"\end{tabular}")


## Difficulty rating
def get_difficulty_row(key, data, slugged=False):
    a = avg(data)
    color_tex = get_color_string(a, 1, 3, "cyan", "orange")
    row_tex = r"%s & %d & %d & %d & %d & %d & %s \\" % (
        get_label(key, slugged),
        data.count(0),
        data.count(1),
        data.count(2),
        data.count(3),
        data.count(4),
        format_avg(data, DIFFICULTY_WEIGHTS, "%.3f"),
    )
    return color_tex + row_tex


def print_difficulty_table(d, sort_key=None, slugged=False):
    items = sorted(d.items(), key=sort_key)
    print(r"\begin{tabular}{l ccccc c}")
    print(r"\toprule Prob & 1 & 1.5 & 2 & 2.5 & 3 & Avg \\ \midrule")
    for key, data in items:
        print(get_difficulty_row(key, data, slugged))
    print(r"\bottomrule")
    print(r"\end{tabular}")


filtered_qualities = {k: v for k, v in qualities.items() if criteria(k)}
filtered_difficulties = {k: v for k, v in difficulties.items() if criteria(k)}


def print_everything(name, fn=None, flip_slug=False):
    if fn is not None:
        sort_key = lambda item: fn(item[0])
    else:
        sort_key = None
    print(r"\section{" + name + "}")
    if flip_slug:
        print_quality_table(filtered_qualities, sort_key, False)
        print_difficulty_table(filtered_difficulties, sort_key, True)
    else:
        print_quality_table(filtered_qualities, sort_key, True)
        print_difficulty_table(filtered_difficulties, sort_key, False)


if len(difficulties) > 0 or len(qualities) > 0:
    print(r"\section{All ratings}")
    print_quality_table(qualities)
    print_difficulty_table(difficulties)

    print("\n" + r"\newpage" + "\n")
    print_everything(
        "Beauty contest, by overall popularity",
        lambda p: (-avg([QUALITY_WEIGHTS[i] for i in qualities[p]]), p),
        False,
    )
    print_everything(
        "Beauty contest, by subject and popularity",
        lambda p: (p[0], -avg([QUALITY_WEIGHTS[i] for i in qualities[p]]), p),
        False,
    )
    print_everything(
        "Beauty contest, by overall difficulty",
        lambda p: (-avg([DIFFICULTY_WEIGHTS[i] for i in difficulties[p]]), p),
        True,
    )
    print_everything(
        "Beauty contest, by subject and difficulty",
        lambda p: (p[0], -avg([DIFFICULTY_WEIGHTS[i] for i in difficulties[p]]), p),
        True,
    )

    print("\n")
    print(r"\section{Scatter plot}")
    print(r"\begin{center}")
    print(r"\begin{tikzpicture}")
    print(
        r"""\begin{axis}[width=0.9\textwidth, height=22cm, grid=both,
    xlabel={Average difficulty}, ylabel={Average suitability},
    every node near coord/.append style={font=\scriptsize},
    scatter/classes={A={red},C={blue},G={green},N={black}}]"""
    )
    print(
        r"""\addplot [scatter,
    only marks, point meta=explicit symbolic,
    nodes near coords*={\prob},
    visualization depends on={value \thisrow{prob} \as \prob}]"""
    )
    print(r"table [meta=subj] {")
    print("X\tY\tprob\tsubj")
    for p in qualities.keys():
        x = avg([DIFFICULTY_WEIGHTS[i] for i in difficulties[p]])
        y = avg([QUALITY_WEIGHTS[i] for i in qualities[p]])
        print("%0.2f\t%0.2f\t%s\t%s" % (x, y, p[2:], p[0]))
    print(r"};")
    print(r"\end{axis}")
    print(r"\end{tikzpicture}")
    print(r"\end{center}")
else:
    print("No ratings to display here yet")

env = Environment(loader=FileSystemLoader('olypack/jinja-templates'))

with open("final-report/table-test.txt", "w") as f:
    template = env.get_template('table.txt.jinja')
    f.write(template.render())

with open("output/summary.csv", "w") as f:
    for p in sorted(qualities.keys()):
        qs = ",".join(
            str(qualities[p].count(x)) for x in range(len(QUALITY_WEIGHTS))
        )
        ds = ",".join(str(difficulties[p].count(x)) for x in range(len(DIFFICULTY_WEIGHTS)))
        print(f'{p},"{slugs[p]}","{authors[p]}",{qs},{ds}', file=f)
