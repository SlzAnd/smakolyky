# Generated by Django 4.0.5 on 2022-06-12 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0004_alter_dishes_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishes',
            name='description',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
