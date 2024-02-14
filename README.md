# olypack

This is intended to be a git submodule used within git directories
where USA team selection tests or other olympiad-style exams are being prepared.
It automates the setup of some boilerplate for problem proposal packets
and provides a `Makefile` that works with these systems.

While it was written for in-house use, it could still possibly be useful to
others, so this repository was made public.

## Installation

```bash
git submodule add https://github.com/vEnhance/olypack
cd olypack
./init.sh
```

Obtain the required sty files:
```bash
./install_sty.sh
```

## Commands

When initialized, a `Makefile` appears in the directory where the `olypack`
submodule was initialized. It allows the following commands:

- `make packet`: produce the packet
- `make report`: produce the final report
- `make receipt`: produce comments that can be sent to authors on their problems
- `make draft`: produce a draft of the solutions packet

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
