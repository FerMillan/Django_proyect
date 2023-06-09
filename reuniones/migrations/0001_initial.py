# Generated by Django 3.2.4 on 2021-11-30 17:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reunion',
            fields=[
                ('folio', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('fecha', models.DateField(error_messages={'required': 'Este campo es obligatorio'})),
                ('mes', models.CharField(choices=[('Ene', 'Enero'), ('Feb', 'Febrero'), ('Mar', 'Marzo'), ('Abr', 'Abril'), ('May', 'Mayo'), ('Jun', 'Junio'), ('Jul', 'Julio'), ('Ago', 'Agosto'), ('Sep', 'Septiembre'), ('Oct', 'Octubre'), ('Nov', 'Noviembre'), ('Dic', 'Diciembre')], default='Nov', max_length=3)),
                ('año', models.IntegerField(default=2021, error_messages={'required': 'Este campo es obligatorio'})),
                ('inicio', models.TimeField(error_messages={'required': 'Este campo es obligatorio'})),
                ('termino', models.TimeField(error_messages={'required': 'Este campo es obligatorio'})),
                ('lugar', models.TextField(error_messages={'required': 'Este campo es obligatorio'}, max_length=180)),
                ('asunto', models.CharField(error_messages={'max_length': 'La longitud máxima es de 120 caracteres', 'required': 'Este campo es obligatorio'}, max_length=120)),
                ('observaciones', models.TextField(error_messages={'required': 'Este campo es obligatorio'}, max_length=200)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Participante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(error_messages={'max_length': 'La longitud máxima es de 80 caracteres', 'required': 'Este campo es obligatorio'}, help_text='Nombre', max_length=80)),
                ('apellido_p', models.CharField(error_messages={'max_length': 'La longitud máxima es de 80 caracteres', 'required': 'Este campo es obligatorio'}, help_text='Apellido Paterno', max_length=80)),
                ('apellido_m', models.CharField(error_messages={'max_length': 'La longitud máxima es de 80 caracteres', 'required': 'Este campo es obligatorio'}, help_text='Apellido Materno', max_length=80)),
                ('instituto', models.CharField(error_messages={'max_length': 'La longitud máxima es de 200 caracteres', 'required': 'Este campo es obligatorio'}, help_text='Instituto', max_length=200)),
                ('email', models.EmailField(error_messages={'required': 'Este campo es obligatorio'}, max_length=254)),
                ('reunion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reuniones.reunion')),
            ],
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documento', models.FileField(blank=True, upload_to='static/pdf')),
                ('reunion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reuniones.reunion')),
            ],
        ),
    ]
