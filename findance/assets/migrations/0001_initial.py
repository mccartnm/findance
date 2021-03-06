# Generated by Django 2.2 on 2019-04-26 15:52

from django.db import migrations, models
import django.db.models.deletion
import findance.abstract


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', findance.abstract.FindanceIdField(default=findance.abstract.FindanceIdField._build_id, primary_key=True, serialize=False)),
                ('name', models.TextField(unique=True)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('value', findance.abstract.MonetaryField(decimal_places=10, default=1.0, max_digits=64)),
            ],
            options={
                'ordering': ('id',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AssetOwnership',
            fields=[
                ('id', findance.abstract.FindanceIdField(default=findance.abstract.FindanceIdField._build_id, primary_key=True, serialize=False)),
                ('percentage', findance.abstract.MonetaryField(decimal_places=10, default=1.0, max_digits=64)),
                ('count', models.PositiveIntegerField()),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
        ),
    ]
