import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Genre


@csrf_exempt  # decorador de segurança
def genre_create_list_view(request):
    if request.method == "GET":
        genres = Genre.objects.all()
        data = [{"id": genre.id, "name": genre.name} for genre in genres]
        return JsonResponse(data, safe=False)
    elif request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        genre_exists = Genre.objects.all().filter(name__icontains=data["name"])
        print(genre_exists)

        if genre_exists:
            return JsonResponse({"message": "Gênero já está cadastrado"}, status=200)
        else:
            new_genre = Genre(name=data["name"])
            new_genre.save()
            return JsonResponse(
                {"id": new_genre.id, "name": new_genre.name}, status=201
            )


@csrf_exempt
def genre_detail_view(request, pk):
    genre = get_object_or_404(Genre, pk=pk)

    if request.method == "GET":
        data = {"id": genre.id, "name": genre.name}
        return JsonResponse(data, status=200)
    elif request.method == "PUT":
        data = json.loads(request.body.decode("utf-8"))
        genre.name = data["name"]
        genre.save()
        return JsonResponse({"id": genre.id, "name": genre.name}, status=200)
    elif request.method == "DELETE":
        genre.delete()
        return JsonResponse({"message": "Gênero excluído com sucesso."}, status=204)
