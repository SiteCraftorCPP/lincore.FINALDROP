from pathlib import Path

from django.conf import settings
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

    # Слайдер ИТП/ЦТП — только GalleryPhoto (heating_gallery_*), см. «Галерея … ИТП …» в админке.

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

