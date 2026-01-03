# olypack

A copier template for managing olympiad problem packets used for USA team selection
tests and other olympiad-style exams. It provides a complete workflow for problem
collection, review, and test generation.

## Quick Start

### 1. Install olypack (one-time setup)

First, install the olypack package which provides the `olypack` command for setup:

```bash
# Using uv (recommended)
uv tool install git+https://github.com/vEnhance/olypack

# Or using pipx
pipx install git+https://github.com/vEnhance/olypack
```

### 2. Create a new project

Use copier to create a new project from the template:

```bash
# Create a new directory for your test
copier copy gh:vEnhance/olypack my-test-2026
cd my-test-2026
```

Copier will ask you questions about your test (name, author, deadlines, etc.) and
generate a customized project.

### 3. Install LaTeX dependencies

From within your project directory, run:

```bash
olypack install
```

This command will:
- Check that `latexmk` is installed
- Verify `TEXMFHOME` is set correctly
- Download required style files (`evan.sty`, `TST.sty`, `natoly.sty`, `von.sty`)
- Download required Asymptote files (`olympiad.asy`)
- Install pre-commit hooks with prek
- Update the TeX file database

Options:
- `--dry-run`: Preview what would be installed
- `--force` or `-f`: Overwrite existing files

### 4. Work with your packet

Your project includes:
- `Makefile` for building PDFs
- `olypack/` directory with Python utilities
- `packet/`, `test/`, `final-report/` directories for LaTeX files
- `data.yaml` for configuring which problems to include

## Commands

The generated project includes a `Makefile` with these targets:

- `make shuffle`: Randomly shuffle the packet order for each subject
- `make packet`: Generate packet PDFs (problems and solutions)
- `make report`: Generate the final report PDF
- `make test`: Generate the test PDFs
- `make receipt`: Generate receipt HTML for authors

You can also use the Python commands directly:

```bash
python3 olypack.py shuffle    # Shuffle problems
python3 olypack.py packet     # Generate packet data
python3 olypack.py test       # Generate test materials
python3 olypack.py scores     # Generate final report scores
python3 olypack.py receipts   # Generate receipts
python3 olypack.py encrypt INPUT.pdf OUTPUT.pdf password  # Encrypt a PDF
```

## System Requirements

olypack requires LaTeX to be installed on your system:

- **Ubuntu/Debian**: `sudo apt install texlive-full`
- **macOS**: Install [MacTeX](https://www.tug.org/mactex/)
- **Windows**: Install [MiKTeX](https://miktex.org/) or [TeX Live](https://www.tug.org/texlive/)

Python dependencies are managed with the generated project.

## Customization

The generated project includes all Python scripts in the `olypack/` directory, which
you can freely edit and customize for your specific needs. This is intentional - the
scripts are meant to be modified per-project as needed.
