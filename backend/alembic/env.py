from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from app.core.config import settings
from app.db.base import Base

# استيراد صريح لكل الموديلات لضمان تسجيلها في Base.metadata قبل أي
# عملية autogenerate أو migration
from app.db import models  # noqa: F401

# كائن الإعدادات الخاص بـ Alembic (من alembic.ini)
config = context.config

# فرض استخدام رابط قاعدة البيانات من إعدادات التطبيق (settings)، بدلاً من
# الاعتماد على القيمة الثابتة الموجودة في alembic.ini
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# تفعيل إعدادات الـ logging من alembic.ini إن كانت موجودة وصحيحة الصياغة.
# لو الملف ناقص أقسام logging (مشكلة شائعة بعد alembic init)، نتجاهل
# الخطأ بدل ما نوقف تنفيذ المهاجرات بالكامل — الـ logging تفصيلة ثانوية
# ومش المفروض توقف عملية حرجة زي schema migration.
if config.config_file_name is not None:
    try:
        fileConfig(config.config_file_name)
    except Exception as e:
        print(f"Warning: could not configure logging from alembic.ini ({e}). Continuing without it.")

# الـ metadata المرجعية التي سيقارن بها Alembic عند autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """تشغيل المهاجرات في وضع 'offline' (توليد SQL فقط بدون اتصال فعلي)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """تشغيل المهاجرات في وضع 'online' (اتصال فعلي بقاعدة البيانات)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()