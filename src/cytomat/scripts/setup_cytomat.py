import os
import shutil
import sys
from pathlib import Path

def get_config_dir():
    return Path('C:/ProgramData/Cytomat')

def get_sample_path():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent.parent

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
        else:
            print("Ordner existiert bereits")

    except Exception as e:
        print(f"""  Path couldn't be created:{e}")
                    -
                    Please Create manualy the path:{config_dir}")
                    -
                    after that please copy: {sample_config_file} into that directory""")

    try:
        if not config_file.exists():
            shutil.copy2(sample_config_file, config_file)
            print(f"copied sample configs to: {config_dir}")
    except Exception as e:
        print(f"""  Error:{e}
                    -
                    Please copy: {sample_config_file} into: {config_dir}""")

def post_install():
    print("running post install")
    setup_config_dir()

if __name__ == "__main__":
    print(__name__)
    post_install()