from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0018_alter_contactinfo_address_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactinfo',
            name='email_main',
            field=models.EmailField(
                blank=True,
                default='',
                max_length=254,
                verbose_name='E-mail (для блока контактов и сайта)',
            ),
        ),
    ]
