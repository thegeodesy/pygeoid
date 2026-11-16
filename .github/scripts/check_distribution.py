"""Test a built distribution in an isolated environment outside the checkout."""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", choices=["gmeterpy", "pygeoid"])
    parser.add_argument("distribution", choices=["wheel", "sdist"])
    args = parser.parse_args()
    repository = Path(__file__).resolve().parents[2]
    pattern = "*.whl" if args.distribution == "wheel" else "*.tar.gz"
    artifacts = list((repository / "dist").glob(pattern))
    if len(artifacts) != 1:
        raise ValueError("Expected exactly one selected distribution in dist/")
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    environment["PYTHONNOUSERSITE"] = "1"
    with tempfile.TemporaryDirectory(prefix=f"{args.project}-installed-") as directory:
        work = Path(directory)
        venv = work / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
        python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        subprocess.run(
            [
                "uv",
                "pip",
                "install",
                "--python",
                str(python),
                "--upgrade",
                str(artifacts[0]),
                "pytest",
            ],
            check=True,
            env=environment,
        )
        shutil.copytree(
            repository / "tests",
            work / "tests",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        probe = (
            "from pathlib import Path; import sysconfig; "
            f"import {args.project} as package; "
            "assert Path(package.__file__).resolve().is_relative_to("
            "Path(sysconfig.get_path('purelib')).resolve()); "
            "assert package.__version__ not in ('0.0.0', '0+unknown'); "
            "print(package.__version__, package.__file__)"
        )
        subprocess.run(
            [str(python), "-c", probe], cwd=work, env=environment, check=True
        )
        subprocess.run(
            [
                str(python),
                "-m",
                "pytest",
                "tests",
                "-q",
                "-o",
                "addopts=",
                "--import-mode=importlib",
            ],
            cwd=work,
            env=environment,
            check=True,
        )
        if args.project == "gmeterpy":
            for command in ["gabl", "gphone", "loop", "scx2", "vgfit"]:
                subprocess.run(
                    [str(python.parent / command), "--help"],
                    cwd=work,
                    env=environment,
                    check=True,
                )


if __name__ == "__main__":
    main()
