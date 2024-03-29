# Generated by Django 4.2.3 on 2023-08-15 02:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_alter_product_product_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=250)),
                ('postal_code', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='order',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inventory',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_seller', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['-created'], name='social_orde_created_70e563_idx'),
        ),
        migrations.AddField(
            model_name='orderitems',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='social.order'),
        ),
        migrations.AddField(
            model_name='orderitems',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='social.product'),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='social.address'),
            preserve_default=False,
        ),
    ]
