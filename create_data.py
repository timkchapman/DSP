import os
import json
from LarpBook.Models import models
from LarpBook import db, create_app
from datetime import datetime
from LarpBook.extensions import bcrypt

model_order = ['User', 'UserContact', 'Event', 'Album', 'Image']

app = create_app()

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def import_data(model_name):
    file_path = os.path.join('LarpBook', 'Data', 'Dummy_Data', f'{model_name}.json')
    data = read_json_file(file_path)

    for item in data:
        if 'date_joined' in item:
            item['date_joined'] = datetime.strptime(item['date_joined'], '%Y-%m-%d').date()
        if 'birth_date' in item:
            item['birth_date'] = datetime.strptime(item['birth_date'], '%Y-%m-%d').date()
        if 'start_date' in item:
            item['start_date'] = datetime.strptime(item['start_date'], '%Y-%m-%d').date()
        if 'end_date' in item:
            item['end_date'] = datetime.strptime(item['end_date'], '%Y-%m-%d').date()
        if 'password' in item:
            item['password'] = bcrypt.generate_password_hash(item['password']).decode('utf-8')

        model_instance = getattr(models, model_name)(**item)
        db.session.add(model_instance)
    db.session.commit()

with app.app_context():
    for model_name in model_order:
        print(f'Importing {model_name} data')
        import_data(model_name)
        print(f'{model_name} data import complete')
    print('Data import complete')