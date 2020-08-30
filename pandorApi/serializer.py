from rest_framework import serializers
from .models import ImportantOccasionModel


class ImportantOccasionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantOccasionModel
        fields = "__all__"