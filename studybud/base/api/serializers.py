#serializers.py: Turns python objects into JSON object

from rest_framework.serializers import ModelSerializer
from base.models import Room


#Take the Room model and serialize it (turn it into a JSON object)
class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
