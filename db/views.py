from django.http import HttpResponse
from db.settings import CONFIRMATION_TOKEN
from rest_framework.decorators import api_view

from .api import select_method, send_message
from vkbot.models import Users


@api_view(['GET', 'POST'])
def main(request):
    if request.method == "GET":
        return HttpResponse({'<h1>Привет</h1>'})
    elif request.method == 'POST':
        data = request.data
        print(data)
        if data["type"] == "confirmation":
            return HttpResponse(CONFIRMATION_TOKEN)
        elif data["type"] == "message_new":
            user_id = data["object"]["message"]["from_id"]
            if user_id in [i.vk_id for i in Users.objects.all()]:
                select_method(data, user_id)
            else:
                send_message(user_id, "Вы не зареганы")
            return HttpResponse("ok")
        else:
            return HttpResponse("ok")
    else:
        print("ploxo")
        return HttpResponse({"error": "bad request"})
