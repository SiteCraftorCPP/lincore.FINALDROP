# Юр. реквизиты в футере, актуальный адрес и e-mail по умолчанию

from django.db import migrations, models


OLD_ADDRESS_DEFAULT = "г. Москва, шоссе Энтузиастов, д. 31, строение 38"
NEW_ADDRESS = "г. Москва, шоссе Энтузиастов, 31с38, оф. 430"


def sync_contactinfo_row(apps, schema_editor):
    ContactInfo = apps.get_model("website", "ContactInfo")
    for row in ContactInfo.objects.all():
        if not (row.legal_name or "").strip():
            row.legal_name = "ООО «Линкор»"
        if not (row.inn or "").strip():
            row.inn = "7708424070"
        addr = (row.address or "").strip()
        if not addr or addr == OLD_ADDRESS_DEFAULT:
            row.address = NEW_ADDRESS
        em = (row.email_main or "").strip().lower()
        if not em or "info@linkor-msk" in em:
            row.email_main = "service@lin-cor.ru"
        row.save(update_fields=["legal_name", "inn", "address", "email_main"])


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0020_callback_request_proxy"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactinfo",
            name="legal_name",
            field=models.CharField(
                default="ООО «Линкор»",
                max_length=200,
                verbose_name="Юридическое наименование",
            ),
        ),
        migrations.AddField(
            model_name="contactinfo",
            name="inn",
            field=models.CharField(
                default="7708424070",
                max_length=20,
                verbose_name="ИНН",
            ),
        ),
        migrations.AlterField(
            model_name="contactinfo",
            name="address",
            field=models.TextField(
                default=NEW_ADDRESS,
                max_length=500,
                verbose_name="Адрес (юридический / для карты и футера)",
            ),
        ),
        migrations.AlterField(
            model_name="contactinfo",
            name="email_main",
            field=models.EmailField(
                blank=True,
                default="service@lin-cor.ru",
                max_length=254,
                verbose_name="E-mail (для блока контактов и сайта)",
            ),
        ),
        migrations.RunPython(sync_contactinfo_row, migrations.RunPython.noop),
    ]
