import os
import json
from datetime import datetime, date
from LarpBook import db
from LarpBook.Models import models
from LarpBook import create_app
import inspect
from sqlalchemy import select

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

    # Include data from relational tables
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
        print(f"Creating backup for {table_name}...")

        try:
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                # Query all rows from the table
                query = db.session.query(table).all()
                
                # Convert each row to a dictionary
                serialized_data = []
                for row in query:
                    row_dict = {}
                    for column in table.columns:
                        row_dict[column.name] = getattr(row, column.name)
                    serialized_data.append(row_dict)
                    
                # Convert date objects to string representation
                for data in serialized_data:
                    for key, value in data.items():
                        if isinstance(value, date):
                            data[key] = value.isoformat()  # Convert date to ISO string
                
                # Write the serialized data to the JSON file
                json_file.write(json.dumps(serialized_data, indent=4))
                
                print(f"Backup for {table_name} created successfully.")
        except Exception as e:
            print(f"Error creating backup for {table_name}: {e}")

    print(f"Database backup created at {backup_directory_path}")

if __name__ == '__main__':
    with app.app_context():
        backup_database()
