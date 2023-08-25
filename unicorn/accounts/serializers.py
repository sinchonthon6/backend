from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            oauth_id = validated_data['ouath_id']
        )
        return user