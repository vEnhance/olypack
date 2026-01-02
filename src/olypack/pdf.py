"""PDF operations using pikepdf."""

from pathlib import Path

import pikepdf
from pikepdf import Permissions


def encrypt_pdf(input_path: str | Path, output_path: str | Path, password: str) -> None:
    """
    Encrypt a PDF with a password.

    Args:
        input_path: Path to the input PDF file
        output_path: Path to the output encrypted PDF file
        password: Password to use for encryption
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    with pikepdf.open(input_path) as pdf:
        # Encrypt with AES-256, no printing or modification allowed
        pdf.save(
            output_path,
            encryption=pikepdf.Encryption(
                user=password,
                owner=password,
                allow=Permissions(print_lowres=False, modify_assembly=False),
            ),
        )
