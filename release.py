import shutil
import subprocess
from pathlib import Path
import calculator
import glob

LIBRARY_NAME = "mkdocs-ci-cd-sandbox-binnev"
version = calculator.__version__


def cleanup():
    paths = ["dist", "site", ".pytest_cache"]
    paths += glob.glob("*.egg-info")
    paths += glob.glob("*.pytest_cache")
    for path in paths:
        path = Path(__file__).parent / path
        if path.exists():
            shutil.rmtree(path)


def check(question: str):
    response = input(question)
    if response.lower() not in ["y", "yes"]:
        raise Exception(f"Action required")


if __name__ == "__main__":
    print(f"Releasing version {version}")
    cleanup()
    check(f"Did you create / update the Version changelog for version {version}?\n")

    print("Building package")
    subprocess.run("python -m build".split())
    subprocess.run("twine check dist/*".split())
    print("PyPI test run")
    subprocess.run("twine upload -r pypitest dist/*".split())
    check(f"Does the testpypi output look OK?\n")

    # print("PyPI deploy")
    # subprocess.run("twine upload dist/*".split())

    print("Building docs")
    subprocess.run(f"mike deploy {version}".split())
    subprocess.run(f"mike alias {version} latest --update-aliases".split())
    try:
        process = subprocess.run("mike serve".split())
    except KeyboardInterrupt:
        pass
    check("Do the docs look OK?\n")
    subprocess.run("mike list".split())
    check("Does the list of docs versions look OK?")
    subprocess.run(f"mike set-default latest --push".split())
    cleanup()
