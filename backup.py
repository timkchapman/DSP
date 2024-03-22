import os
import json
from datetime import datetime, date
from LarpBook import db
from LarpBook.Models import models
from LarpBook import create_app
import inspect

app = create_app()

def backup_database():
    backup_directory_name = f"Backup_{datetime.now().strftime('%Y-%m-%d')}"
    backup_directory_path = os.path.join(os.getcwd(),'LarpBook', 'Backup', backup_directory_name)

    try:
        os.makedirs(backup_directory_path, exist_ok=True)
    except OSError as e:
        print(f"Error creating backup directory: {e}")
        return
    
    # Get all classes from the models module
    model_classes = inspect.getmembers(models, inspect.isclass)

    for _, model_class in model_classes:
        model_name = model_class.__name__
        json_file_path = os.path.join(backup_directory_path, f"{model_name}.json")
        print(f"Creating backup for {model_name}...")

        try:
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                query_set = db.session.query(model_class).all()
                serialized_data = [row.serialize() for row in query_set]
                # Convert date objects to string representation
                for data in serialized_data:
                    for key, value in data.items():
                        if isinstance(value, date):
                            data[key] = value.isoformat()  # Convert date to ISO string
                json_file.write(json.dumps(serialized_data, indent=4))
                print(f"Backup for {model_name} created successfully.")
        except Exception as e:
            print(f"Error creating backup for {model_name}: {e}")

    print(f"Database backup created at {backup_directory_path}")

if __name__ == '__main__':
    with app.app_context():
        backup_database()
