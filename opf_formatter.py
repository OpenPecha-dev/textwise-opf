import os
import uuid
from pathlib import Path
from openpecha.formatters import HFMLFormatter


if __name__ == "__main__":
    pecha_id = "D1115_nam"
    opfs_path = "./opfs"
    hfml_text = f"./hfmls/{pecha_id}/"
    opf_path = f"./opfs/{pecha_id}/{pecha_id}.opf"

    # Converts HFML to OPF
    formatter = HFMLFormatter(output_path=opfs_path)
    formatter.create_opf(hfml_text, pecha_id)