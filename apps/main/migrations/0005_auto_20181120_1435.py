# Generated by Django 2.1.2 on 2018-11-20 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20181119_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faceswapimage',
            name='image',
            field=models.ImageField(blank=True, upload_to='./'),
        ),
    ]