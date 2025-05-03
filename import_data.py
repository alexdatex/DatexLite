import logging
from typing import Dict, Any

import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

from db import DBController, SessionLocal, init_db
from db import Equipment

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataImporter:
    def __init__(self):
        self.db = SessionLocal()
        self.db_controller = DBController(self.db)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    @staticmethod
    def get_array_element(arr: list, index: int, default_value: Any) -> Any:
        """Безопасное получение элемента массива по индексу."""
        try:
            value = arr[index] if arr[index] is not None else default_value
            if str(value) == "nan":
                return default_value
            else:
                return value
        except IndexError:
            return default_value

    @staticmethod
    def prepare_data(data_in: Dict[str, Any]) -> Dict[str, str]:
        """Подготовка данных: преобразование в строки и создание lowercase версий."""
        data_out = {}
        for name, value in data_in.items():
            str_value = str(value).strip() if value is not None else ""
            data_out[name] = str_value
            data_out[f"{name}_lower"] = str_value.lower()
        return data_out

    def add_equipment(self, data: Dict[str, Any]) -> bool:
        """Добавление оборудования в базу данных."""
        try:
            equipment = Equipment(
                **data,
                user_id=0,
                is_deleted=False
            )
            self.db.add(equipment)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Ошибка при добавлении оборудования: {e}")
            return False

    def import_excel_data(self, file_path: str, sheet_name: int = 0) -> None:
        """Импорт данных из Excel файла."""
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            logger.info(f"Найдено {len(df.columns)} колонок и {len(df)} строк")

            success_count = 0
            for row in df.itertuples(index=False):
                data = {
                    "group_name": self.get_array_element(row, 0, ""),
                    "korpus": self.get_array_element(row, 1, ""),
                    "position": self.get_array_element(row, 2, ""),
                    "code": self.get_array_element(row, 3, ""),
                    "name": self.get_array_element(row, 4, ""),
                    "purpose": self.get_array_element(row, 5, ""),
                    "manufacturer": self.get_array_element(row, 6, ""),
                    "type": self.get_array_element(row, 7, ""),
                    "serial_number": self.get_array_element(row, 8, ""),
                    "production_date": self.get_array_element(row, 9, "")
                }

                if self.add_equipment(self.prepare_data(data)):
                    success_count += 1

            logger.info(f"Успешно импортировано {success_count} из {len(df)} записей")

        except Exception as e:
            logger.error(f"Ошибка при импорте данных: {e}")
            raise


def main():
    init_db()

    print("Программа для импорта данных из Excel файла")
    print("------------------------------------------")

    try:
        with DataImporter() as importer:
            importer.import_excel_data("data.xlsx")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
    finally:
        print("\nРабота программы завершена.")


if __name__ == "__main__":
    main()
