#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261120 (Python 3.13, stdlib only).

The entry image is entry.png beside this file; this program copies it to
the output directory. Outside the grader's container, MAKEFUN_OUTPUT_DIR
stands in for /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEST = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

DEST.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", DEST / "entry.png")
