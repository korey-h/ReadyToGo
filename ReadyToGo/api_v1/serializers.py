from registration.models import Categories, Cups, Participants, Races
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


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participants
        fields = '__all__'
        read_only_fields = ['reg_code']

    def validate(self, attrs):
        pre_instance = self.Meta.model(**attrs)
        pre_instance.clean()
        return attrs
