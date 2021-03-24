# Generated by Django 3.1.7 on 2021-03-24 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OutFeed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='The title of the feed.', max_length=1024)),
                ('slug', models.SlugField(blank=True, help_text='The string to use to identify this feed in URLs. Leave blank to auto-generate  from the title.', max_length=100, unique=True)),
                ('enabled', models.BooleanField(help_text='Determines whether or not this item is enabled.', verbose_name='Enabled?')),
                ('description', models.TextField(help_text='The description of the feed.')),
                ('updated', models.DateTimeField(help_text='The date/time the content of the feed last changed.')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='InFeed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the feed.', max_length=1024)),
                ('enabled', models.BooleanField(help_text='Determines whether or not this item is enabled.', verbose_name='Enabled?')),
                ('feed_url', models.CharField(help_text='The URL of the feed.', max_length=1024)),
                ('auto_publish', models.BooleanField(default=False, help_text='Automatically publish posts from this feed?', verbose_name='Auto publish?')),
                ('out_feed', models.ForeignKey(help_text='Select the outbound feed to which this feed will be linked.', on_delete=django.db.models.deletion.CASCADE, to='feeds.outfeed')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=False, help_text='Determines whether or not this item is enabled.', verbose_name='Enabled?')),
                ('title', models.CharField(help_text='The title of the post.', max_length=1024)),
                ('author', models.CharField(help_text='The author of the post.', max_length=1024)),
                ('description', models.TextField(help_text='The description or summary of the post.')),
                ('override_desc', models.TextField(help_text='The description or summary of the post. Overrides the auto-fetched description.', null=True)),
                ('link', models.CharField(help_text='The URL of the post.', max_length=1024)),
                ('guid', models.CharField(help_text='The unique ID of the post.', max_length=1024)),
                ('published', models.DateTimeField(help_text='The publication date/time of the post.')),
                ('in_feed', models.ForeignKey(help_text='The inbound found from where the post originated.', on_delete=django.db.models.deletion.CASCADE, to='feeds.infeed')),
            ],
            options={
                'ordering': ['-published', 'in_feed__name', 'title'],
                'unique_together': {('in_feed', 'guid')},
            },
        ),
    ]