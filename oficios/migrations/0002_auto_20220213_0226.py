# Generated by Django 3.2.4 on 2022-02-13 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oficios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oficio',
            name='año',
            field=models.IntegerField(default=2022, error_messages={'required': 'Este campo es obligatorio'}),
        ),
        migrations.AlterField(
            model_name='oficio',
            name='mes',
            field=models.CharField(choices=[('Ene', 'Enero'), ('Feb', 'Febrero'), ('Mar', 'Marzo'), ('Abr', 'Abril'), ('May', 'Mayo'), ('Jun', 'Junio'), ('Jul', 'Julio'), ('Ago', 'Agosto'), ('Sep', 'Septiembre'), ('Oct', 'Octubre'), ('Nov', 'Noviembre'), ('Dic', 'Diciembre')], default='Feb', max_length=3),
        ),
    ]
