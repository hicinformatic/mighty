# Generated by Django 2.2.7 on 2019-12-04 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mighty', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='email',
            options={'default_permissions': ('add', 'detail', 'list', 'change', 'delete', 'enable', 'disable', 'export', 'import', 'alert', 'error', 'admin_perm', 'askfor_perm'), 'ordering': ['-date_create'], 'permissions': [('check_email', 'Can check Email')], 'verbose_name': 'Email', 'verbose_name_plural': 'Emails'},
        ),
        migrations.AlterModelOptions(
            name='graph',
            options={'default_permissions': ('add', 'detail', 'list', 'change', 'delete', 'enable', 'disable', 'export', 'import', 'alert', 'error', 'admin_perm', 'askfor_perm'), 'verbose_name': 'Graphic', 'verbose_name_plural': 'Graphics'},
        ),
        migrations.AlterModelOptions(
            name='nationality',
            options={'ordering': ['country'], 'verbose_name': 'Nationalité', 'verbose_name_plural': 'Nationalités'},
        ),
        migrations.AlterModelOptions(
            name='sms',
            options={'default_permissions': ('add', 'detail', 'list', 'change', 'delete', 'enable', 'disable', 'export', 'import', 'alert', 'error', 'admin_perm', 'askfor_perm'), 'ordering': ['-date_create'], 'permissions': [('check_sms', 'Can check SMS')], 'verbose_name': 'SMS', 'verbose_name_plural': 'SMS'},
        ),
        migrations.AlterModelOptions(
            name='template',
            options={'default_permissions': ('add', 'detail', 'list', 'change', 'delete', 'enable', 'disable', 'export', 'import', 'alert', 'error', 'admin_perm', 'askfor_perm'), 'verbose_name': 'Graphic template', 'verbose_name_plural': 'Graphic templates'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'default_permissions': ('add', 'detail', 'list', 'change', 'delete', 'enable', 'disable', 'export', 'import', 'alert', 'error', 'admin_perm', 'askfor_perm'), 'ordering': ['last_name', 'first_name', 'email'], 'verbose_name': 'Utilisateur', 'verbose_name_plural': 'Utilisateurs'},
        ),
    ]
