import sys
import os.path


def init_path():
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


class EsCfg:
    hosts = ['10.11.3.190:1024']

