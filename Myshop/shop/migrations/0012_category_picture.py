# Generated by Django 5.1.2 on 2024-11-13 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_rename_name_brand_brandname'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='picture',
            field=models.ImageField(default='path/to/default/image.jpg', upload_to='category_pictures/'),
        ),
    ]
