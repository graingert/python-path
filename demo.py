import subprocess
import sys
import tempfile
import pathlib
import contextlib
import venv


@contextlib.contextmanager
def _tmp_path():
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield pathlib.Path(tmp_dir)


def demo(mode):
    with _tmp_path() as tmp_path:
        v = tmp_path / "venv"
        venv.EnvBuilder(with_pip=True).create(v)
        subprocess.run(
            [
                v / "bin" / "python",
                "-m",
                "pip",
                "install",
                *(("-e",) if mode == "editable" else ()),
                "src/example_setup",
            ],
            check=True,
        )
        subprocess.run(
            [
                v / "bin" / "python",
                "-m",
                "pip",
                "install",
                *(("-e",) if mode == "editable" else ()),
                "src/example_pyproject",
            ],
            check=True,
        )
        subprocess.run(
            [
                v / "bin" / "python",
                "-c",
                "import example_setup; print(example_setup.source)",
            ],
            check=True,
        )
        print(f"=== setup.py {mode=} succeeded ===")
        subprocess.run(
            [
                v / "bin" / "python",
                "-c",
                "import example_pyproject; print(example_pyproject.source)",
            ],
            check=True,
        )
        print(f"=== pyproject {mode=} succeeded ===")


def main():
    demo("regular")
    demo("editable")


if __name__ == "__main__":
    sys.exit(main())
