import shutil
import subprocess
from pathlib import Path
import calculator

LIBRARY_NAME = "mkdocs-ci-cd-sandbox-binnev"
version = calculator.__version__


def cleanup():
    for folder in [
        Path(__file__).parent / f"{LIBRARY_NAME}.egg-info",
        Path(__file__).parent / "dist",
        Path(__file__).parent / "site",
    ]:
        if folder.exists():
            shutil.rmtree(folder)


def ask(question: str):
    response = input(question)
    if response.lower() not in ["y", "yes"]:
        raise Exception(f"Action required")


if __name__ == "__main__":
    print(f"Releasing version {version}")
    cleanup()
    ask(f"Did you create / update the Version changelog for version {version}?\n")

    print("Building package")
    subprocess.run("python -m build".split())
    subprocess.run("twine check dist/*".split())
    print("PyPI test run")
    subprocess.run("twine upload -r pypitest dist/*".split())
    ask(f"Does the testpypi output look OK?\n")

    # print("PyPI deploy")
    # subprocess.run("twine upload dist/*".split())

    print("Building docs")
    subprocess.run(f"mike deploy {version}".split())
    subprocess.run(f"mike alias {version} latest --update-aliases".split())
    try:
        process = subprocess.run("mike serve".split())
    except KeyboardInterrupt:
        pass
    ask("Do the docs look OK?\n")

    # subprocess.run(f"mike set-default latest --push".split())
    cleanup()
