#!/usr/bin/env python3
"""olypack command-line tool for the template."""

import sys

import click

from olypack.utils import encrypt_pdf


@click.group()
def main():
    """olypack utilities for managing olympiad problem packets."""
    pass


@main.command()
@click.argument("input_pdf")
@click.argument("output_pdf")
@click.argument("password_file")
def encrypt(input_pdf: str, output_pdf: str, password_file: str):
    """Encrypt a PDF file with a password from a file."""
    with open(password_file, "r") as f:
        password = f.read().strip()

    encrypt_pdf(input_pdf, output_pdf, password)
    click.echo(f"✓ Encrypted {input_pdf} -> {output_pdf}")


@main.command()
def shuffle():
    """Shuffle the packet problems."""
    import subprocess
    subprocess.run([sys.executable, "olypack/shuffle-packet.py"], check=True)


@main.command()
def packet():
    """Generate packet data files."""
    import subprocess
    subprocess.run([sys.executable, "olypack/produce-packet.py"], check=True)


@main.command()
def test():
    """Generate test materials."""
    import subprocess
    subprocess.run([sys.executable, "olypack/produce-test.py"], check=True)


@main.command()
def scores():
    """Generate final report scores."""
    import subprocess
    subprocess.run([sys.executable, "olypack/produce-scores.py"], check=True)


@main.command()
def receipts():
    """Generate receipts."""
    import subprocess
    subprocess.run([sys.executable, "olypack/produce-receipts.py"], check=True)


if __name__ == "__main__":
    main()
