# Generated by Django 3.1.11 on 2021-05-26 11:14

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('home', '0004_auto_20210409_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionRecommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.section')),
                ('source', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommended_sections', to='home.article')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='home.article')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_articletag_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArticleRecommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.article')),
                ('source', modelcluster.fields.ParentalKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='recommended_articles', to='home.article')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='home.ArticleTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]