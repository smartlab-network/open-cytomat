import sys

sys.path.insert(1, "C:/labhub/Repos/smartlab-network/open-cytomat/src")

from cytomat.config import load_config  # noqa: E402

config = load_config()

print(config.com_port)
