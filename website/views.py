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
    from django.conf import settings
    from .models import Photo, GalleryPhoto
    import os
    
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
    
    # Проверяем наличие фотографий в папках media (только если нет в БД)
    media_root = settings.MEDIA_ROOT
    
    # Фотографии для главной страницы (str1) - только если нет в БД
    str1_path = os.path.join(media_root, 'str1')
    if os.path.exists(str1_path):
        for i in range(1, 5):  # photo1.jpg - photo4.jpg
            photo_file = f'photo{i}.jpg'
            photo_path = os.path.join(str1_path, photo_file)
            # Проверяем, есть ли уже фотография команды в БД
            team_key = f'main_team_{i}'
            if team_key not in photos and os.path.exists(photo_path):
                photos[f'main_str1_{i}'] = {
                    'url': f'/media/str1/{photo_file}',
                    'alt_text': f'Фото {i}'
                }
        
        # Новые фотографии для галереи в конце сайта - только если нет в БД
        for i in range(14, 18):  # photo14.jpg - photo17.jpg
            photo_file = f'photo{i}.jpg'
            photo_path = os.path.join(str1_path, photo_file)
            gallery_index = i - 13  # 1, 2, 3, 4
            gallery_key = f'main_gallery_{gallery_index}'
            if gallery_key not in photos and os.path.exists(photo_path):
                photos[gallery_key] = {
                    'url': f'/media/str1/{photo_file}',
                    'alt_text': f'Галерея фото {gallery_index}'
                }
    
    # Фотографии для страниц услуг (str2)
    str2_path = os.path.join(media_root, 'str2')
    if os.path.exists(str2_path):
        for i in range(5, 9):  # photo5.jpg - photo8.jpg
            photo_file = f'photo{i}.jpg'
            photo_path = os.path.join(str2_path, photo_file)
            if os.path.exists(photo_path):
                photos[f'service_str2_{i}'] = {
                    'url': f'/media/str2/{photo_file}',
                    'alt_text': f'Фото {i}'
                }
                # Добавляем ключи для страницы комплексного обслуживания - только если нет в БД
                complex_index = i - 4  # 1, 2, 3, 4
                complex_key = f'complex_str2_{complex_index}'
                if complex_key not in photos:
                    photos[complex_key] = {
                        'url': f'/media/str2/{photo_file}',
                        'alt_text': f'Фото {i}'
                    }
                
                # Добавляем ключи для команды комплексного обслуживания - только если нет в БД
                if i == 5:  # photo5.jpg
                    if 'complex_team_1' not in photos:
                        photos['complex_team_1'] = {
                            'url': f'/media/str2/{photo_file}',
                            'alt_text': 'Специалист 1 - Комплексное обслуживание'
                        }
                elif i == 6:  # photo6.jpg
                    if 'complex_team_2' not in photos:
                        photos['complex_team_2'] = {
                            'url': f'/media/str2/{photo_file}',
                            'alt_text': 'Специалист 2 - Комплексное обслуживание'
                        }
                elif i == 7:  # photo7.jpg
                    if 'complex_electro_1' not in photos:
                        photos['complex_electro_1'] = {
                            'url': f'/media/str2/{photo_file}',
                            'alt_text': 'Электрохозяйство 1 - Комплексное обслуживание'
                        }
                elif i == 8:  # photo8.jpg
                    if 'complex_electro_2' not in photos:
                        photos['complex_electro_2'] = {
                            'url': f'/media/str2/{photo_file}',
                            'alt_text': 'Электрохозяйство 2 - Комплексное обслуживание'
                        }
    
    # Фотографии str3
    str3_path = os.path.join(media_root, 'str3')
    if os.path.exists(str3_path):
        # photo9.jpg
        photo_file = 'photo9.jpg'
        photo_path = os.path.join(str3_path, photo_file)
        if os.path.exists(photo_path):
            photos['service_str3_9'] = {
                'url': f'/media/str3/{photo_file}',
                'alt_text': 'Фото 9'
            }
            # Добавляем ключ для страницы ИТП
            photos['heating_str3_1'] = {
                'url': f'/media/str3/{photo_file}',
                'alt_text': 'ИТП отопления'
            }
            # Добавляем ключ для команды ИТП
            photos['heating_team_1'] = {
                'url': f'/media/str3/{photo_file}',
                'alt_text': 'Команда ИТП 1'
            }
        
        # photoFF.jpg
        photo_file = 'photoFF.jpg'
        photo_path = os.path.join(str3_path, photo_file)
        if os.path.exists(photo_path):
            photos['heating_team_2'] = {
                'url': f'/media/str3/{photo_file}',
                'alt_text': 'Команда ИТП 2'
            }
        
        # Новые фотографии галереи - только если нет в БД
        # Убираем жестко заданный список файлов, чтобы не ограничивать количество фотографий
        gallery_files = ['photou', 'photop', 'photoy', 'photog']
        for i, photo_file in enumerate(gallery_files, 1):
            photo_path = os.path.join(str3_path, f'{photo_file}.jpg')
            heating_key = f'heating_gallery_{i}'
            # Проверяем, что ключ не занят фотографией из БД
            if heating_key not in photos and os.path.exists(photo_path):
                photos[heating_key] = {
                    'url': f'/media/str3/{photo_file}.jpg',
                    'alt_text': f'Работа специалистов ИТП {i}'
                }
    
    # Фотографии str4 - только если нет в БД
    str4_path = os.path.join(media_root, 'str4')
    if os.path.exists(str4_path):
        # Новые фотографии галереи поверки - только если нет в БД
        gallery_files = ['photojk', 'photopkk', 'photoub', 'photogl']
        for i, photo_file in enumerate(gallery_files, 1):
            photo_path = os.path.join(str4_path, f'{photo_file}.jpg')
            verification_key = f'verification_gallery_{i}'
            # Проверяем, что ключ не занят фотографией из БД
            if verification_key not in photos and os.path.exists(photo_path):
                photos[verification_key] = {
                    'url': f'/media/str4/{photo_file}.jpg',
                    'alt_text': f'Работа специалистов поверки {i}'
                }
    
    # Фотографии str5
    str5_path = os.path.join(media_root, 'str5')
    if os.path.exists(str5_path):
        for i in range(10, 14):  # photo10.jpg - photo13.jpg
            photo_file = f'photo{i}.jpg'
            photo_path = os.path.join(str5_path, photo_file)
            if os.path.exists(photo_path):
                photos[f'service_str5_{i}'] = {
                    'url': f'/media/str5/{photo_file}',
                    'alt_text': f'Фото {i}'
                }
                # Добавляем ключи для галереи аварийной службы
                gallery_index = i - 9  # 1, 2, 3, 4
                photos[f'emergency_gallery_{gallery_index}'] = {
                    'url': f'/media/str5/{photo_file}',
                    'alt_text': f'Аварийная служба фото {gallery_index}'
                }
    
    # Фотографии str8
    str8_path = os.path.join(media_root, 'str8')
    if os.path.exists(str8_path):
        # photougtt.jpg
        photo_file = 'photougtt.jpg'
        photo_path = os.path.join(str8_path, photo_file)
        if os.path.exists(photo_path):
            photos['preparation_team_1'] = {
                'url': f'/media/str8/{photo_file}',
                'alt_text': 'Специалист подготовки 1'
            }
        
        # photoyktt.jpg
        photo_file = 'photoyktt.jpg'
        photo_path = os.path.join(str8_path, photo_file)
        if os.path.exists(photo_path):
            photos['preparation_team_2'] = {
                'url': f'/media/str8/{photo_file}',
                'alt_text': 'Специалист подготовки 2'
            }
    
    # Фотографии str9
    str9_path = os.path.join(media_root, 'str9')
    if os.path.exists(str9_path):
        # vent1.jpg - только если нет в БД
        photo_file = 'vent1.jpg'
        photo_path = os.path.join(str9_path, photo_file)
        if 'ventilation_team_1' not in photos and os.path.exists(photo_path):
            photos['ventilation_team_1'] = {
                'url': f'/media/str9/{photo_file}',
                'alt_text': 'Специалист вентиляции 1'
            }
        
        # vent2.jpg - только если нет в БД
        photo_file = 'vent2.jpg'
        photo_path = os.path.join(str9_path, photo_file)
        if 'ventilation_team_2' not in photos and os.path.exists(photo_path):
            photos['ventilation_team_2'] = {
                'url': f'/media/str9/{photo_file}',
                'alt_text': 'Специалист вентиляции 2'
            }
    
    # Фотографии для галереи аудита (str7)
    str7_path = os.path.join(media_root, 'str7')
    if os.path.exists(str7_path):
        # photoug.jpg - только если нет в БД
        photo_file = 'photoug.jpg'
        photo_path = os.path.join(str7_path, photo_file)
        if 'audit_gallery_1' not in photos and os.path.exists(photo_path):
            photos['audit_gallery_1'] = {
                'url': f'/media/str7/{photo_file}',
                'alt_text': 'Аудит инженерных систем - Работа 1'
            }
        
        # photoyk.jpg - только если нет в БД
        photo_file = 'photoyk.jpg'
        photo_path = os.path.join(str7_path, photo_file)
        if 'audit_gallery_2' not in photos and os.path.exists(photo_path):
            photos['audit_gallery_2'] = {
                'url': f'/media/str7/{photo_file}',
                'alt_text': 'Аудит инженерных систем - Работа 2'
            }
    
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

        application = ServiceApplication.objects.create(
            full_name=data.get('full_name', ''),
            phone=data.get('phone', ''),
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
            full_name = request.POST.get('name', '')
            phone = request.POST.get('phone', '')
            service_type = request.POST.get('service_type', 'complex_service')
            request_type = request.POST.get('request_type', 'application')
            organization = request.POST.get('organization', '')
            message = request.POST.get('message', '')
            preferred_time = request.POST.get('preferred_time', '')
            
            if not full_name or not phone:
                return JsonResponse({
                    'success': False,
                    'message': 'Пожалуйста, заполните все обязательные поля.'
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
        full_name = request.POST.get('full_name', '')
        phone = request.POST.get('phone', '')
        company_name = request.POST.get('company_name', '')
        agreed_to_processing = request.POST.get('agreed_to_processing') == 'on'
        
        # Обработка файла
        technical_task = request.FILES.get('technical_task')
        
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
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        organization = request.POST.get('organization', '')
        service_type = request.POST.get('service_type', 'audit')
        
        if not all([name, phone]):
            return JsonResponse({
                'success': False,
                'message': 'Имя и телефон обязательны для заполнения'
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

