from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(['GET'])
def logged_in(request):
    return JsonResponse({'authenticated': request.user.is_authenticated})
