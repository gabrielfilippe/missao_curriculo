# Generated by Django 5.0.6 on 2024-06-25 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_curriculo_area_de_interesse_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='endereco',
            name='endereco',
        ),
        migrations.RemoveField(
            model_name='pessoa',
            name='categoria',
        ),
        migrations.AddField(
            model_name='endereco',
            name='rua',
            field=models.CharField(default=1, max_length=255, verbose_name='Rua'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pessoa',
            name='categoria_da_cnh',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=255, null=True, verbose_name='Categoria da CNH'),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='numero',
            field=models.PositiveIntegerField(verbose_name='Número'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='e_pcd',
            field=models.BooleanField(default=False, verbose_name='É pessoa com deficiência?'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='e_primeiro_emprego',
            field=models.BooleanField(default=False, verbose_name='Primeiro Emprego?'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='possui_cnh',
            field=models.BooleanField(default=False, verbose_name='Possui CNH?'),
        ),
    ]
