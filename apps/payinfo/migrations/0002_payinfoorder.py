# Generated by Django 2.1.2 on 2019-06-27 06:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payinfo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayinfoOrder',
            fields=[
                ('uid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('price', models.IntegerField(default=0)),
                ('istype', models.SmallIntegerField(default=0)),
                ('status', models.SmallIntegerField(default=0)),
                ('pub_time', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('payinfo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='payinfo.PayInfo')),
            ],
            options={
                'ordering': ['-pub_time'],
            },
        ),
    ]
