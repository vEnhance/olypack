# olypack

A Python package for managing olympiad problem packets used for USA team selection
tests and other olympiad-style exams. It automates the setup of boilerplate for
problem proposal packets and provides commands for generating PDFs.

While it was written for in-house use, it could still possibly be useful to
others, so this repository was made public.

## Installation

Install olypack using uv or pip:

```bash
# Using uv (recommended)
uv pip install .

# Or using pip
pip install .

# Or install in development mode
pip install -e .
```

### System Requirements

olypack requires LaTeX to be installed on your system, as it uses `latexmk` to
compile PDFs. Install LaTeX before using olypack:

- **Ubuntu/Debian**: `sudo apt install texlive-full`
- **macOS**: Install [MacTeX](https://www.tug.org/mactex/)
- **Windows**: Install [MiKTeX](https://miktex.org/) or [TeX Live](https://www.tug.org/texlive/)

### Installing LaTeX Style Files

After installing olypack, run the install command to download required `.sty` and
`.asy` files:

```bash
# Install required LaTeX and Asymptote files
olypack install

# Preview what would be installed without actually installing
olypack install --dry-run

# Force overwrite existing files
olypack install --force
```

This command will:
- Check that `latexmk` is installed
- Verify `TEXMFHOME` is set correctly
- Download required style files (`evan.sty`, `TST.sty`, `natoly.sty`, `von.sty`)
- Download required Asymptote files (`olympiad.asy`)
- Update the TeX file database

## Quick Start

Initialize a new project:

```bash
# Create a new directory and initialize a project
mkdir my-test-2025
cd my-test-2025
olypack init

# Or initialize in the current directory
olypack init .
```

The `init` command will prompt you for information about your test (name, author,
deadline, etc.) and set up the project structure with all necessary files.

## Commands

olypack provides the following commands:

- `olypack shuffle`: Randomly shuffle the packet order for each subject
- `olypack packet`: Generate packet PDFs (problems and solutions)
- `olypack report`: Generate the final report PDF
- `olypack test`: Generate the test PDFs
- `olypack receipt`: Generate receipt HTML for authors

For convenience, a `Makefile` is also generated that wraps these commands:

- `make shuffle`: same as `olypack shuffle`
- `make packet`: same as `olypack packet`
- `make report`: same as `olypack report`
- `make test`: same as `olypack test`
- `make receipt`: same as `olypack receipt`

## Format used for storing

Each individual submission is stored as a single TeX file in a format similar to
that used for the [VON](https://github.com/vEnhance/von) database.
There are three parts:

1. The metadata for the problem. This has three fields:

   - `desc`: (required) A one-line description of the problem.
   - `author`: (required) The authors of the problem,
     comma-separated list if more than one author.
   - `prev`: (optional) A list of places the problem was previously sent.

   Additional keys are allowed, but not currently used.

2. Statement of the problem.
3. Solution to the problem.

These parts are separated by the magic string `---`:
three hyphens, surrounded by blank newlines.

Thus, an example submission could look like:

```latex
desc: Poodles are not cats (insert a one-line description of the problem here)
author: Ellie Example, Sammy Sample (replace this with names of all authors)
prev: TSTST 2010 packet G-24 (list of previous packet appearances)

---

Let $\mathbf{P}$ denote the set of poodles and $\mathbf{NP}$ denote the set of
non-deterministic poodles (that is, animals that could plausibly be poodles).
Does $\mathbf{P} = \mathbf{NP}$?

---

We show that a poodle is not a cat.
Since cats are in $\mathbf{NP}$, it will follow $\mathbf{P} \neq \mathbf{NP}$.

% In the packet, a claim* environment is provided for claims.
% (There is an analogous lemma* environment and remark* environment.)

\begin{lemma*}
  A poodle is a dog.
\end{lemma*}
\begin{proof}
  Well-known.
\end{proof}

\begin{claim*}
  A dog is not a cat.
\end{claim*}
\begin{proof}
  We use barycentric coordinates.
\end{proof}

\begin{remark*}
  You can add any remarks to the problem using the \texttt{remark*} environment.
\end{remark*}
```
