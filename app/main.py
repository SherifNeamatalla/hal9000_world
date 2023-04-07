from config.env_loader import load_env
from runners.auto_gpt_runner import AutoGptRunner
from util.config_util import init_app_config

load_env()


def main():
    init_app_config()
    runner = AutoGptRunner()
    runner.run()


if __name__ == "__main__":
    main()
