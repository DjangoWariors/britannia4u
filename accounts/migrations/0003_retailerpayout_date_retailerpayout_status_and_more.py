# Generated by Django 4.2.3 on 2023-07-21 06:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_rsm'),
    ]

    operations = [
        migrations.AddField(
            model_name='retailerpayout',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retailerpayout',
            name='status',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='britanniapoint',
            name='date',
            field=models.DateField(blank=True, help_text='Insert Date', null=True),
        ),
        migrations.CreateModel(
            name='BritanniaTarget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Pending', 'Pending')], max_length=50, null=True)),
                ('reason', models.CharField(blank=True, choices=[('Reason for changing the targets - ACE CLUB', 'Reason for changing the targets - ACE CLUB'), ('Retailer started purchasing from other Source', 'Retailer started purchasing from other Source'), ('Municipal Work in Progress', 'Municipal Work in Progress'), ('Retailer sale has gone Down', 'Retailer sale has gone Down'), ('Festival Season', 'Festival Season'), ('Want to Increase Target', 'Want to Increase Target'), ('Store permanently Closed', 'Store permanently Closed'), ('Store temporarily closed', 'Store temporarily closed')], max_length=256, null=True)),
                ('tier', models.CharField(blank=True, max_length=256, null=True)),
                ('month', models.CharField(blank=True, max_length=15, null=True)),
                ('year', models.CharField(blank=True, max_length=15, null=True)),
                ('bcradl_target', models.CharField(blank=True, help_text=' BCRADL Target', max_length=80, null=True)),
                ('biscuit_target', models.CharField(blank=True, help_text='Biscuit Target', max_length=80, null=True)),
                ('cradl_target', models.CharField(blank=True, help_text='CRADL Target', max_length=80, null=True)),
                ('unqiue_target', models.CharField(blank=True, help_text='Unqiue Lines Target', max_length=80, null=True)),
                ('ghee_target', models.CharField(blank=True, help_text='Ghee Target', max_length=80, null=True)),
                ('focus_target1', models.CharField(blank=True, help_text='Focus Target1', max_length=80, null=True)),
                ('focus_target2', models.CharField(blank=True, help_text='Focus Target2', max_length=80, null=True)),
                ('cheese', models.CharField(blank=True, help_text='Cheese', max_length=80, null=True)),
                ('cheese_ulpo', models.CharField(blank=True, help_text='Cheese ULPO', max_length=80, null=True)),
                ('visibility', models.CharField(blank=True, help_text='Visibility', max_length=80, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, help_text='Retailer', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
