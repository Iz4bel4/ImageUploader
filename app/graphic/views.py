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

    def try_fill_with_thumbnail_links(self, tier, graphic, data):
        """Thumbnail links"""
        if tier.thumbnail_sizes is None:
            return
        
        thumbnail_heights = tier.thumbnail_sizes["heights"]
        if thumbnail_heights is None or not thumbnail_heights:
            return
        
        if graphic.image is None or not graphic.image:
            for height in thumbnail_heights:
                data['thumbnail_' + str(height)] = None
            return
        
        ratio = graphic.image.height / graphic.image.width
        for height in thumbnail_heights:
            options = {'size': (height, int(float(height) * ratio)), 'crop': True}
            thumb_url = get_thumbnailer(graphic.image).get_thumbnail(options).url
            data['thumbnail_' + str(height)] = 'http://127.0.0.1:8000' + thumb_url
    def try_adjust_original_link_presence(self, tier, data):
        """Add/remove/update original image link"""
    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve graphics for authenticated user."""
        queryset = self.queryset
        return queryset.filter(user=self.request.user).order_by("-id").distinct()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        return self.serializer_class
    
    def create(self, request):
        """New graphic creation with proper links managament"""     

        # Basic create procedure
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        modifiedData = serializer.data

        graphic = Graphic.objects.get(id=modifiedData["id"])
        tier = graphic.user.tier
        self.try_fill_with_links(tier, graphic, modifiedData)
            
        # All links should be packed and unpacked with protecting hash
        return Response(modifiedData, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """Create a new graphic."""
        serializer.save(user=self.request.user)
class BaseGraphicAttrViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Base viewset for graphic attributes."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        assigned_only = bool(int(self.request.query_params.get("assigned_only", 0)))
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(graphic__isnull=False)

        return queryset.filter(user=self.request.user).order_by("-name").distinct()