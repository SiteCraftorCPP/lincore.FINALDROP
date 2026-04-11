from pathlib import Path
from types import SimpleNamespace
from typing import Optional

from django.conf import settings
from django.templatetags.static import static as static_asset_url
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
from .models import ContactInfo, ServiceApplication, TenderInvitation, CommercialProposal


def get_contact_info():
    """Получить контактную информацию (всегда объект с полями по умолчанию)."""
    try:
        info = ContactInfo.objects.first()
        if info is not None:
            return info
    except Exception:
        pass
    return ContactInfo()


def _media_photo_placeholder(url, alt_text=''):
    """Объект как у ImageField: шаблоны используют {{ x.image.url }} и x.alt_text."""
    return SimpleNamespace(image=SimpleNamespace(url=url), alt_text=alt_text)


def _db_upload_file_exists(obj) -> bool:
    """
    True, если у записи из БД (Photo / GalleryPhoto) реально есть файл в MEDIA_ROOT.
    У объектов из _media_photo_placeholder нет image.name — считаем источник валидным.
    """
    img = getattr(obj, 'image', None)
    if img is None:
        return False
    name = getattr(img, 'name', None)
    if name is None:
        return bool(getattr(img, 'url', None))
    name_str = str(name).strip()
    if not name_str:
        try:
            return bool(img.url)
        except Exception:
            return False
    return (Path(settings.MEDIA_ROOT) / name_str).is_file()


def _fill_bundled_if_missing(photos: dict, key: str, url: Optional[str], alt_text: str) -> None:
    """Подставляет bundled/static URL, если слота нет или файл из админки на диске отсутствует."""
    if not url:
        return
    cur = photos.get(key)
    if cur is None or not _db_upload_file_exists(cur):
        photos[key] = _media_photo_placeholder(url, alt_text)


# Копии тех же путей, что в media/, но под static/bundled_media/ — в git, без загрузки на VPS через админку
BUNDLED_MEDIA_PREFIX = 'bundled_media'


def _public_image_url(relative_path: str) -> Optional[str]:
    """
    URL картинки: сначала файл из MEDIA (админка / заливка на сервер),
    иначе — из static/bundled_media/... (приходит на VPS вместе с git + collectstatic).
    """
    rel = relative_path.replace('\\', '/').strip('/')
    if not rel:
        return None
    media_abs = Path(settings.MEDIA_ROOT) / rel
    if media_abs.is_file():
        return f"{settings.MEDIA_URL.rstrip('/')}/{rel}"
    bundled_abs = Path(settings.BASE_DIR) / 'static' / BUNDLED_MEDIA_PREFIX / rel
    if bundled_abs.is_file():
        return static_asset_url(f'{BUNDLED_MEDIA_PREFIX}/{rel}')
    return None


def get_photos_context():
    """Получить все фотографии для контекста"""
    from .models import Photo, GalleryPhoto

    photos = {}
    
    # Сначала получаем фотографии из базы данных (приоритет)
    try:
        photo_objects = Photo.objects.all()
        for photo in photo_objects:
            photos[photo.photo_type] = photo
    except Exception as e:
        print(f"Error loading photos from database: {e}")
    
    # Загружаем фотографии галереи главной страницы
    try:
        gallery_photos = GalleryPhoto.objects.filter(gallery_type='main_objects', is_active=True).order_by('order')
        for i, gallery_photo in enumerate(gallery_photos, 1):
            photos[f'main_gallery_{i}'] = gallery_photo
    except Exception as e:
        print(f"Error loading gallery photos from database: {e}")
    
    # Загружаем фотографии комплексного обслуживания
    try:
        complex_photos = GalleryPhoto.objects.filter(gallery_type='complex_objects', is_active=True).order_by('order')
        for i, complex_photo in enumerate(complex_photos, 1):
            photos[f'complex_electro_{i}'] = complex_photo
    except Exception as e:
        print(f"Error loading complex photos from database: {e}")
    
    # Загружаем фотографии ИТП и ЦТП
    try:
        heating_photos = GalleryPhoto.objects.filter(gallery_type='heating_objects', is_active=True).order_by('order')
        for i, heating_photo in enumerate(heating_photos, 1):
            photos[f'heating_gallery_{i}'] = heating_photo
    except Exception as e:
        print(f"Error loading heating photos from database: {e}")
    
    # Загружаем фотографии поверки
    try:
        verification_photos = GalleryPhoto.objects.filter(gallery_type='verification_objects', is_active=True).order_by('order')
        for i, verification_photo in enumerate(verification_photos, 1):
            photos[f'verification_gallery_{i}'] = verification_photo
    except Exception as e:
        print(f"Error loading verification photos from database: {e}")

    # Загружаем фотографии аудита
    try:
        audit_photos = GalleryPhoto.objects.filter(gallery_type='audit_objects', is_active=True).order_by('order')
        for i, audit_photo in enumerate(audit_photos, 1):
            photos[f'audit_gallery_{i}'] = audit_photo
    except Exception as e:
        print(f"Error loading audit photos from database: {e}")
    
    # Загружаем фотографии аварийной службы
    try:
        emergency_photos = Photo.objects.filter(photo_type__startswith='emergency_photo')
        for emergency_photo in emergency_photos:
            photos[emergency_photo.photo_type] = emergency_photo
    except Exception as e:
        print(f"Error loading emergency photos from database: {e}")
    
    # Загружаем фотографии подготовки к отопительному сезону
    try:
        preparation_photos = GalleryPhoto.objects.filter(gallery_type='preparation_objects', is_active=True).order_by('order')
        for i, preparation_photo in enumerate(preparation_photos, 1):
            photos[f'preparation_gallery_{i}'] = preparation_photo
    except Exception as e:
        print(f"Error loading preparation photos from database: {e}")
    
    # Загружаем фотографии вентиляции
    try:
        ventilation_photos = Photo.objects.filter(photo_type__startswith='ventilation_team')
        for ventilation_photo in ventilation_photos:
            photos[ventilation_photo.photo_type] = ventilation_photo
    except Exception as e:
        print(f"Error loading ventilation photos from database: {e}")

    # Загружаем фотографии ИТП и ЦТП
    try:
        heating_photos = Photo.objects.filter(photo_type__startswith='heating_professional')
        for heating_photo in heating_photos:
            photos[heating_photo.photo_type] = heating_photo
    except Exception as e:
        print(f"Error loading heating photos from database: {e}")
    
    # Файлы с диска: сначала MEDIA, иначе static/bundled_media/ (в репозитории для VPS).
    # Записи в БД без файла на диске (типично после бэка/миграций на VPS) не блокируют подстановку bundled.
    for i in range(1, 5):
        photo_file = f'photo{i}.jpg'
        team_key = f'main_team_{i}'
        url = _public_image_url(f'str1/{photo_file}')
        _fill_bundled_if_missing(photos, team_key, url, f'Специалист {i}')

    for i in range(14, 18):
        photo_file = f'photo{i}.jpg'
        gallery_index = i - 13
        gallery_key = f'main_gallery_{gallery_index}'
        url = _public_image_url(f'str1/{photo_file}')
        _fill_bundled_if_missing(photos, gallery_key, url, f'Галерея фото {gallery_index}')

    for i in range(5, 9):
        photo_file = f'photo{i}.jpg'
        url = _public_image_url(f'str2/{photo_file}')
        if not url:
            continue
        photos[f'service_str2_{i}'] = _media_photo_placeholder(url, f'Фото {i}')
        complex_index = i - 4
        complex_key = f'complex_str2_{complex_index}'
        _fill_bundled_if_missing(photos, complex_key, url, f'Фото {i}')
        if i == 5:
            _fill_bundled_if_missing(photos, 'complex_team_1', url, 'Специалист 1 - Комплексное обслуживание')
        elif i == 6:
            _fill_bundled_if_missing(photos, 'complex_team_2', url, 'Специалист 2 - Комплексное обслуживание')
        elif i == 7:
            _fill_bundled_if_missing(photos, 'complex_electro_1', url, 'Электрохозяйство 1 - Комплексное обслуживание')
        elif i == 8:
            _fill_bundled_if_missing(photos, 'complex_electro_2', url, 'Электрохозяйство 2 - Комплексное обслуживание')

    photo9_url = _public_image_url('str3/photo9.jpg')
    if photo9_url:
        _fill_bundled_if_missing(photos, 'service_str3_9', photo9_url, 'Фото 9')
        _fill_bundled_if_missing(photos, 'heating_str3_1', photo9_url, 'ИТП отопления')
        _fill_bundled_if_missing(photos, 'heating_team_1', photo9_url, 'Команда ИТП 1')

    url_ff = _public_image_url('str3/photoFF.jpg')
    if url_ff:
        _fill_bundled_if_missing(photos, 'heating_team_2', url_ff, 'Команда ИТП 2')

    gallery_files = ['photou', 'photop', 'photoy', 'photog']
    for i, stem in enumerate(gallery_files, 1):
        heating_key = f'heating_gallery_{i}'
        url = _public_image_url(f'str3/{stem}.jpg')
        _fill_bundled_if_missing(photos, heating_key, url, f'Работа специалистов ИТП {i}')

    gallery_files_v = ['photojk', 'photopkk', 'photoub', 'photogl']
    for i, stem in enumerate(gallery_files_v, 1):
        verification_key = f'verification_gallery_{i}'
        url = _public_image_url(f'str4/{stem}.jpg')
        _fill_bundled_if_missing(photos, verification_key, url, f'Работа специалистов поверки {i}')

    for i in range(10, 14):
        photo_file = f'photo{i}.jpg'
        url = _public_image_url(f'str5/{photo_file}')
        if not url:
            continue
        photos[f'service_str5_{i}'] = _media_photo_placeholder(url, f'Фото {i}')
        gallery_index = i - 9
        photos[f'emergency_gallery_{gallery_index}'] = _media_photo_placeholder(
            url, f'Аварийная служба фото {gallery_index}',
        )

    url_p1 = _public_image_url('str8/photougtt.jpg')
    if url_p1:
        _fill_bundled_if_missing(photos, 'preparation_team_1', url_p1, 'Специалист подготовки 1')
    url_p2 = _public_image_url('str8/photoyktt.jpg')
    if url_p2:
        _fill_bundled_if_missing(photos, 'preparation_team_2', url_p2, 'Специалист подготовки 2')

    url_v1 = _public_image_url('str9/vent1.jpg')
    _fill_bundled_if_missing(photos, 'ventilation_team_1', url_v1, 'Специалист вентиляции 1')
    url_v2 = _public_image_url('str9/vent2.jpg')
    _fill_bundled_if_missing(photos, 'ventilation_team_2', url_v2, 'Специалист вентиляции 2')

    url_a1 = _public_image_url('str7/photoug.jpg')
    _fill_bundled_if_missing(photos, 'audit_gallery_1', url_a1, 'Аудит инженерных систем - Работа 1')
    url_a2 = _public_image_url('str7/photoyk.jpg')
    _fill_bundled_if_missing(photos, 'audit_gallery_2', url_a2, 'Аудит инженерных систем - Работа 2')

    url_kp = _public_image_url('str7/kp.jpg')
    if url_kp:
        _fill_bundled_if_missing(photos, 'audit_kp_fallback', url_kp, 'Коммерческое предложение')

    return photos


def personal_data_policy(request):
    """Текст политики обработки ПДн (как в исходном файле, без правок)."""
    path = Path(settings.BASE_DIR) / 'static' / 'legal' / 'personal_data_policy.txt'
    try:
        policy_text = path.read_text(encoding='utf-8')
    except OSError:
        policy_text = ''
    return render(request, 'website/personal_data_policy.html', {
        'policy_text': policy_text,
    })


def index(request):
    """Главная страница"""
    context = {
        'contact_info': get_contact_info(),
        'photos': get_photos_context(),
    }
    return render(request, 'website/index.html', context)


def complex_service(request):
    """Комплексное обслуживание инженерных систем"""
    context = {
        'contact_info': get_contact_info(),
        'photos': get_photos_context(),
    }
    return render(request, 'website/complex_service.html', context)


def heating_service(request):
    """Комплексное обслуживание систем (ИТП) отопления"""
    context = {
        'contact_info': get_contact_info(),
        'photos': get_photos_context(),
    }
    return render(request, 'website/heating_service.html', context)


def verification(request):
    """Поверка приборов учёта"""
    context = {
        'contact_info': get_contact_info(),
        'photos': get_photos_context(),
    }
    return render(request, 'website/verification.html', context)


def emergency(request):
    """Аварийная служба"""
    context = {
        'contact_info': get_contact_info(),
        'photos': get_photos_context(),
    }
    return render(request, 'website/emergency.html', context)


def installation(request):
    """Монтаж инженерных коммуникаций"""
    context = {
        'contact_info': get_contact_info(),
        'photos': get_photos_context(),
    }
    return render(request, 'website/installation.html', context)


def audit(request):
    """Аудит инженерных систем"""
    # Получаем активное коммерческое предложение
    commercial_proposal = None
    try:
        commercial_proposal = CommercialProposal.objects.filter(is_active=True).first()
    except Exception as e:
        print(f"Error loading commercial proposal: {e}")
    
    context = {
        'contact_info': get_contact_info(),
        'photos': get_photos_context(),
        'commercial_proposal': commercial_proposal,
    }
    return render(request, 'website/audit.html', context)


def heating_preparation(request):
    """Подготовка к отопительному сезону"""
    context = {
        'contact_info': get_contact_info(),
        'photos': get_photos_context(),
    }
    return render(request, 'website/heating_preparation.html', context)


def ventilation(request):
    """Вентиляция"""
    context = {
        'contact_info': get_contact_info(),
        'photos': get_photos_context(),
    }
    return render(request, 'website/ventilation.html', context)


@csrf_exempt
@require_POST
def service_application(request):
    """AJAX обработчик для заявок на услуги"""
    try:
        data = json.loads(request.body)

        valid_services = {c[0] for c in ServiceApplication.SERVICE_CHOICES}
        valid_requests = {c[0] for c in ServiceApplication.REQUEST_TYPE_CHOICES}
        service_type = data.get('service_type') or 'main_page'
        if service_type not in valid_services:
            service_type = 'main_page'
        request_type = data.get('request_type') or 'application'
        if request_type not in valid_requests:
            request_type = 'application'

        phone = (data.get('phone') or '').strip()
        if not phone:
            return JsonResponse({
                'success': False,
                'message': 'Укажите телефон для связи.'
            }, status=400)

        application = ServiceApplication.objects.create(
            full_name=(data.get('full_name') or '').strip(),
            phone=phone,
            service_type=service_type,
            request_type=request_type,
            organization=data.get('organization', ''),
            message=data.get('message', ''),
            preferred_time=data.get('preferred_time', '')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Произошла ошибка при отправке заявки. Попробуйте еще раз.'
        }, status=400)


@csrf_exempt
@require_POST
def submit_request(request):
    """Обработчик для заявок с модальных окон"""
    if request.method == 'POST':
        try:
            full_name = (request.POST.get('name') or '').strip()
            phone = (request.POST.get('phone') or '').strip()
            service_type = request.POST.get('service_type', 'complex_service')
            request_type = request.POST.get('request_type', 'application')
            organization = request.POST.get('organization', '')
            message = request.POST.get('message', '')
            preferred_time = request.POST.get('preferred_time', '')
            
            if not phone:
                return JsonResponse({
                    'success': False,
                    'message': 'Укажите телефон для связи.'
                }, status=400)
            
            application = ServiceApplication.objects.create(
                full_name=full_name,
                phone=phone,
                service_type=service_type,
                request_type=request_type,
                organization=organization,
                message=message,
                preferred_time=preferred_time
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.'
            })
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Произошла ошибка при отправке заявки. Попробуйте еще раз.'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Недопустимый метод запроса.'
    }, status=405)


@csrf_exempt
@require_POST
def tender_invitation(request):
    """AJAX обработчик для приглашений в тендер"""
    try:
        # Обработка обычных полей
        full_name = (request.POST.get('full_name') or '').strip()
        phone = (request.POST.get('phone') or '').strip()
        company_name = request.POST.get('company_name', '')
        agreed_to_processing = request.POST.get('agreed_to_processing') == 'on'
        
        # Обработка файла
        technical_task = request.FILES.get('technical_task')

        if not phone:
            return JsonResponse({
                'success': False,
                'message': 'Укажите телефон для связи.'
            }, status=400)
        
        invitation = TenderInvitation.objects.create(
            full_name=full_name,
            phone=phone,
            company_name=company_name,
            technical_task=technical_task,
            agreed_to_processing=agreed_to_processing
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Приглашение в тендер успешно отправлено! Мы рассмотрим вашу заявку и свяжемся с вами.'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Произошла ошибка при отправке приглашения. Попробуйте еще раз.'
        }, status=400)


@csrf_protect
@require_POST
def submit_quote(request):
    """Обработка запроса КП для аудита"""
    try:
        name = (request.POST.get('name') or '').strip()
        phone = (request.POST.get('phone') or '').strip()
        organization = request.POST.get('organization', '')
        service_type = request.POST.get('service_type', 'audit')
        
        if not phone:
            return JsonResponse({
                'success': False,
                'message': 'Укажите телефон для связи.'
            })
        
        # Создаем запись в ServiceApplication
        application = ServiceApplication.objects.create(
            full_name=name,
            phone=phone,
            service_type=service_type,
            request_type='quote_request',
            organization=organization,
            message='Запрос коммерческого предложения'
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Заявка успешно отправлена'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Произошла ошибка при обработке заявки'
        })

