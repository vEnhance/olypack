import os

from utils import chosen_problems, jinja_env

env = jinja_env()

if os.path.exists("test/problems-1.tex"):
    res = input(
        "Problem files already exist. If you are using those to edit the statements, note that this command will OVERWRITE those files. Continue? (y/N)"
    )
    if res.lower() != "y":
        exit()

for day, problems in chosen_problems().items():
    with open(f"test/problems-{day}.tex", "w") as f:
        template = env.get_template("problems-day.tex.jinja")
        f.write(template.render(problems=problems))
    with open(f"test/solutions-{day}.tex", "w") as f:
        template = env.get_template("solutions-day.tex.jinja")
        f.write(template.render(problems=problems, day=day))
