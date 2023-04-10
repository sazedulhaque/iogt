from rest_framework import serializers

from home import models


class ArticleSerializer(serializers.ModelSerializer):
    language = serializers.CharField(source='locale.get_display_name', read_only=True)
    owners_email = serializers.CharField(source='owner.email', read_only=True)

    class Meta:
        model = models.Article
        fields = [
            'id',
            'language',
            'owners_email',
            'owner_id',
            'title',
            'body',
            'latest_revision_created_at',
            'first_published_at',
            'last_published_at',
            'live'
        ]

    def update(self, instance, validated_data):
        data = super().update(instance, validated_data)
        instance.live = False
        instance.save()
        return data
