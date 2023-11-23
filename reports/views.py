from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view


@api_view(['POST'])
def submit_report(request):
    print(request.headers)
    print(request.data)
    return HttpResponse(500)
