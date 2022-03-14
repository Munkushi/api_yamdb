from rest_framework import serializers
from reviews.models import User, Comments, Review

class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comments
        fields = '__all__'