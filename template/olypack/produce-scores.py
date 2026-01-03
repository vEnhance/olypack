#!/usr/bin/env python3
"""Generate final report scores and tables."""

from pathlib import Path

from olypack.utils import all_problems, all_problems_with_ratings, chosen_problems, jinja_env


Path("final-report").mkdir(exist_ok=True)
env = jinja_env()

with open("final-report/table.tex", "w") as f:
    problems = all_problems_with_ratings()
    filtered_problems = [p for p in problems if p["quality_avg"] >= 0]
    if problems:
        template = env.get_template("table.tex.jinja")
        f.write(
            template.render(
                problems=problems,
                filtered_problems=filtered_problems,
            )
        )
    else:
        f.write("No ratings to display here yet\n")

with open("final-report/comments.tex", "w") as f:
    template = env.get_template("comments.tex.jinja")
    f.write(
        template.render(
            problems=all_problems(),
        )
    )

with open("final-report/author-table.tex", "w") as f:
    template = env.get_template("author-table.tex.jinja")
    f.write(
        template.render(
            problems=chosen_problems(),
        )
    )
