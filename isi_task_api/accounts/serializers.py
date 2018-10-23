from rest_framework import serializers
from accounts.models import CustomUser
from dialogs.serializers import ThreadListSerializer

class CustomUserListSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    num_threads = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['url', 'id', 'username', 'num_threads', 'user_type']

        
        
class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    threads = ThreadListSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 
                  'email', 'user_type', 'threads']
        

