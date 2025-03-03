import os
import shutil
import sys
from pathlib import Path


def find_file_in_meipass(filename):
    if not getattr(sys, "frozen", False):
        raise RuntimeError(
            "The Script has to executed as .exe file (by using Pyinstaller)."
        )

    meipass_dir = sys._MEIPASS
    for root, dirs, files in os.walk(meipass_dir):
        if filename in files:
            return os.path.join(root, filename)

    return None


def get_config_dir():
    return Path("C:/ProgramData/Cytomat")


def get_sample_path():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent.parent / "data"

    sample_config_file = base_path / "sample_config.json"
    return sample_config_file


def setup_config_dir():
    config_dir = get_config_dir()
    config_file = config_dir / "config.json"
    sample_config_file = get_sample_path()
    print(sample_config_file)

    try:
        if not config_dir.exists():
            os.mkdir(config_dir)
            print(f"Created: {config_dir}")

    except Exception as e:
        print(
            f"""  Path couldn't be created:{e}")
                    -
                    Please Create manualy the path:{config_dir}")
                    -
                    after that please copy: {sample_config_file} into that directory"""
        )

    try:
        if not config_file.exists():
            shutil.copy2(sample_config_file, config_file)
            print(f"copied sample configs to: {config_dir}")
    except Exception as e:
        print(
            f"""  Error:{e}
                    -
                    Please copy: {sample_config_file} into: {config_dir}"""
        )


def post_install():
    print("running post install")
    setup_config_dir()


def find():
    filename_to_find = "sample_config.json"
    full_path = find_file_in_meipass(filename_to_find)

    if full_path:
        print(f"Die Datei '{filename_to_find}' wurde gefunden unter: {full_path}")
    else:
        print(
            f"Die Datei '{filename_to_find}' wurde im _MEIPASS Ordner nicht gefunden."
        )


if __name__ == "__main__":
    print(__name__)
    post_install()
