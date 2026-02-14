from django.shortcuts import render
from django.http import JsonResponse
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from collections import Counter
from dateutil import parser

load_dotenv()

def get_db_data(request):
    mongo_str = os.getenv('MONGODB_CONNECTION_STRING')
    client = MongoClient(mongo_str)
    db = client['support_db']
    collection = db['tickets']

    search_query = request.GET.get('search', '')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    query = {}
    if search_query:
        query['$or'] = [
            {'description': {'$regex': search_query, '$options': 'i'}},
            {'name': {'$regex': search_query, '$options': 'i'}},
            {'ticket_id': {'$regex': search_query, '$options': 'i'}},
            {'priority': {'$regex': search_query, '$options': 'i'}},
            {'status': {'$regex': search_query, '$options': 'i'}}
        ]

    all_found = list(collection.find(query).sort('created_at', -1))
    
    filtered_data = []
    if start_date_str and end_date_str:
        try:
            start_dt = parser.parse(start_date_str).date()
            end_dt = parser.parse(end_date_str).date()
            for t in all_found:
                raw_date = t.get('created_at')
                if raw_date:
                    ticket_dt = parser.parse(str(raw_date)).date()
                    if start_dt <= ticket_dt <= end_dt:
                        filtered_data.append(t)
        except:
            filtered_data = all_found
    else:
        filtered_data = all_found

    statuses = [t.get('status', 'Невідомо') for t in filtered_data]
    status_counts = Counter(statuses)

    priorities = [t.get('priority', 'Не вказано') for t in filtered_data]
    priority_counts = Counter(priorities)

    workers = [t.get('accepted_by') for t in filtered_data if t.get('accepted_by')]
    worker_counts = Counter(workers).most_common(10)

    dates = [str(t.get('created_at'))[:7] for t in filtered_data if t.get('created_at')]
    date_counts = Counter(dates)
    sorted_months = sorted(date_counts.keys())

    tickets_list = []
    for t in filtered_data[:15]:
        tickets_list.append({
            'date': str(t.get('created_at', ''))[11:16],
            'id': t.get('ticket_id', '-'),
            'name': t.get('name', 'Гість'),
            'desc': t.get('description', ''),
            'priority': t.get('priority', 'Середній'),
            'status': t.get('status', 'Нова')
        })

    return {
        'total': len(filtered_data),
        'status_labels': list(status_counts.keys()),
        'status_data': list(status_counts.values()),
        'priority_labels': list(priority_counts.keys()),
        'priority_data': list(priority_counts.values()),
        'worker_labels': [item[0] for item in worker_counts],
        'worker_data': [item[1] for item in worker_counts],
        'month_labels': sorted_months,
        'month_data': [date_counts[m] for m in sorted_months],
        'tickets_list': tickets_list,
        'search_query': search_query,
        'selected_start': start_date_str,
        'selected_end': end_date_str,
    }

def dashboard_home(request):
    data = get_db_data(request)
    return render(request, 'dashboard/index.html', data)

def api_data(request):
    data = get_db_data(request)
    return JsonResponse(data)