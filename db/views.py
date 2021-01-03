from django.http import HttpResponse
from db.settings import CONFIRMATION_TOKEN
from rest_framework.decorators import api_view

from .api import select_method
from vkbot.models import Users


@api_view(['GET', 'POST'])
def main(request):
    if request.method == "GET":
        return HttpResponse({'<h1>Привет</h1>'})
    elif request.method == 'POST':
        data = request.data
        if data["type"] == "confirmation":
            return HttpResponse(CONFIRMATION_TOKEN)
        if data["type"] == "message_new":
            user_id = data["object"]["user_id"]
            # obj return user_id, created bool status
            select_method(data, user_id)
            return HttpResponse("ok")
        else:
            return HttpResponse("ok")
    else:
        print("ploxo")
        return HttpResponse({"error": "bad request"})
