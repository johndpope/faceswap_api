# Generated by Django 2.1.7 on 2019-03-01 14:30

import apps.main.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_faceswapimage_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faceswapimage',
            name='name',
            field=models.TextField(default=apps.main.models.generate_filename, unique=True),
        ),
    ]
