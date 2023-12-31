# Generated by Django 4.2.3 on 2023-07-22 05:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_retailerpayout_date_retailerpayout_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='britanniatarget',
            name='app_eco_retention',
            field=models.CharField(blank=True, help_text='App ECO Retention', max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='britanniatarget',
            name='bcrda',
            field=models.CharField(blank=True, help_text='BCRDA', max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='britanniatarget',
            name='date',
            field=models.DateField(blank=True, help_text='Inserted Date', null=True),
        ),
        migrations.AddField(
            model_name='britanniatarget',
            name='focus_brand',
            field=models.CharField(blank=True, help_text='Focus Brand', max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='britanniatarget',
            name='inserted_by',
            field=models.CharField(blank=True, help_text='Inserted By', max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='britanniatarget',
            name='over_all',
            field=models.CharField(blank=True, help_text='Over All', max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='britanniatarget',
            name='phasing',
            field=models.CharField(blank=True, help_text='Phasing', max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='britanniatarget',
            name='power_brand',
            field=models.CharField(blank=True, help_text='Power Brand', max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='britanniatarget',
            name='ulpr',
            field=models.CharField(blank=True, help_text='ULPR', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='britanniatarget',
            name='tier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.tier'),
        ),
    ]
