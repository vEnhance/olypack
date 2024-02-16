import yaml
from jinja2 import Environment, FileSystemLoader


def jinja_env():
    return Environment(loader=FileSystemLoader("olypack/jinja-templates"))


def get_individual_authors(author_string: str) -> list[str]:
    author_string = author_string.replace(", and ", ", ")
    author_string = author_string.replace(" and ", ", ")
    return author_string.split(", ")


def problem_data_from_filename(filename: str) -> dict:
    with open(filename) as g:
        text = g.read()
        stuff = text.split("\n---\n")
        try:
            metadata_raw, prob, sol = stuff[0:3]
        except ValueError:
            print(stuff)
            raise ValueError("Couldn't process " + filename)
        metadata_dict = yaml.load(metadata_raw, Loader=yaml.FullLoader)
        prob = prob.strip()
        author = metadata_dict.get("author")
        desc = metadata_dict.get("desc")
        prev_appear = metadata_dict.get("prev", "")
        sol = sol.strip()
        assert len(author) < 100, f"Author name {author} too long"

    return {
        "prob_source": filename,
        "prob": prob.strip(),
        "sol": sol.strip(),
        "desc": desc,
        "prev_appear": prev_appear,
        "author": author,
        "split_authors": get_individual_authors(author),
    }
