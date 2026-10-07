"""Application settings."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

# Новая база для актуальной ER-модели.
# Старую housing.db не трогаем.
DATABASE_PATH = DATA_DIR / "housing_v2.db"

APP_NAME = "Мониторинг расходов ЖКХ"

APP_VERSION = "0.2.0"