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

## Commands

When initialized, a `Makefile` appears in the directory where the `olypack`
submodule was initialized. It allows the following commands:

- `make packet`: produce the packet
- `make report`: produce the final report
- `make receipt`: produce comments that can be sent to authors on their problems
- `make draft`: produce a draft of the solutions packet
