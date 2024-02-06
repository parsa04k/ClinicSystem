# Generated by Django 4.2.7 on 2024-02-02 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_remove_appointment_clinicid_remove_appointment_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.TextField(choices=[('finished', 'Finished'), ('occupied', 'Occupied'), ('available', 'Available')], default='available'),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='address',
            field=models.TextField(max_length=255),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='name',
            field=models.TextField(max_length=20),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='services',
            field=models.TextField(max_length=255),
        ),
    ]