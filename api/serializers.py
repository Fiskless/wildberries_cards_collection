import datetime

from django.utils.timezone import utc
from rest_framework import serializers
from cards.models import TrackParameter, Product
from cards.tasks import update_product_data


class TrackParameterSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrackParameter
        fields = ['article', 'start_at', 'end_at', 'time_interval']

    def create(self, validated_data):
        track_parameter = self.validated_data
        if track_parameter['end_at'] < datetime.datetime.utcnow().replace(tzinfo=utc):
            raise serializers.ValidationError({'error': "End time should be more current time"})
        if track_parameter['start_at'] >= track_parameter['end_at']:
            raise serializers.ValidationError({'error': 'Start time should be less end time'})
        if track_parameter['start_at'] < datetime.datetime.utcnow().replace(tzinfo=utc):
            raise serializers.ValidationError({'error': 'Start time should be more or equal current time'})
        new_track = TrackParameter.objects.create(**validated_data)
        new_track.user.add(self.context['request'].user)
        res = update_product_data.delay(track_parameter['article'])
        return new_track


class TrackParameterListSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrackParameter
        fields = ['article', 'start_at', 'end_at', 'time_interval']


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['article', 'name', 'price_without_discount', 'price_with_discount', 'brand', 'seller', 'time']