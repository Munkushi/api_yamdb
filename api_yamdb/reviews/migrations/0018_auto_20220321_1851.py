# Generated by Django 2.2.16 on 2022-03-21 15:51

from django.db import migrations, models
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0017_merge_20220320_1044'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('id',)},
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(db_index=True, validators=[reviews.validators.validate_year], verbose_name='Год'),
        ),
    ]
