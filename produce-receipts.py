from utils import all_problems_with_ratings, jinja_env, DIFFICULTY_SCALE

env = jinja_env()

QUALITY_RATINGS = ["Unsuitable", "Mediocre", "Acceptable", "Nice", "Excellent"]

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
