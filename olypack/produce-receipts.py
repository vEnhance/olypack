#!/usr/bin/env python3
"""Generate receipt markdown for authors."""

from pathlib import Path

from olypack.utils import all_problems_with_ratings, jinja_env, DIFFICULTY_SCALE

QUALITY_RATINGS = ["Unsuitable", "Mediocre", "Acceptable", "Nice", "Excellent"]


Path("output").mkdir(exist_ok=True)
env = jinja_env()

with open("output/receipt.mkd", "w") as f:
    problems = all_problems_with_ratings()
    template = env.get_template("receipt.mkd.jinja")
    f.write(
        template.render(
            problems=problems,
            QUALITY_RATINGS=QUALITY_RATINGS,
            DIFFICULTY_RATINGS=DIFFICULTY_SCALE,
        )
    )
