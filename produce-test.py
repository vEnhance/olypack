from utils import chosen_problems, jinja_env

env = jinja_env()

for day, problems in chosen_problems().items():
    with open(f"test/problems-{day}.tex", "w") as f:
        template = env.get_template("problems-day.tex.jinja")
        f.write(template.render(problems=problems))
    with open(f"test/solutions-{day}.tex", "w") as f:
        template = env.get_template("solutions-day.tex.jinja")
        f.write(template.render(problems=problems, day=day))
