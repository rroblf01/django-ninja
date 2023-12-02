from cooking.models import History
import json

def create_history(request, response):
    body = getattr(request, 'body', '') or '{}'
    History.objects.create(user=request.auth, endpoint=request.path,
                           body=json.loads(body),
                           response={'status_code': response[0], 'response': f'{response[1]}'})
