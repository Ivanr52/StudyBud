from django.forms import ModelForm
from .models import Room

#Model form
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' #Gets all editable fields from Room model
