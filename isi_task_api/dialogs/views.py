from rest_framework import viewsets
from rest_framework import mixins
from dialogs.serializers import ThreadSerializer,  MessageSerializer
from dialogs.serializers import ThreadListSerializer
from dialogs.models import Thread, Message
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from accounts.models import USERTYPE_ADMIN
from rest_framework.response import Response
from django.db.models import Count


class ThreadViewSet(viewsets.ModelViewSet):

    @method_decorator(user_passes_test(
        lambda u: u.user_type == USERTYPE_ADMIN))
    def create(self, request, *args, **kwargs):
        return mixins.CreateModelMixin.create(self, request, *args, **kwargs)

    @method_decorator(user_passes_test(
        lambda u: u.user_type == USERTYPE_ADMIN))
    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        participants = serializer.validated_data.get('participants')
        members = len(participants)
        if members == 1:
            if participants[0].user_type == USERTYPE_ADMIN:
                return self.destroy(request, *args, **kwargs)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @method_decorator(user_passes_test(
        lambda u: u.user_type == USERTYPE_ADMIN))
    def destroy(self, request, *args, **kwargs):
        return viewsets.ModelViewSet.destroy(self, request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = Thread.objects.annotate(
            num_messages=Count('messages')).all()
        serializer = ThreadListSerializer(
            queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


class MessageViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
