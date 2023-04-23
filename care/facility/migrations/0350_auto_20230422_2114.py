# Generated by Django 2.2.11 on 2023-04-22 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0349_auto_20230422_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shiftingrequest',
            name='assigned_facility_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Educational Inst'), (2, 'Private Hospital'), (3, 'Other'), (4, 'Hostel'), (5, 'Hotel'), (6, 'Lodge'), (7, 'TeleMedicine'), (8, 'Govt Hospital'), (9, 'Labs'), (800, 'Primary Health Centres'), (801, '24x7 Public Health Centres'), (802, 'Family Health Centres'), (803, 'Community Health Centres'), (820, 'Urban Primary Health Center'), (830, 'Taluk Hospitals'), (831, 'Taluk Headquarters Hospitals'), (840, 'Women and Child Health Centres'), (850, 'General hospitals'), (860, 'District Hospitals'), (870, 'Govt Medical College Hospitals'), (900, 'Co-operative hospitals'), (910, 'Autonomous healthcare facility'), (950, 'Corona Testing Labs'), (1000, 'Corona Care Centre'), (1010, 'COVID-19 Domiciliary Care Center'), (1100, 'First Line Treatment Centre'), (1200, 'Second Line Treatment Center'), (1300, 'Shifting Centre'), (1400, 'Covid Management Center'), (1500, 'Request Approving Center'), (1510, 'Request Fulfilment Center'), (1600, 'District War Room')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='shiftingrequest',
            name='breathlessness_level',
            field=models.IntegerField(blank=True, choices=[(10, 'NOT SPECIFIED'), (15, 'NOT BREATHLESS'), (20, 'MILD'), (30, 'MODERATE'), (40, 'SEVERE')], default=10, null=True),
        ),
        migrations.AlterField(
            model_name='shiftingrequest',
            name='preferred_vehicle_choice',
            field=models.IntegerField(blank=True, choices=[(10, 'D Level Ambulance'), (20, 'All double chambered Ambulance with EMT'), (30, 'Ambulance without EMT'), (40, 'Car'), (50, 'Auto-rickshaw')], default=None, null=True),
        ),
    ]