import os
import json
from datetime import datetime, date
from LarpBook import db
from LarpBook.Models import models
from LarpBook import create_app
import inspect

app = create_app()

def restore_database():
    while True:
        backup_date = input("Enter the date of the backup you want to restore (YYYY-MM-DD): ")
        backup_directory_name = f"Backup_{backup_date}"
        backup_directory_path = os.path.join(os.getcwd(),'LarpBook', 'Backup', backup_directory_name)

        if os.path.exists(backup_directory_path):
            break
        else:
            print(f"No backup found for date: {backup_date}")

    try:
        # Get all classes from the models module
        model_classes = inspect.getmembers(models, inspect.isclass)

        for _, model_class in model_classes:
            model_name = model_class.__name__
            json_file_path = os.path.join(backup_directory_path, f"{model_name}.json")

            if os.path.exists(json_file_path):
                print(f"Found backup file for {model_name}. Restoring data...")
                with open(json_file_path, 'r', encoding='utf-8') as json_file:
                    serialized_data = json.load(json_file)
                    # Delete existing records in the table
                    db.session.query(model_class).delete()
                    # Create or update records from the serialized data
                    for data in serialized_data:
                        # Convert date strings back to datetime.date objects
                        for key, value in data.items():
                            if isinstance(value, str) and value:
                                try:
                                    data[key] = datetime.fromisoformat(value).date()
                                except ValueError:
                                    pass  # Ignore if value is not a valid date string
                        # Create new database record
                        instance = model_class(**data)
                        db.session.add(instance)
                    db.session.commit()
                    print(f"Data for {model_name} restored successfully.")
            else:
                print(f"No backup file found for {model_name}. Skipping...")

        # Include relational tables that aren't classes
        relational_tables = [
            (models.friendslist, 'friendslist'),
            (models.blocklist, 'blocklist'),
            (models.userevents, 'userevents'),
            (models.eventtags, 'eventtags'),
            (models.usertags, 'usertags'),
            (models.albumimage, 'albumimage')
        ]

        for table, table_name in relational_tables:
            json_file_path = os.path.join(backup_directory_path, f"{table_name}.json")

            if os.path.exists(json_file_path):
                print(f"Found backup file for {table_name}. Restoring data...")
                with open(json_file_path, 'r', encoding='utf-8') as json_file:
                    serialized_data = json.load(json_file)
                    # Delete existing records in the table
                    db.session.query(table).delete()
                    # Create or update records from the serialized data
                    for data in serialized_data:
                        # Convert date strings back to datetime.date objects
                        for key, value in data.items():
                            if isinstance(value, str) and value:
                                try:
                                    data[key] = datetime.fromisoformat(value).date()
                                except ValueError:
                                    pass  # Ignore if value is not a valid date string
                        # Create new database record
                        db.session.execute(table.insert().values(**data))
                    db.session.commit()
                    print(f"Data for {table_name} restored successfully.")
            else:
                print(f"No backup file found for {table_name}. Skipping...")
                
    except Exception as e:
        print(f"Error restoring database: {e}")

if __name__ == '__main__':
    with app.app_context():
        restore_database()
