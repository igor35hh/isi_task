from rest_framework import serializers
from accounts.models import CustomUser
from dialogs.serializers import ThreadListSerializer
from accounts.auth.backends import AccountAuthBackend


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


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):

        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError(
                'An username is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = AccountAuthBackend().authenticate(
            None, username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this name and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }
