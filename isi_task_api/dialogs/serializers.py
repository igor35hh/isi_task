from rest_framework import serializers
from dialogs.models import Thread, Message
from django.utils.translation import gettext_lazy as _
from accounts.models import USERTYPE_ADMIN, CustomUser


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()
    updated = serializers.ReadOnlyField()

    class Meta:
        model = Message
        fields = '__all__'
        extra_kwargs = {'text': {'required': True}, 'sender':
                        {'required': True}, 'thread': {'required': True}}


class ThreadSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()
    updated = serializers.ReadOnlyField()
    participants = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), many=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        depth = 1
        fields = '__all__'
        extra_kwargs = {'participants': {'required': True}}

    def validate_participants(self, value):
        admins = sum(map(lambda p: p.user_type == USERTYPE_ADMIN, value))
        if admins > 1:
            raise serializers.ValidationError(
                _('The field participants contains more than one admin.'))
        return value


class ThreadListSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()
    updated = serializers.ReadOnlyField()
    num_messages = serializers.IntegerField(read_only=True)

    class Meta:
        model = Thread
        fields = ('url', 'id', 'num_messages', 'created', 'updated')
