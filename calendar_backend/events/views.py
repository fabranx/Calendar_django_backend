from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status

from .models import Event
from .serializers import EventSerializer
from .permission import IsAuthorListView, IsAuthorDetailView
from rest_framework import permissions
from rest_framework.filters import OrderingFilter
from django.shortcuts import get_object_or_404

class EventPost(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventSerializer

    def post(self, request, *args, **kwargs):
        isList = isinstance(request.data, list)
        if isList:
            serializer = self.get_serializer(data=request.data, many=True)
            if serializer.is_valid(raise_exception=True):
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """CONTROLLA SE L'USER LOGGATO SIA UGUALE A L'AUTORE DELL' EVENTO"""
        isList = isinstance(self.request.data, list)
        same_author_user = False
        if isList:
            # controlla se tutti gli author nell' array self.request.data sono uguali a request.user.id
            same_author_user = all(int(item['author']) == self.request.user.id for item in self.request.data)
        else:
            same_author_user = self.request.user.id == int(self.request.data['author'])

        if same_author_user:
            serializer.save()
        else:
            raise PermissionDenied(detail="Request Failed - Different User and Author")

            # if self.request.user.id == int(self.request.data['author']):
            #     serializer.save()
            # else:
            #     raise PermissionDenied(detail="Request Failed - Different User and Author")


class EventListView(generics.ListAPIView):
    permission_classes = [IsAuthorListView, permissions.IsAuthenticated]
    serializer_class = EventSerializer
    filter_backends = [OrderingFilter]
    ordering = ['-created_at']  # dal più nuovo

    def get_user(self):  # metodo personale
        user = get_object_or_404(get_user_model(), username=self.kwargs['username'])
        return user

    def get_queryset(self):
        return Event.objects.filter(author=self.get_user())



class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorDetailView, permissions.IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_update(self, serializer):
        """CONTROLLA SE L'USER LOGGATO SIA UGUALE A L'AUTORE DELL' EVENTO"""
        if self.request.user.id == int(self.request.data['author']):
            serializer.save()
        else:
            raise PermissionDenied(detail="Request Failed - Different User and Author")
