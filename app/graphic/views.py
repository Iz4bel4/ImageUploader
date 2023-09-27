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

    def try_delete_original_link(self, data):
        if 'image' in data:
            del data['image']

    def try_adjust_original_link_presence(self, tier, data):
        """Add/remove/update original image link"""
        if 'image' not in data:
            return
        
        image_path = data['image']
        if not tier.returns_original_image_link:
            self.try_delete_original_link(data)
        elif image_path is not None:
            if 'http://127.0.0.1:8000' not in image_path:
                data['image'] = 'http://127.0.0.1:8000' + image_path

    def change_link_to_expirational_link(self, tier, graphic, data, seconds_to_expire):
        """Expirational links"""
        if tier.returns_original_image_expiring_link:
            signer = TimestampSigner()

            # Set the expiration time (e.g., 1 day from now)
            expiration_time = datetime.now() + timedelta(seconds=seconds_to_expire)

            # Sign the URL with the expiration time
            if graphic.image is None or not graphic.image:
                return
            
            link = str(graphic.image)
            expirational_link = signer.sign_object(
                f"{link}:{expiration_time.timestamp()}"
            )  
            data['image'] = 'http://127.0.0.1:8000/api/graphic/expirational-link/' + expirational_link

    def try_fill_with_links(self, tier, graphic, data):
        if tier is not None:
            # Thumbnail links
            self.try_fill_with_thumbnail_links(tier, graphic, data)
            # Original link
            self.try_adjust_original_link_presence(tier, data)
        else:
            self.try_delete_original_link(data)

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        if serializer.data is not None:
            for item in serializer.data:
                graphic = Graphic.objects.get(id=item["id"])
                tier = graphic.user.tier
                self.try_fill_with_links(tier, graphic, item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            graphic = Graphic.objects.get(pk=pk)
        except Graphic.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(graphic)
        modifiedData = serializer.data
        tier = graphic.user.tier
        self.try_fill_with_links(tier, graphic, modifiedData)
        return Response(modifiedData, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=True, url_path="get-expirational-link/(?P<seconds_to_expire>[0-9]+)")
    def get_image_expirational_link(self, request, pk=None, seconds_to_expire=None):
        """Return image expirational link with a certain time"""
        try:
            seconds_to_expire_int = int(seconds_to_expire)
        except ValueError:
            return Response({"detail": "Invalid parameter. It must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
        
        if (300 > seconds_to_expire_int or seconds_to_expire_int > 30000):
            return Response({"detail": "Invalid value. Value must be between 300 and 30000."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Expirational link
        graphic = Graphic.objects.get(id=pk)
        tier = graphic.user.tier
        if not tier.returns_original_image_expiring_link:
            return Response({"detail": "User account tier is not authorized to get the expiring link."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(graphic)
        modifiedData = serializer.data
        self.change_link_to_expirational_link(tier, graphic, modifiedData, seconds_to_expire_int)

        return Response(modifiedData, status=status.HTTP_200_OK)

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


class ExpirationalLinkView(View):
    def get(self, request, expirational_link):
        try:
            signer = TimestampSigner()
            original_url, expiration_timestamp = signer.unsign_object(expirational_link).split(':')
            original_url = "http://127.0.0.1:8000/static/media/" + original_url

            # Check if the link is still valid
            expiration_time = datetime.fromtimestamp(float(expiration_timestamp))
            if datetime.now() <= expiration_time:
                # Redirect the user to the original image URL
                return HttpResponseRedirect(original_url)
            else:
                return HttpResponse("Link has expired", status=403)
        except BadSignature:
            return HttpResponseBadRequest("Invalid link")


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