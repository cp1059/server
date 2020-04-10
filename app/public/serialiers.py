


from rest_framework import serializers
from app.public.models import Banner,Video


class BannerModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = '__all__'

class VideoModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = '__all__'