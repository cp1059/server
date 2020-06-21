


from rest_framework import serializers
from app.public.models import Banner,Video,Holiday


class HolidayModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Holiday
        fields = '__all__'

class BannerModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = '__all__'

class VideoModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = '__all__'