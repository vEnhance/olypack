"""Command-line interface for olypack."""

import shutil
import subprocess
import sys

import click


@click.group()
@click.version_option(version="1.0.0", prog_name="olypack")
def main():
    """olypack - Copier template for managing olympiad problem packets."""
    pass


@main.command()
@click.argument("destination", default=".", required=False)
@click.option("--template", "--source", default="gh:vEnhance/olypack", help="Template source URL")
def setup(destination: str, template: str):
    """
    Set up a new olympiad packet project using copier.

    DESTINATION is the directory where the project will be created (default: current directory).
    """
    try:
        from copier import run_copy
    except ImportError:
        click.echo("Error: copier is not installed.", err=True)
        click.echo("Install it with: pip install copier", err=True)
        sys.exit(1)

    click.echo(f"Initializing project from {template} in {destination}...")
    try:
        run_copy(
            template,
            destination,
            unsafe=True,
            answers_file=".copier-answers.yml"
        )
        click.echo("✓ Project initialized!")
        click.echo(f"✓ Questionnaire answers saved to {destination}/.copier-answers.yml")
    except Exception as e:
        click.echo(f"Error: Failed to initialize project: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("destination", default=".", required=False)
def update(destination: str):
    """
    Update an existing project from its original template.

    DESTINATION is the project directory to update (default: current directory).
    """
    try:
        from copier import run_update
    except ImportError:
        click.echo("Error: copier is not installed.", err=True)
        click.echo("Install it with: pip install copier", err=True)
        sys.exit(1)

    click.echo(f"Updating project in {destination}...")
    try:
        run_update(destination, unsafe=True, skip_answered=True)
        click.echo("✓ Project updated!")
    except Exception as e:
        click.echo(f"Error: Failed to update project: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option("--dry-run", is_flag=True, help="Show what would be installed without installing")
@click.option("-f", "--force", is_flag=True, help="Overwrite existing files")
def install(dry_run: bool, force: bool):
    """
    Install required LaTeX and Asymptote files, and set up pre-commit hooks.

    Checks for latexmk and TEXMFHOME, then downloads required .sty and .asy files.
    Also installs prek hooks if in a git repository.
    """
    # Check if we're in a git repository
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        click.echo("Error: Not in a git repository. Please run this command from within a git repository.", err=True)
        sys.exit(1)

    # Check for latexmk
    if not shutil.which("latexmk"):
        click.echo("Error: latexmk is not installed. Please install LaTeX.", err=True)
        sys.exit(1)

    # Check for TEXMFHOME
    try:
        result = subprocess.run(
            ["kpsewhich", "-var-value=TEXMFHOME"],
            capture_output=True,
            text=True,
            check=True,
        )
        texmfhome = result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        click.echo("Error: Could not determine TEXMFHOME directory.", err=True)
        sys.exit(1)

    if not texmfhome:
        click.echo("Error: TEXMFHOME is not set.", err=True)
        sys.exit(1)

    click.echo(f"TEXMFHOME: {texmfhome}")

    # Files to download
    files_to_fetch = [
        (
            "evan.sty",
            "https://raw.githubusercontent.com/vEnhance/dotfiles/main/texmf/tex/latex/evan/evan.sty",
            f"{texmfhome}/tex/latex/evan.sty",
        ),
        (
            "TST.sty",
            "https://raw.githubusercontent.com/vEnhance/dotfiles/main/texmf/tex/latex/TST/TST.sty",
            f"{texmfhome}/tex/latex/TST.sty",
        ),
        (
            "natoly.sty",
            "https://raw.githubusercontent.com/vEnhance/dotfiles/main/texmf/tex/latex/TST/natoly.sty",
            f"{texmfhome}/tex/latex/natoly.sty",
        ),
        (
            "von.sty",
            "https://raw.githubusercontent.com/vEnhance/dotfiles/main/texmf/tex/latex/von/von.sty",
            f"{texmfhome}/tex/latex/von.sty",
        ),
        (
            "olympiad.asy",
            "https://raw.githubusercontent.com/vEnhance/dotfiles/main/asy/olympiad.asy",
            f"{str(subprocess.run(['sh', '-c', 'echo $HOME'], capture_output=True, text=True).stdout.strip())}/.asy/olympiad.asy",
        ),
    ]

    from pathlib import Path
    import urllib.request

    for filename, url, target_path in files_to_fetch:
        target = Path(target_path)

        # Check if file exists
        if target.exists() and not force:
            click.echo(f"✓ {filename} already exists at {target}")
            continue

        if dry_run:
            click.echo(f"Would download {filename} to {target}")
            continue

        # Download the file
        click.echo(f"Downloading {filename}...")
        target.parent.mkdir(parents=True, exist_ok=True)

        try:
            urllib.request.urlretrieve(url, target)
            click.echo(f"✓ Downloaded {filename} to {target}")
        except Exception as e:
            click.echo(f"✗ Failed to download {filename}: {e}", err=True)

    if not dry_run:
        # Run mktexlsr to update the TeX file database
        click.echo("Updating TeX file database...")
        try:
            subprocess.run(["mktexlsr", texmfhome], check=True)
        except subprocess.CalledProcessError as e:
            click.echo(f"Warning: Failed to run mktexlsr: {e}", err=True)

        # Install prek hooks
        click.echo("Installing pre-commit hooks with prek...")
        try:
            subprocess.run(["prek", "install"], check=True)
            click.echo("✓ Pre-commit hooks installed!")
        except subprocess.CalledProcessError as e:
            click.echo(f"Warning: Failed to install prek hooks: {e}", err=True)
        except FileNotFoundError:
            click.echo("Warning: prek command not found. Hooks not installed.", err=True)

        click.echo("✓ Installation complete!")
    else:
        click.echo("\nDry run complete. Would also install prek hooks.")


if __name__ == "__main__":
    main()
