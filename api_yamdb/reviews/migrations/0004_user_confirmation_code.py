# Generated by Django 2.2.16 on 2022-03-16 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20220315_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='XXXX', max_length=255, null=True, verbose_name='код подтверждения'),
        ),
    ]
