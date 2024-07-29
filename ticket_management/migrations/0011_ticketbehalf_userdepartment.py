# Generated by Django 4.1.8 on 2024-07-26 10:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticket_management', '0010_ticket_ticketfollower_ticketrevision'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketBehalf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('behalf_email', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ticket_behalf_created_by', to=settings.AUTH_USER_MODEL)),
                ('ticket_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_behalf_ticket', to='ticket_management.ticket')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ticket_behalf_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ticket_behalf',
            },
        ),
        migrations.CreateModel(
            name='UserDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(blank=True, null=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_department_created_by', to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_department_department', to='ticket_management.department')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_department_updated_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_department_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_department',
                'ordering': ['-created_on'],
                'unique_together': {('department', 'user')},
            },
        ),
    ]
