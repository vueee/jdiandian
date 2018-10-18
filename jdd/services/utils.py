# -*- coding: utf-8 -*-
import datetime
import decimal
# replace the script tag in input data
def safe_script(text):
    new_text = text.replace('script','javascript')
    return new_text
    
def request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']

def jsonify_datatime(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

def format_datetime(dt):
    return dt.strftime('%Y-%m-%d @ %H:%M')

def format_date(dt):
    return dt.strftime('%Y-%m-%d')