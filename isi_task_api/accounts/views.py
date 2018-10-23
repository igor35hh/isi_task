from rest_framework import viewsets, mixins, generics
from accounts.serializers import CustomUserListSerializer 
from accounts.serializers import CustomUserSerializer
from accounts.models import CustomUser
from rest_framework.response import Response
from django.db.models import Count

class CustomUserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, 
                        mixins.RetrieveModelMixin):
    
    def list(self, request, *args, **kwargs):
        queryset = CustomUser.objects.annotate(num_threads=Count('threads')).all()
        serializer = CustomUserListSerializer(queryset, 
                                    context={'request': request}, many=True)
        return Response(serializer.data)
    
    
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    
    
