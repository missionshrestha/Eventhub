# Generated by Django 3.2.6 on 2021-08-09 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_merge_0003_auto_20210711_1508_0003_auto_20210724_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
