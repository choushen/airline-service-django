# Generated by Django 2.0.5 on 2018-05-08 00:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('airlines', '0003_auto_20180507_2042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='booking_number',
            new_name='booking_num',
        ),
    ]
