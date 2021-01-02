from django.http import HttpResponse




def main(request):
    if request.method == "GET":
        return HttpResponse({"message": "hello world!"})
    elif request.method == 'POST':
        data = request.data
        print(data)
        return HttpResponse('8294de96')