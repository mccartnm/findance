# Generated by Django 2.2 on 2019-04-26 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assets', '0001_initial'),
        ('entity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetownership',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entity.OwningEntity'),
        ),
        migrations.AlterUniqueTogether(
            name='assetownership',
            unique_together={('asset', 'owner')},
        ),
    ]
