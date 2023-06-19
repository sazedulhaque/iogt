from django.db import transaction
from rest_framework import serializers
from wagtail_localize.models import TranslationSource, Translation

from home import models


class ArticleSerializer(serializers.ModelSerializer):
    language = serializers.CharField(source='locale.get_display_name', read_only=True)
    language_code = serializers.CharField(source='locale.language_code', read_only=True)
    owners_email = serializers.CharField(source='owner.email', read_only=True)

    class Meta:
        model = models.Article
        read_only_fields = ('slug', 'first_published_at', 'url_path', 'language_code')
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
            'slug',
            'url_path',
            'language_code',
            'live'
        ]

    @transaction.atomic
    def update(self, instance, validated_data):
        data = super().update(instance, validated_data)
        # ----------------------------------------------------
        # unpublished to verify the Article by Moderator
        instance.live = False
        # ----------------------------------------------------
        # In this section we reduce the manual work of
        # stop sync and also keep the option to undo it
        instance.alias_of_id = None
        instance.save()
        translation_obj = TranslationSource.objects.filter(object_id=instance.translation_key)
        if translation_obj.exists():
            Translation.objects.get_or_create(
                source=translation_obj.last(),
                target_locale=instance.locale,
                enabled=False
            )
        return data
