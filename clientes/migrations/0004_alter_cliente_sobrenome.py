# Generated by Django 5.1.3 on 2024-12-08 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0003_alter_cliente_sobrenome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='sobrenome',
            field=models.CharField(max_length=50),
        ),
    ]