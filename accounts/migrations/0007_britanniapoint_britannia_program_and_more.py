# Generated by Django 4.2.3 on 2023-07-24 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_britanniapointyearmaster_britanniapoint_bpu_remark_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='britanniapoint',
            name='britannia_program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.britanniaprogram'),
        ),
        migrations.AddField(
            model_name='britanniapoint',
            name='britannia_program_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='britanniapointyearmaster',
            name='britannia_program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.britanniaprogram'),
        ),
        migrations.AddField(
            model_name='britanniapointyearmaster',
            name='britannia_program_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
