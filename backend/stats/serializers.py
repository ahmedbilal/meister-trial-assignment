from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from stats.models import Country, City, Sale


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        email, password = data["email"], data["password"]
        user = authenticate(self.context.get('request'), username=email, password=password)
        print(user)
        if not user:
            raise serializers.ValidationError("Unable to log in with provided credentials.")
        data['user'] = user
        return data

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"


class SalesSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField()

    class Meta:
        model = Sale
        exclude = ["user"]
        # fields = "__all__"
