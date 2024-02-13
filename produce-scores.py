import collections
import csv
from typing import DefaultDict, List

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


def format_avg(x, s: str):
    if len(x) == 0:
        return "---"
    else:
        return s % avg(x)


WT_U = -0.75
WT_M = -0.5
WT_A = 0
WT_N = 1
WT_E = 1.5


def criteria(k):
    a = avg(qualities[k])
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
                if r == "UNSUITABLE":
                    qualities[p].append(WT_U)
                elif r == "MEDIOCRE":
                    qualities[p].append(WT_M)
                elif r == "ACCEPTABLE":
                    qualities[p].append(WT_A)
                elif r == "NICE":
                    qualities[p].append(WT_N)
                elif r == "EXCELLENT":
                    qualities[p].append(WT_E)
            if "difficulty rating" in key:
                p = key[key.index("[") + 1 :]
                p = p[: p.index(" ")]
                r = row[key]
                r = r.replace(" ", "").upper()
                if r == "IMO1":
                    difficulties[p].append(1)
                elif r == "IMO1,IMO2":
                    difficulties[p].append(1.5)
                elif r == "IMO2":
                    difficulties[p].append(2)
                elif r == "IMO2,IMO3":
                    difficulties[p].append(2.5)
                elif r == "IMO3":
                    difficulties[p].append(3)

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
    color_tex = get_color_string(a, WT_U, WT_E, "Salmon", "green")
    row_tex = r"%s & %d & %d & %d & %d & %d & %s \\" % (
        get_label(key, slugged),
        data.count(WT_U),
        data.count(WT_M),
        data.count(WT_A),
        data.count(WT_N),
        data.count(WT_E),
        format_avg(data, "$%+4.2f$"),
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
        data.count(1),
        data.count(1.5),
        data.count(2),
        data.count(2.5),
        data.count(3),
        format_avg(data, "%.3f"),
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
        lambda p: (-avg(qualities[p]), p),
        False,
    )
    print_everything(
        "Beauty contest, by subject and popularity",
        lambda p: (p[0], -avg(qualities[p]), p),
        False,
    )
    print_everything(
        "Beauty contest, by overall difficulty",
        lambda p: (-avg(difficulties[p]), p),
        True,
    )
    print_everything(
        "Beauty contest, by subject and difficulty",
        lambda p: (p[0], -avg(difficulties[p]), p),
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
        x = avg(difficulties[p])
        y = avg(qualities[p])
        print("%0.2f\t%0.2f\t%s\t%s" % (x, y, p[2:], p[0]))
    print(r"};")
    print(r"\end{axis}")
    print(r"\end{tikzpicture}")
    print(r"\end{center}")
else:
    print("No ratings to display here yet")

with open("output/summary.csv", "w") as f:
    for p in sorted(qualities.keys()):
        qs = ",".join(
            str(qualities[p].count(x)) for x in (WT_U, WT_M, WT_A, WT_N, WT_E)
        )
        ds = ",".join(str(difficulties[p].count(x)) for x in (1, 1.5, 2, 2.5, 3))
        print(f'{p},"{slugs[p]}","{authors[p]}",{qs},{ds}', file=f)
