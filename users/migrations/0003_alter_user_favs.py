# Generated by Django 4.0b1 on 2021-11-05 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_auto_20191216_0937'),
        ('users', '0002_alter_user_avatar_alter_user_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='favs',
            field=models.ManyToManyField(null=True, related_name='favs', to='rooms.Room'),
        ),
    ]
