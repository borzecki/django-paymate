# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created on')),
                ('name', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AccountBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=4, default=0, max_digits=14)),
                ('allow_negative_balance', models.BooleanField(default=False)),
                ('account',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('name', models.CharField(max_length=64)),
                ('code', models.CharField(max_length=3)),
            ],
            options={
                'verbose_name_plural': 'Currencies',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created on')),
                ('amount', models.DecimalField(decimal_places=4, max_digits=10)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Currency')),
                ('from_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                                   related_name='transactions_from', to='accounts.Account')),
                ('to_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                                 related_name='transactions_to', to='accounts.Account')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='currency',
            unique_together=set([('name', 'code')]),
        ),
        migrations.AddField(
            model_name='accountbalance',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Currency'),
        ),
    ]
