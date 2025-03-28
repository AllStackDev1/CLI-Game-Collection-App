import importlib
import pkgutil
from db.connection import Database
import db.migrations


class MigrationManager:
    """Manages database migrations."""

    @staticmethod
    def _get_current_version():
        """Get the current schema version from the database."""
        try:
            with Database.execute("SELECT MAX(version) FROM schema_migrations") as cursor:
                result = cursor.fetchone()
                return result[0] if result and result[0] is not None else -1
        except Exception:
            return -1

    @staticmethod
    def _record_migration(version, name):
        """Record a migration in the schema_migrations table."""
        with Database.execute(
            "INSERT INTO schema_migrations (version, name) VALUES (?, ?)",
            (version, name)
        ):
            pass

    @staticmethod
    def _get_migration_modules():
        """Get all migration modules sorted by version."""
        migrations = []
        for _, name, _ in pkgutil.iter_modules(db.migrations.__path__):
            module = importlib.import_module(f"db.migrations.{name}")
            if name.startswith('v') and '_' in name:
                try:
                    version = int(name.split('_')[0][1:])
                    migrations.append((version, name, module))
                except ValueError:
                    print(f"Warning: Migration {name} doesn't follow naming convention vX_description")
        return sorted(migrations, key=lambda x: x[0])

    @classmethod
    def migrate(cls, target_version=None):
        init_module = importlib.import_module("db.migrations.v0_initialize")
        Database.execute_script(init_module.up())

        current_version = cls._get_current_version()
        migrations = cls._get_migration_modules()

        if target_version is None:
            target_version = migrations[-1][0] if migrations else 0

        print(f"Current database version: {current_version}")
        print(f"Target database version: {target_version}")

        if current_version < target_version:
            print("Applying migrations:")
            for version, name, module in migrations:
                if current_version < version <= target_version:
                    print(f"  Applying migration {name}...")
                    if hasattr(module, 'up') and callable(module.up):
                        if not cls._is_version_applied(version):
                            Database.execute_script(module.up())
                            cls._record_migration(version, name)
                    else:
                        print(f"  Warning: Migration {name} has no up() function")
            print("Migrations completed successfully.")

        elif current_version > target_version:
            print("Rolling back migrations:")
            for version, name, module in sorted(migrations, key=lambda x: x[0], reverse=True):
                if target_version < version <= current_version:
                    print(f"  Rolling back migration {name}...")
                    if hasattr(module, 'down') and callable(module.down):
                        Database.execute_script(module.down())
                        with Database.execute("DELETE FROM schema_migrations WHERE version = ?", (version,)):
                            pass
                    else:
                        print(f"  Warning: Migration {name} has no down() function")
            print("Rollback completed successfully.")
        else:
            print("Database is already at the target version.")

    @staticmethod
    def _is_version_applied(version):
        try:
            with Database.execute("SELECT 1 FROM schema_migrations WHERE version = ?", (version,)) as cursor:
                return cursor.fetchone() is not None
        except Exception as e:
            print(f"Error checking if version {version} is applied: {e}")
            raise
