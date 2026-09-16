from src.core.database import engine
from src.migrations.runner import MigrationRunner


def main() -> None:
    version = MigrationRunner(engine).upgrade()
    print(f"Database schema upgraded to version {version}.")


if __name__ == "__main__":
    main()
