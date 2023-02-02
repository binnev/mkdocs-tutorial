import shutil
import subprocess
from pathlib import Path
from . import calculator

LIBRARY_NAME = "mkdocs-tutorial"
version = calculator.__version__


def cleanup():
    for folder in [
        Path(__file__).parent / f"{LIBRARY_NAME}.egg-info",
        Path(__file__).parent / "dist",
        Path(__file__).parent / "site",
    ]:
        if folder.exists():
            shutil.rmtree(folder)


if __name__ == "__main__":
    cleanup()
    # subprocess.run("python -m build".split())
    # subprocess.run("twine upload dist/*".split())
    subprocess.run(f"mike deploy {version}".split())
    subprocess.run(f"mike alias {version} latest --update-aliases".split())
    subprocess.run(f"mike set-default latest --push".split())
    cleanup()
