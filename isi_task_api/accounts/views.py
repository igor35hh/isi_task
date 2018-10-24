from rest_framework import viewsets, mixins, status
from accounts.serializers import CustomUserListSerializer
from accounts.serializers import CustomUserSerializer
from accounts.models import CustomUser
from rest_framework.response import Response
from django.db.models import Count
from rest_framework.permissions import AllowAny
from accounts.renderers import UserJSONRenderer
from accounts.serializers import LoginSerializer
from rest_framework.views import APIView


class CustomUserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                        mixins.RetrieveModelMixin):

    def list(self, request, *args, **kwargs):
        queryset = CustomUser.objects.annotate(
            num_threads=Count('threads')).all()
        serializer = CustomUserListSerializer(
            queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
