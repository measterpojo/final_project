# Generated by Django 4.1.7 on 2023-06-28 22:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('flag_count', models.PositiveIntegerField(default=0)),
                ('state', models.SmallIntegerField(choices=[(1, 'Unflagged'), (2, 'Flagged'), (3, 'Flag rejected by the moderator'), (4, 'Comment modified by the author')], default=1)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('moderator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='flags_moderated', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FlagInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField(blank=True, null=True)),
                ('date_flagged', models.DateTimeField(auto_now=True)),
                ('reason', models.SmallIntegerField(choices=[(1, 'Spam | Exists only to promote a service'), (2, 'Abusive | Intended at promoting hatred'), (100, 'Something else')], default=1)),
                ('flag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flags', to='flags.flag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flags', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date_flagged',),
                'unique_together': {('flag', 'user')},
            },
        ),
    ]
