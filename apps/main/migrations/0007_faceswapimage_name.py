# Generated by Django 2.1.7 on 2019-03-01 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_faceswapimage_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='faceswapimage',
            name='name',
            field=models.TextField(blank=True, default=''),
        ),
    ]