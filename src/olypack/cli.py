"""Command-line interface for olypack."""

import shutil
import subprocess
import sys
from pathlib import Path

import click
import markdown

from .pdf import encrypt_pdf
from .produce_packet import generate_packet
from .produce_receipts import generate_receipts
from .produce_scores import generate_scores
from .produce_test import generate_test
from .shuffle_packet import shuffle_packet


@click.group()
@click.version_option(version="1.0.0", prog_name="olypack")
def main():
    """olypack - Package for managing olympiad problem packets."""
    pass


@main.command()
@click.option("--dry-run", is_flag=True, help="Show what would be installed without installing")
@click.option("-f", "--force", is_flag=True, help="Overwrite existing files")
def install(dry_run: bool, force: bool):
    """
    Install required LaTeX and Asymptote files.

    Checks for latexmk and TEXMFHOME, then downloads required .sty and .asy files.
    """
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
            Path(texmfhome) / "tex/latex/evan.sty",
        ),
        (
            "TST.sty",
            "https://raw.githubusercontent.com/vEnhance/dotfiles/main/texmf/tex/latex/TST/TST.sty",
            Path(texmfhome) / "tex/latex/TST.sty",
        ),
        (
            "natoly.sty",
            "https://raw.githubusercontent.com/vEnhance/dotfiles/main/texmf/tex/latex/TST/natoly.sty",
            Path(texmfhome) / "tex/latex/natoly.sty",
        ),
        (
            "von.sty",
            "https://raw.githubusercontent.com/vEnhance/dotfiles/main/texmf/tex/latex/von/von.sty",
            Path(texmfhome) / "tex/latex/von.sty",
        ),
        (
            "olympiad.asy",
            "https://raw.githubusercontent.com/vEnhance/dotfiles/main/asy/olympiad.asy",
            Path.home() / ".asy/olympiad.asy",
        ),
    ]

    for filename, url, target_path in files_to_fetch:
        # Check if file exists
        existing_files = []
        if filename.endswith(".asy"):
            search_dir = Path.home() / ".asy"
            if search_dir.exists():
                existing_files = list(search_dir.rglob(filename))
        else:
            if Path(texmfhome).exists():
                existing_files = list(Path(texmfhome).rglob(filename))

        if existing_files and not force:
            click.echo(f"✓ {filename} already exists at {existing_files[0]}")
            continue

        if dry_run:
            click.echo(f"Would download {filename} to {target_path}")
            continue

        # Download the file
        click.echo(f"Downloading {filename}...")
        target_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            import urllib.request

            urllib.request.urlretrieve(url, target_path)
            click.echo(f"✓ Downloaded {filename} to {target_path}")
        except Exception as e:
            click.echo(f"✗ Failed to download {filename}: {e}", err=True)

    if not dry_run:
        # Run mktexlsr to update the TeX file database
        click.echo("Updating TeX file database...")
        try:
            subprocess.run(["mktexlsr", texmfhome], check=True)
            click.echo("✓ Installation complete!")
        except subprocess.CalledProcessError as e:
            click.echo(f"Warning: Failed to run mktexlsr: {e}", err=True)


@main.command()
@click.argument("target_dir", type=click.Path(), default=".", required=False)
def init(target_dir: str):
    """
    Initialize a new olympiad packet project using copier template.

    TARGET_DIR is the directory where the project will be created (default: current directory).
    """
    try:
        from copier import run_copy
    except ImportError:
        click.echo("Error: copier is not installed. Install with: pip install copier", err=True)
        sys.exit(1)

    template_dir = Path(__file__).parent.parent.parent / "template"
    if not template_dir.exists():
        click.echo(f"Error: Template directory not found at {template_dir}", err=True)
        sys.exit(1)

    click.echo(f"Initializing project in {target_dir}...")
    run_copy(str(template_dir), target_dir, unsafe=True)
    click.echo("✓ Project initialized!")


@main.command()
def shuffle():
    """Randomly shuffle the packet order for each subject."""
    click.echo("Shuffling packet...")
    shuffle_packet()
    click.echo("✓ Packet shuffled!")


@main.command()
def packet():
    """Generate packet PDFs (problems and solutions)."""
    click.echo("Generating packet data files...")
    generate_packet()

    click.echo("Building packet PDFs...")
    _run_latexmk("packet/internal-NO-SEND-probs.tex")
    _run_latexmk("packet/internal-NO-SEND-solns.tex")

    # Encrypt PDFs
    click.echo("Encrypting PDFs...")
    password = _read_password()
    encrypt_pdf("packet/internal-NO-SEND-probs.pdf", "output/confidential-probs.pdf", password)
    encrypt_pdf("packet/internal-NO-SEND-solns.pdf", "output/confidential-solns.pdf", password)

    click.echo("✓ Packet generated!")


@main.command()
def report():
    """Generate the final report PDF."""
    click.echo("Generating report data...")
    generate_scores()

    click.echo("Building report PDF...")
    _run_latexmk("final-report/final-NO-SEND-report.tex")

    # Encrypt PDF
    click.echo("Encrypting PDF...")
    password = _read_password()
    encrypt_pdf(
        "final-report/final-NO-SEND-report.pdf", "output/confidential-report.pdf", password
    )

    click.echo("✓ Report generated!")


@main.command()
def test():
    """Generate the test PDFs."""
    click.echo("Generating test materials...")
    generate_test()

    click.echo("Building test PDFs...")
    _run_latexmk("test/final-probs.tex")
    _run_latexmk("test/final-solns.tex")

    # Encrypt PDFs
    click.echo("Encrypting PDFs...")
    password = _read_password()
    encrypt_pdf("test/final-probs.pdf", "test/final-probs-encrypted.pdf", password)
    encrypt_pdf("test/final-solns.pdf", "test/final-solns-encrypted.pdf", password)

    click.echo("✓ Test generated!")


@main.command()
def receipt():
    """Generate receipt HTML for authors."""
    click.echo("Generating receipt...")
    generate_receipts()

    # Convert markdown to HTML
    with open("output/receipt.mkd", "r") as f:
        md_content = f.read()

    html_content = markdown.markdown(md_content)

    with open("output/receipt.html", "w") as f:
        f.write(html_content)

    click.echo("✓ Receipt generated!")


def _run_latexmk(tex_file: str):
    """Run latexmk on a TeX file."""
    tex_path = Path(tex_file)
    if not tex_path.exists():
        click.echo(f"Error: {tex_file} not found", err=True)
        sys.exit(1)

    try:
        subprocess.run(["latexmk", "-cd", "-pdf", str(tex_path)], check=True)
        # Touch the output file
        pdf_path = tex_path.with_suffix(".pdf")
        pdf_path.touch()
    except subprocess.CalledProcessError as e:
        click.echo(f"Error: latexmk failed for {tex_file}", err=True)
        sys.exit(1)


def _read_password() -> str:
    """Read password from password file."""
    password_file = Path("password")
    if not password_file.exists():
        click.echo("Error: password file not found", err=True)
        sys.exit(1)

    with open(password_file, "r") as f:
        return f.read().strip()


if __name__ == "__main__":
    main()
