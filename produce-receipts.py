from utils import all_problems_with_ratings, jinja_env

env = jinja_env()

QUALITY_RATINGS = ["Unsuitable", "Mediocre", "Acceptable", "Nice", "Excellent"]
DIFFICULTY_RATINGS = ["IMO 1", "IMO 1.5", "IMO 2", "IMO 2.5", "IMO 3"]

with open("output/receipt.mkd", "w") as f:
    problems = all_problems_with_ratings()
    template = env.get_template("receipt.mkd.jinja")
    f.write(
        template.render(
            problems=problems,
            QUALITY_RATINGS=QUALITY_RATINGS,
            DIFFICULTY_RATINGS=DIFFICULTY_RATINGS,
        )
    )
