import os
from dataclasses import dataclass
from functools import cached_property
from typing import Optional, Self

SLOT_SIZE = 0x4000


@dataclass(kw_only=True, frozen=True)
class SidewaysRom:
    name: str = ""
    bin: bytes

    @classmethod
    def from_file(cls, file_path: str) -> Self:
        # Placeholder for actual file reading logic
        # This should read the file and return an instance of SidewaysRom
        name: str = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            bin = f.read()
        if len(bin) > SLOT_SIZE:
            raise ValueError(
                f"File {name} is too large for a sideways ROM (max {SLOT_SIZE} bytes)"
            )
        return cls(name=name, bin=bin)

    @cached_property
    def padded(self) -> bytes:
        """Return the ROM data padded to the full slot size."""
        return self.bin.ljust(SLOT_SIZE, b"\xff")


@dataclass(kw_only=True, frozen=True)
class FatRom:
    size: int
    roms: list[Optional[SidewaysRom]]

    @cached_property
    def padded(self) -> bytes:
        if len(self.roms) > self.size:
            raise ValueError(
                f"Too many ROMs for FatRom (max {self.size}, got {len(self.roms)})"
            )
        slots: list[bytes] = []
        empty = SidewaysRom(bin=b"", name="Empty ROM")
        for rom in self.roms:
            rom = rom or empty
            slots.append(rom.padded)
        while len(slots) < self.size:
            slots.append(empty.padded)
        return b"".join(slots)


roms: list[Optional[FatRom]] = [
    None,  # Sideways RAM
    FatRom(
        size=4,
        roms=[
            SidewaysRom.from_file("roms/View version A3.0.rom"),
            SidewaysRom.from_file("roms/Viewsheet 1.00.rom"),
            SidewaysRom.from_file("roms/FORTH.rom"),
            SidewaysRom.from_file("roms/BASIC Editor 1.32.rom"),
        ],
    ),
    FatRom(
        size=4,
        roms=[
            SidewaysRom.from_file("roms/COMAL.rom"),
            SidewaysRom.from_file("roms/LISP.rom"),
            SidewaysRom.from_file("roms/Termulator 1.00.rom"),
            SidewaysRom.from_file("roms/Disc Doctor 1.09.rom"),
        ],
    ),
    FatRom(
        size=4,
        roms=[
            SidewaysRom.from_file("roms/m-uts.rom"),
            SidewaysRom.from_file("roms/DNFS.rom"),
            SidewaysRom.from_file("roms/ADFS 1.53.rom"),
            SidewaysRom.from_file("roms/BBC BASIC version 2.rom"),
        ],
    ),
]

for slot, fat_rom in enumerate(roms):
    if fat_rom is not None:
        print(f"{slot:>2} Fat ROM")
        for i, rom in enumerate(fat_rom.roms):
            vslot = slot * 4 + i
            if rom is not None:
                print(f"  {vslot:>2} {rom.name}")
            else:
                print(f"  {vslot:>2} Empty")
    else:
        print(f"{slot:>2} Empty")

OUT = "tmp/fat"
os.makedirs(OUT, exist_ok=True)
for slot, fat_rom in enumerate(roms):
    if fat_rom is not None:
        with open(os.path.join(OUT, f"fat-{slot:02}.rom"), "wb") as f:
            f.write(fat_rom.padded)
