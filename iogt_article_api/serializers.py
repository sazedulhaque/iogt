from rest_framework import serializers

from home import models


class ArticleSerializer(serializers.ModelSerializer):
    language = serializers.CharField(source='locale.get_display_name', read_only=True)

    class Meta:
        model = models.Article
        fields = ['id', 'language', 'title', 'body', 'live']

    def update(self, instance, validated_data):
        data = super().update(instance, validated_data)
        instance.live = False
        instance.save()
        return data
