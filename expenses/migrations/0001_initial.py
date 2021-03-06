# Generated by Django 3.1.3 on 2020-11-29 15:29

from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CostCenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Cost Center',
                'verbose_name_plural': 'Cost Centers',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='VariableCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cost_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'Euro')], default='XYZ', editable=False, max_length=3)),
                ('cost', djmoney.models.fields.MoneyField(decimal_places=2, max_digits=19)),
                ('notes', models.TextField(blank=True)),
                ('cost_center', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='expenses.costcenter')),
                ('tags', models.ManyToManyField(blank=True, to='expenses.Tag')),
            ],
            options={
                'verbose_name': 'Variable Cost',
                'verbose_name_plural': 'Variable Costs',
            },
        ),
    ]
