# Generated manually: default address text for ContactInfo

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0017_commercialproposal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='address',
            field=models.TextField(
                default='г. Москва, шоссе Энтузиастов, д. 31, строение 38',
                max_length=500,
                verbose_name='Адрес',
            ),
        ),
    ]
