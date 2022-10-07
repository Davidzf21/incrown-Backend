# Generated by Django 4.1.1 on 2022-10-04 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('nombre', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=200)),
                ('correo', models.CharField(max_length=50, unique=True)),
                ('valoracion', models.FloatField(default=0.0)),
                ('numValoraciones', models.PositiveIntegerField(default=0)),
                ('numEventosCreados', models.PositiveIntegerField(default=0)),
                ('numEventosParticipa', models.PositiveIntegerField(default=0)),
                ('amigos', models.ManyToManyField(to='incrown_app.usuario')),
            ],
        ),
    ]
