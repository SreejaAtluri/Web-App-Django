# Generated by Django 4.0.4 on 2022-07-05 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_merge_20220705_1556'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'Student', 'verbose_name_plural': 'Students'},
        ),
        migrations.AddField(
            model_name='course',
            name='interested',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='stages',
            field=models.PositiveIntegerField(default=3),
        ),
        migrations.RemoveField(
            model_name='order',
            name='course',
        ),
        migrations.AddField(
            model_name='order',
            name='course',
            field=models.ManyToManyField(related_name='orders', to='myapp.course'),
        ),
        migrations.AlterField(
            model_name='order',
            name='levels',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.IntegerField(choices=[(0, 'Cancelled'), (1, 'Order Confirmed')], default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='myapp.student'),
        ),
        migrations.AlterField(
            model_name='student',
            name='address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='city',
            field=models.CharField(choices=[('WS', 'Windsor'), ('CG', 'Calgary'), ('MR', 'Montreal'), ('VC', 'Vancouver')], default='WS', max_length=2),
        ),
        migrations.AlterField(
            model_name='student',
            name='interested_in',
            field=models.ManyToManyField(related_name='students', to='myapp.topic'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='category',
            field=models.CharField(max_length=200),
        ),
    ]
