"""
Views for the graphic APIs
"""
from rest_framework import (
    viewsets,
    mixins,
)

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from datetime import datetime, timedelta
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect


from core.models import (
    Graphic,
)
from rest_framework.decorators import action
from graphic import serializers
from easy_thumbnails.files import get_thumbnailer


class GraphicViewSet(viewsets.ModelViewSet):
    """View for manage graphic APIs."""

    serializer_class = serializers.GraphicSerializer
    queryset = Graphic.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
