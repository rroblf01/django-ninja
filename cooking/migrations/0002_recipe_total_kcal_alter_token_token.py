# Generated by Django 4.2.7 on 2023-12-02 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='total_kcal',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.CharField(default='e60104e3ef0842bab522a5a0f1b0a583', max_length=100, unique=True),
        ),
    ]
