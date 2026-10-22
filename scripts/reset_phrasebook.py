"""Delete the local phrasebook and seed the three sample entries again."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db import get_db_path, init_db


def main() -> None:
    path = get_db_path()
    if path.exists():
        path.unlink()
    init_db()
    print(f"Reset {path}")
    print("Seeded the Vale family sample entries.")


if __name__ == "__main__":
    main()
