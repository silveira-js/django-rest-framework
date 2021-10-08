import json

from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import View

from cfeapi.mixins import JsonResponseMixin
from .models import Update

# Create your views here.
#  python manage.py dumpdata updates --format json --indent 4

# def detail_view(request):
#     return render() # return JSON data --> JS Object Notation 

def json_example_view(request):
    '''
    URI -- for a REST API
    GET -- Retrieve
    '''
    data = {
        "count": 1000,
        "content": "Some new content"
    }
    json_data = json.dumps(data)
    # return JsonResponse(data)
    return HttpResponse(json_data, content_type='application/json') 

class JsonCBV(View):
    def get(self, request, *args, **kwargs):
        data = {
            "count": 1000,
            "content": "Some new content"
        }
        return JsonResponse(data)


class JsonCBV2(JsonResponseMixin, View):
    def get(self, request, *args, **kwargs):
        data = {
            "count": 1000,
            "content": "Some new content"
        }
        return self.render_to_json_response(data)

class SerializedDetailView(View):
    def get(self, request, *args, **kwargs):
        obj = Update.objects.get(id=4) 
        json_data = obj.serialize()
        return HttpResponse(json_data, content_type='application/json')


class SerializedListView(View):
    def get(self, request, *args, **kwargs):
        qs = Update.objects.all()
        json_data = Update.objects.all().serialize()
        return HttpResponse(json_data, content_type='application/json')














class SerializedDetailView(View):
    def get(self, request, *args, **kwargs):
        obj = Update.objects.get(id=4) 
        # data = serialize("json", [obj,], fields=('user', 'content'))
        # print(data)
        # json_data = data
        json_data = obj.serialize()
        # data = {
        #     "user": obj.user.username,
        #     "content": obj.content
        # } 
        return HttpResponse(json_data, content_type='application/json')


class SerializedListView(View):
    def get(self, request, *args, **kwargs):
        qs = Update.objects.all()
        # data = serialize("json", qs, fields=('user', 'content'))
        # print(data)
        # json_data = data
        json_data = Update.objects.all().serialize()
        # data = {
        #     "user": obj.user.username,
        #     "content": obj.content
        # } 
        return HttpResponse(json_data, content_type='application/json')