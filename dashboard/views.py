from django.http import HttpResponse
from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()

def test_db(request):
    try:
        mongo_str = os.getenv('MONGODB_CONNECTION_STRING')
        
        if not mongo_str:
            return HttpResponse("❌ ПОМИЛКА: Не знайдено змінну MONGODB_CONNECTION_STRING у файлі .env")

        client = MongoClient(mongo_str)

        db_name = 'ServiceDeskDB' 
        db = client[db_name]
        
        collection = db['mech_tickets']
        count = collection.count_documents({})

        return HttpResponse(f"""
            <h1 style='color:green'>✅ Успішне підключення!</h1>
            <p>База даних: <b>{db_name}</b></p>
            <p>Знайдено заявок у 'mech_tickets': <b>{count}</b></p>
        """)

    except Exception as e:
        return HttpResponse(f"<h1 style='color:red'>❌ Помилка підключення:</h1><p>{e}</p>")