import os
import shutil
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
import tempfile
import zipfile
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from constants.constants import DATABASE_NAME, PATH_FOR_BACKUP

# SMTP_PASS = "dnJFEDGc2pfVuH9kVvwa"
# SMTP_SERVER = "smtp.mail.ru"
# SMTP_USER = "ekaputkin@mail.ru"
# SMTP_PORT = 465
SQLALCHEMY_DATABASE_URL = f"sqlite:///./{DATABASE_NAME}"


# def _send_email( subject, body):
#     """Отправляет лог по почте (если настроено в config.ini)."""
#     # if not self.config.has_section("EMAIL"):
#     #     self._log_message("Ошибка: Нет секции [EMAIL] в config.ini")
#     #     return False
#
#     recipient = "ayukhovich@mail.ru"
#
#     try:
#         subject = "Создание копии БД"
#         msg = MIMEMultipart()
#         msg['From'] = SMTP_USER
#         msg['To'] = recipient
#         msg['Subject'] = subject
#
#         # Прикрепляем лог-файл
# #        with open(self.log_file, "r", encoding="utf-8") as f:
# #            log_content = f.read()
#         msg.attach(MIMEText(body + "\n\nЛог:\n" + "log_content", "plain"))
#
#         # Отправка через SMTP
#         print("111")
#         with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
#             print("222")
#             server.login( SMTP_USER, SMTP_PASS)
#             print("333")
#             server.send_message(msg)
#             print("444")
#
#         #self._log_message(f"Письмо отправлено на {recipient}")
#         print(f"Письмо отправлено на {recipient}")
#         return True
#     except Exception as e:
#         #self._log_message(f"Ошибка отправки письма: {e}")
#         print(f"Ошибка отправки письма: {e}")
#         return False

def _send_email(subject, body):
    print(f"{body}")
    # pass


def backup_db_if_exists(db_path):
    if not os.path.exists(db_path):
        return
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")

    base_name, ext = os.path.splitext(db_path)
    backup_path = f"{base_name}_{yesterday_str}{ext}"

    # Формируем имя для резервной копии (без расширения)
    base_name, ext = os.path.splitext(db_path)
    backup_name = f"{base_name}_{yesterday_str}"
    backup_db_path = f"{backup_name}{ext}"  # Полный путь к копии БД
    backup_zip_path = backup_zip_path = os.path.join(PATH_FOR_BACKUP, f"{backup_name}.zip")

    # Если архив уже существует, ничего не делаем
    if os.path.exists(backup_zip_path):
        # _send_email("[Datelite]", f"Создана временная копия: {backup_db_path}")
        return

    temp_filename = tempfile.mktemp(suffix='.db')
    # Создаём временную копию файла БД
    try:
        try:
            shutil.copy2(db_path, temp_filename)
            # _send_email("[Datelite]", f"Создана временная копия: {temp_filename}")
        except Exception as e:
            # print(f"Ошибка при создании временной копии: {e}")
            return

        # Архивируем файл в ZIP
        try:
            with zipfile.ZipFile(backup_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(temp_filename, arcname=backup_db_path)
                # print(f"Создан архив: {backup_zip_path}")
        except Exception as e:
            # print(f"Ошибка при создании архива: {e}")
            # _send_email("[Datelite]", "Ошибка при создании архива:")
            return
    finally:
        # Удаляем временный файл вручную
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


# backup_db_if_exists(DATABASE_NAME)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
engine.echo = False

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
