import shutil
import subprocess
from pathlib import Path

LIBRARY_NAME = "mkdocs-tutorial"
VERSION = "5.1"


def cleanup():
    for folder in [
        Path(__file__).parent / f"{LIBRARY_NAME}.egg-info",
        Path(__file__).parent / "dist",
        Path(__file__).parent / "site",
    ]:
        if folder.exists():
            shutil.rmtree(folder)

if __name__ == '__main__':
    cleanup()
    # subprocess.run("python -m build".split())
    # subprocess.run("twine upload dist/*".split())
    subprocess.run(f"mike deploy {VERSION}".split())
    subprocess.run(f"mike alias {VERSION} latest --update-aliases".split())
    subprocess.run(f"mike deploy {VERSION} --push".split())
    cleanup()
