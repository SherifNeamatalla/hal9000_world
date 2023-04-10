from config.env_loader import load_env
from config.saved_app_configs import PYTHON_APP_CONFIG_NAME
from runners.python_app_runner_v2 import PythonAppV2Runner
from util.config_util import init_app_config

load_env()


def main():
    init_app_config(PYTHON_APP_CONFIG_NAME)
    runner = PythonAppV2Runner()
    runner.run()


if __name__ == "__main__":
    main()
