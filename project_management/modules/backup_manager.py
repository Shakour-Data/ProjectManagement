import os
import shutil
import datetime
from pathlib import Path

class BackupManager:
    def __init__(self,
                 source_dir: str = "project_inputs/PM_JSON/user_inputs",
                 backup_base_dir: str = "project_management/PM_Backups/user_inputs_backup"):
        self.source_dir = Path(source_dir)
        self.backup_base_dir = Path(backup_base_dir)
        self.backup_base_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.backup_base_dir / f"backup_{timestamp}"
        try:
            shutil.copytree(self.source_dir, backup_dir)
            print(f"Backup created at: {backup_dir}")
            return backup_dir
        except Exception as e:
            print(f"Failed to create backup: {e}")
            return None

    def list_backups(self):
        backups = sorted(self.backup_base_dir.glob("backup_*"), reverse=True)
        return backups

    def restore_backup(self, backup_dir: str):
        backup_path = Path(backup_dir)
        if not backup_path.exists():
            print(f"Backup directory {backup_dir} does not exist.")
            return False
        try:
            # Clear current source_dir contents
            if self.source_dir.exists():
                for item in self.source_dir.iterdir():
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
            # Copy backup contents to source_dir
            shutil.copytree(backup_path, self.source_dir, dirs_exist_ok=True)
            print(f"Restored backup from {backup_dir} to {self.source_dir}")
            return True
        except Exception as e:
            print(f"Failed to restore backup: {e}")
            return False

if __name__ == "__main__":
    bm = BackupManager()
    print("Creating backup...")
    bm.create_backup()
