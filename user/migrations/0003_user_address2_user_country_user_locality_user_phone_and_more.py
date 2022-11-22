# Generated by Django 4.0.8 on 2022-11-20 01:45

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_managers_remove_user_username_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address2',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='address2'),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='country'),
        ),
        migrations.AddField(
            model_name='user',
            name='locality',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='locality'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=150, null=True, region=None),
        ),
        migrations.AddField(
            model_name='user',
            name='postcode',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='postcode'),
        ),
        migrations.AddField(
            model_name='user',
            name='ship_address',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='ship_address'),
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='state'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=150, verbose_name='last name'),
        ),
    ]
