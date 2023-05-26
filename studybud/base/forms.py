from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

#Model form
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' #Gets all editable fields from Room model
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
