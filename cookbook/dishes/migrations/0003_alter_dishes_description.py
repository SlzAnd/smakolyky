# Generated by Django 4.0.5 on 2022-06-10 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0002_dishes_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishes',
            name='description',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
