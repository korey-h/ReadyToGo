from registration.models import Categories, Cups, Races
from rest_framework import serializers


class CupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cups
        fields = ['id', 'name']    


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name'] 


class RacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Races
        fields = ['id', 'name']


class RaceDetailSerializer(serializers.ModelSerializer):
    cup = CupsSerializer()
    race_categories = CategoriesSerializer(many=True)

    class Meta:
        model = Races
        fields = ['id', 'name', 'date', 'cup', 'town', 'description',
                  'is_active', 'race_categories']
