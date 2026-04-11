from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0021_contactinfo_legal_and_defaults'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceapplication',
            name='full_name',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='ФИО'),
        ),
        migrations.AlterField(
            model_name='tenderinvitation',
            name='full_name',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='ФИО'),
        ),
    ]
