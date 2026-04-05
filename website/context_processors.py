from .models import ContactInfo


def contact_info(request):
    try:
        info = ContactInfo.objects.first()
        if info is not None:
            return {'contact_info': info}
    except Exception:
        pass
    return {'contact_info': ContactInfo()}
