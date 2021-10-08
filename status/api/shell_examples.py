import json
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from six import BytesIO

from status.api.serializers import CustomSerializer, StatusSerializers
from status.models import Status

'''
Serialize a single object
'''
obj = Status.objects.first()
serializer = StatusSerializers(obj)
serializer.data
json_data = JSONRenderer().render(serializer.data)
print(json_data)

stream = BytesIO(json_data)
data = JSONParser().parse(stream)
print(data)

'''
Serialize a queryset
'''
qs = Status.objects.all()
serializer2 = StatusSerializers(qs, many=True)
serializer2.data
json_data2 = JSONRenderer(serializer2.data)
print(json_data2)

stream2 = BytesIO(json_data2)
data2 = JSONParser().parse(stream2)
print(data2)

'''
Create obj
'''
data = {'user':1}
serializer = StatusSerializers(data=data)
serializer.is_valid()
serializer.save()

'''
Update obj
'''
obj = Status.objects.first()
data = {'content':'some new content', 'user':1}
update_serializer = StatusSerializers(obj, data=data)
update_serializer.is_valid()
update_serializer.save()

'''
Delete obj
'''
data = {'user':1, 'content': "please delete me", 'image':''}
create_obj_serializer = StatusSerializers(data=data)
create_obj_serializer.is_valid()
create_obj = create_obj_serializer.save()
print(create_obj)

# data = {'id':4}
obj = Status.objects.last()
get_data_serializer = StatusSerializers(obj)
# update_serializer.is_valid()
# update_serializer.save()
print(get_data_serializer)




from rest_framework import serializers
class CustomSerializer(serializers.Serializer):
    content    = serializers.CharField()
    email      = serializers.EmailField()


data = {'email':'hello@teamcfe.com', 'content':'please delete me'}
create_obj_serializer = CustomSerializer(data=data)
if create_obj_serializer.is_valid():
    data = create_obj_serializer.data
    print(data)
