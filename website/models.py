from django.db import models
from django.utils import timezone


class ContactInfo(models.Model):
    """Контактная информация компании"""
    legal_name = models.CharField("Юридическое наименование", max_length=200, default='ООО «Линкор»')
    inn = models.CharField("ИНН", max_length=20, default="7708424070")
    address = models.TextField(
        "Адрес (юридический / для карты и футера)",
        max_length=500,
        default="г. Москва, шоссе Энтузиастов, 31с38, оф. 430",
    )
    phone_main = models.CharField("Общий номер телефона (единый для всех страниц)", max_length=20, default="8-800-XXX-XX-XX")
    email_main = models.EmailField(
        "E-mail (для блока контактов и сайта)",
        max_length=254,
        blank=True,
        default="service@lin-cor.ru",
    )
    tender_invitation = models.TextField("Текст приглашения в тендер", max_length=1000, default="Приглашаем к участию в тендерах", blank=True)
    
    # Дополнительные телефоны (оставляем для совместимости)
    phone_emergency = models.CharField("Телефон аварийной службы", max_length=20, default="8-800-XXX-XX-XX")
    phone_government = models.CharField("Телефон для госзаказчиков", max_length=20, default="8-800-XXX-XX-XX")
    phone_technical = models.CharField("Отдел технического надзора", max_length=20, default="8-800-XXX-XX-XX")
    phone_orders = models.CharField("Телефон для заказа услуг", max_length=20, default="8-800-XXX-XX-XX")
    
    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактная информация"
    
    def __str__(self):
        return f"Контакты компании"


class ServiceApplication(models.Model):
    """Заявки на услуги"""
    SERVICE_CHOICES = [
        ('main_page', 'Главная страница'),
        ('complex_service', 'Комплексное обслуживание инженерных систем'),
        ('heating_service', 'Комплексное обслуживание ИТП и ЦТП «под ключ»'),
        ('verification_service', 'Поверка, ремонт и восстановление приборов учета'),
        ('emergency_service', 'Аварийная служба'),
        ('installation_service', 'Монтаж инженерных коммуникаций'),
        ('audit_service', 'Аудит инженерных систем для госзаказчиков'),
        ('heating_preparation_service', 'Подготовка к отопительному сезону'),
        ('ventilation_service', 'Профессиональное техническое обслуживание климатических систем'),
    ]
    
    REQUEST_TYPE_CHOICES = [
        ('application', 'Оставить заявку'),
        ('callback', 'Заказать звонок специалиста'),
        ('emergency_call', 'Вызвать аварийную службу'),
        ('quote_request', 'Запросить КП/коммерческое предложение'),
        ('phone_call', 'Позвонить сейчас'),
    ]
    
    full_name = models.CharField("ФИО", max_length=200, blank=True, default="")
    phone = models.CharField("Телефон", max_length=20)
    organization = models.CharField("Организация", max_length=200, blank=True, null=True)
    message = models.TextField("Сообщение", blank=True, null=True)
    preferred_time = models.CharField("Удобное время для звонка", max_length=50, blank=True, null=True)
    service_type = models.CharField("Страница-источник", max_length=30, choices=SERVICE_CHOICES)
    request_type = models.CharField("Тип заявки", max_length=20, choices=REQUEST_TYPE_CHOICES, default='application')
    created_at = models.DateTimeField("Дата создания", default=timezone.now)
    processed = models.BooleanField("Обработана", default=False)
    
    class Meta:
        verbose_name = "Заявка на услугу"
        verbose_name_plural = "Заявки на услуги"
        ordering = ['-created_at']
    
    def __str__(self):
        label = (self.full_name or "").strip() or self.phone
        return f"{label} — {self.get_service_type_display()}"


class CallbackRequest(ServiceApplication):
    """Прокси-модель: в админке отдельный раздел только для обратных звонков."""

    class Meta:
        proxy = True
        verbose_name = "Обратный звонок"
        verbose_name_plural = "Обратные звонки"


class TenderInvitation(models.Model):
    """Приглашения в тендер"""
    full_name = models.CharField("ФИО", max_length=200, blank=True, default="")
    phone = models.CharField("Телефон для связи", max_length=20)
    company_name = models.CharField("Название компании", max_length=200, blank=True)
    technical_task = models.FileField("Техническое задание", upload_to='tender_tasks/', blank=True, null=True)
    agreed_to_processing = models.BooleanField("Согласие на обработку данных", default=False)
    created_at = models.DateTimeField("Дата создания", default=timezone.now)
    processed = models.BooleanField("Обработана", default=False)
    
    class Meta:
        verbose_name = "Приглашение в тендер"
        verbose_name_plural = "Приглашения в тендер"
        ordering = ['-created_at']
    
    def __str__(self):
        label = (self.full_name or "").strip() or self.phone
        company = (self.company_name or "").strip()
        return f"{label} — {company}" if company else label


class Photo(models.Model):
    """Фиксированные фотографии для сайта (команда специалистов и т.д.)"""
    PHOTO_TYPES = [
        # Главная страница
        ('main_team_1', 'Главная страница - У нас работают люди, проверенные временем! - Фото 1'),
        ('main_team_2', 'Главная страница - У нас работают люди, проверенные временем! - Фото 2'),
        ('main_team_3', 'Главная страница - У нас работают люди, проверенные временем! - Фото 3'),
        ('main_team_4', 'Главная страница - У нас работают люди, проверенные временем! - Фото 4'),
        
        # Аварийная служба
        ('emergency_photo_1', 'Аварийная служба - Фото 1'),
        ('emergency_photo_2', 'Аварийная служба - Фото 2'),
        
        # Комплексное обслуживание инженерных систем
        ('complex_team_1', 'Комплексное обслуживание - У нас работают люди, проверенные временем! - Фото 1'),
        ('complex_team_2', 'Комплексное обслуживание - У нас работают люди, проверенные временем! - Фото 2'),
        ('complex_team_3', 'Комплексное обслуживание - У нас работают люди, проверенные временем! - Фото 3'),
        ('complex_team_4', 'Комплексное обслуживание - У нас работают люди, проверенные временем! - Фото 4'),
        
        # Комплексное обслуживание ИТП и ЦТП «под ключ»
        ('heating_professional_1', 'ИТП и ЦТП - Профессиональное обслуживание тепловых пунктов - Фото 1'),
        ('heating_professional_2', 'ИТП и ЦТП - Профессиональное обслуживание тепловых пунктов - Фото 2'),
        ('heating_professional_3', 'ИТП и ЦТП - Профессиональное обслуживание тепловых пунктов - Фото 3'),
        ('heating_professional_4', 'ИТП и ЦТП - Профессиональное обслуживание тепловых пунктов - Фото 4'),
        
        # Аварийная служба
        ('emergency_team_1', 'Аварийная служба - Команда специалистов аварийной службы - Фото 1'),
        ('emergency_team_2', 'Аварийная служба - Команда специалистов аварийной службы - Фото 2'),
        ('emergency_team_3', 'Аварийная служба - Команда специалистов аварийной службы - Фото 3'),
        ('emergency_team_4', 'Аварийная служба - Команда специалистов аварийной службы - Фото 4'),
        
        # Профессиональное техническое обслуживание климатических систем
        ('ventilation_team_1', 'Техническое обслуживание климатических систем - Команда специалистов по вентиляции - Фото 1'),
        ('ventilation_team_2', 'Техническое обслуживание климатических систем - Команда специалистов по вентиляции - Фото 2'),
        ('ventilation_team_3', 'Техническое обслуживание климатических систем - Команда специалистов по вентиляции - Фото 3'),
        ('ventilation_team_4', 'Техническое обслуживание климатических систем - Команда специалистов по вентиляции - Фото 4'),
    ]
    
    title = models.CharField("Название", max_length=100)
    photo_type = models.CharField("Тип фотографии", max_length=30, choices=PHOTO_TYPES, unique=True)
    image = models.ImageField("Изображение", upload_to='photos/')
    alt_text = models.CharField("Альтернативный текст", max_length=200, blank=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    
    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"
    
    def __str__(self):
        return f"{self.title} ({self.get_photo_type_display()})"


class GalleryPhoto(models.Model):
    """Галерея фотографий - можно добавлять неограниченное количество"""
    GALLERY_TYPES = [
        ('main_objects', 'Главная страница - Живые фотографии с объектов'),
        ('complex_objects', 'Комплексное обслуживание - Живые фотографии с объектов'),
        ('heating_objects', 'ИТП и ЦТП - Фотографии с объектов'),
        ('verification_objects', 'Поверка приборов - Живые фотографии с объектов'),
        ('audit_objects', 'Аудит систем - Живые фотографии с объектов'),
        ('preparation_objects', 'Подготовка к отопительному сезону - Фотографии с объектов'),
    ]
    
    title = models.CharField("Название", max_length=100)
    gallery_type = models.CharField("Тип галереи", max_length=30, choices=GALLERY_TYPES)
    image = models.ImageField("Изображение", upload_to='gallery/')
    alt_text = models.CharField("Альтернативный текст", max_length=200, blank=True)
    order = models.PositiveIntegerField("Порядок отображения", default=0, help_text="Чем меньше число, тем раньше отображается")
    is_active = models.BooleanField("Активная", default=True)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    
    class Meta:
        verbose_name = "Фото в галерее"
        verbose_name_plural = "Галерея фотографий"
        ordering = ['gallery_type', 'order', 'created_at']
    
    def __str__(self):
        return f"{self.get_gallery_type_display()} - {self.title}"


class DownloadableDocument(models.Model):
    """Документы для скачивания"""
    DOCUMENT_TYPES = [
        ('audit_form', 'Форма заявки для аудита'),
        ('heating_form', 'Форма заявки для подготовки к отопительному сезону'),
    ]
    
    title = models.CharField("Название документа", max_length=200)
    document_type = models.CharField("Тип документа", max_length=20, choices=DOCUMENT_TYPES, unique=True)
    file = models.FileField("Файл", upload_to='documents/')
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    
    class Meta:
        verbose_name = "Документ для скачивания"
        verbose_name_plural = "Документы для скачивания"
    
    def __str__(self):
        return self.title


class CommercialProposal(models.Model):
    """Коммерческое предложение для страницы аудита"""
    title = models.CharField("Название", max_length=200, default="Коммерческое предложение")
    image = models.ImageField("Изображение", upload_to='commercial_proposals/')
    alt_text = models.CharField("Альтернативный текст", max_length=200, blank=True, default="Коммерческое предложение")
    description = models.TextField("Описание", max_length=500, default="Подробная информация о стоимости услуг")
    is_active = models.BooleanField("Активное", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    
    class Meta:
        verbose_name = "Коммерческое предложение"
        verbose_name_plural = "Коммерческие предложения"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title




# Proxy модели для группировки в админ панели
class PhotoGroup(Photo):
    """Группа Фото"""
    class Meta:
        proxy = True
        verbose_name = "Фото"
        verbose_name_plural = "Фото"

class GalleryGroup(GalleryPhoto):
    """Группа Фотогалерея"""
    class Meta:
        proxy = True
        verbose_name = "Фотогалерея"
        verbose_name_plural = "Фотогалерея"

class ComplexGalleryGroup(GalleryPhoto):
    """Группа Галерея Комплексное обслуживание инженерных систем"""
    class Meta:
        proxy = True
        verbose_name = "Галерея Комплексное обслуживание инженерных систем"
        verbose_name_plural = "Галерея Комплексное обслуживание инженерных систем"

class HeatingGalleryGroup(GalleryPhoto):
    """Группа Галерея Комплексное обслуживание ИТП и ЦТП «под ключ»"""
    class Meta:
        proxy = True
        verbose_name = "Галерея Комплексное обслуживание ИТП и ЦТП «под ключ»"
        verbose_name_plural = "Галерея Комплексное обслуживание ИТП и ЦТП «под ключ»"

class VerificationGalleryGroup(GalleryPhoto):
    """Группа Галерея Поверка, ремонт и восстановление приборов учета"""
    class Meta:
        proxy = True
        verbose_name = "Галерея Поверка, ремонт и восстановление приборов учета"
        verbose_name_plural = "Галерея Поверка, ремонт и восстановление приборов учета"

class EmergencyPhotoGroup(Photo):
    """Группа Фото Аварийная служба"""
    class Meta:
        proxy = True
        verbose_name = "Фото Аварийная служба"
        verbose_name_plural = "Фото Аварийная служба"

class AuditGalleryGroup(GalleryPhoto):
    """Группа Галерея Аудит инженерных систем для госзаказчиков"""
    class Meta:
        proxy = True
        verbose_name = "Галерея Аудит инженерных систем для госзаказчиков"
        verbose_name_plural = "Галерея Аудит инженерных систем для госзаказчиков"

class PreparationGalleryGroup(GalleryPhoto):
    """Группа Галерея Подготовка к отопительному сезону"""
    class Meta:
        proxy = True
        verbose_name = "Галерея Подготовка к отопительному сезону"
        verbose_name_plural = "Галерея Подготовка к отопительному сезону"

class VentilationPhotoGroup(Photo):
    """Группа Фото Профессиональное техническое обслуживание"""
    class Meta:
        proxy = True
        verbose_name = "Фото Профессиональное техническое обслуживание"
        verbose_name_plural = "Фото Профессиональное техническое обслуживание"

class HeatingPhotoGroup(Photo):
    """Группа Фото Комплексное обслуживание ИТП и ЦТП «под ключ»"""
    class Meta:
        proxy = True
        verbose_name = "Фото Комплексное обслуживание ИТП и ЦТП «под ключ»"
        verbose_name_plural = "Фото Комплексное обслуживание ИТП и ЦТП «под ключ»"
