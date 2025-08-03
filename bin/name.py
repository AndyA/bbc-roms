#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

import glob
import os
import re

OUTDIR = "roms"


def read_readme(readme_file: str):
    name_map: dict[str, str] = {}
    with open(readme_file, "r", encoding="utf-8") as f:
        lines = f.read().replace("\r", "\n").splitlines()

    for ln in lines:
        ln = ln.strip()
        if m := re.match(r"^(\S+)\s+-\s+(.+)", ln):
            name_map[m.group(1)] = m.group(2)

    return name_map


os.makedirs(OUTDIR, exist_ok=True)
for file in glob.glob("**/!ReadMe", recursive=True):
    dir = os.path.dirname(file)
    for src, dst in read_readme(file).items():
        src_rom = os.path.join(dir, src)
        dst_rom = os.path.join(OUTDIR, f"{dst}.rom")
        if os.path.exists(dst_rom):
            print(f"Skipping {src_rom} -> {dst_rom}, already exists")
            continue
        print(f"Linking {src_rom} to {dst_rom}")
        try:
            os.link(src_rom, dst_rom)
        except FileNotFoundError:
            print(f"Source file {src_rom} does not exist, skipping")

# vim:ts=2:sw=2:sts=2:et:ft=python
