from rest_framework import serializers

from home import models


class ArticleSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()

    class Meta:
        model = models.Article
        fields = ['id', 'language', 'title', 'body', 'live']
        # fields = "__all__"

    def get_language(self, obj):
        return obj.locale.get_display_name()

    def update(self, instance, validated_data):
        data = super().update(instance, validated_data)
        instance.live = False
        instance.save()
        return data
