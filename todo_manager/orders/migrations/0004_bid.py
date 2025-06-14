# Generated by Django 5.1.6 on 2025-05-13 13:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_customer_alter_order_type_of_work'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Запропонована ціна (грн)')),
                ('comment', models.TextField(blank=True, verbose_name='Коментар виконавця')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата подання')),
                ('is_selected', models.BooleanField(default=False, verbose_name='Вибрано замовником')),
                ('executor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to=settings.AUTH_USER_MODEL, verbose_name='Виконавець')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='orders.order', verbose_name='Замовлення')),
            ],
            options={
                'verbose_name': 'Пропозиція',
                'verbose_name_plural': 'Пропозиції',
                'ordering': ['-created_at'],
            },
        ),
    ]
