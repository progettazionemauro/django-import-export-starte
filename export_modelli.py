'''
django standalone script to take backup of database in the form of csvs for each model.
- Place it in the same directory as manage.py file
- Rename PROJECT_NAME to your project's name
- Questa è un'utility molto potente in quanto permette di scaricare ed esportare tutti i modelli
 - all'interno del progetto. Fatto ciò tali modelli possono essere nuoavmente importati in excel o google sheets
 - per essere ulteriormente elaborati - Mauro febbraio 2023
 - vedere qui: https://dev.to/rugved/django-standalone-script-to-take-database-backup-2287
 - Per una spiegazione molto ben fatta sulla libreria import export vedere qui: https://python.plainenglish.io/django-standalone-script-to-take-database-backup-5a12f51813e0
'''

import os

PROJECT_NAME = 'DemoProject'

def main():
    from django.apps import apps
    import csv

    model_list = apps.get_models()
    model_name_list = [x.__name__ for x in model_list]
    
    for model in model_list:
        all_fields = model._meta.get_fields()
        columns = [x.name for x in all_fields]
        
        if not os.path.exists('csvs'):
            os.makedirs('csvs')

        with open(f'csvs/{model.__name__}.csv', mode='w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            # Writing column names
            writer.writerow(columns)

            objects = model.objects.all()
            
            for obj in objects:
                row = [str(getattr(obj, field_name,"NA")) for field_name in columns]
                writer.writerow(row)
    
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % PROJECT_NAME)
    import django
    django.setup()
    main()