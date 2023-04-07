from config.env_loader import load_env
from runners.auto_gpt_runner import AutoGptRunner

load_env()


def main():
    runner = AutoGptRunner()
    runner.run()


if __name__ == "__main__":
    main()
