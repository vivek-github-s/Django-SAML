from django.shortcuts import redirect
from django.http import JsonResponse
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

def prepare_django_request(request):
    return {
        'http_host': request.get_host(),
        'server_port': request.META['SERVER_PORT'],
        'script_name': request.path,
        'get_data': request.GET.copy(),
        'post_data': request.POST.copy(),
    }
@csrf_exempt
def saml_login(request):
    req = prepare_django_request(request)
    auth = OneLogin_Saml2_Auth(req, settings.SAML_SETTINGS)
    return redirect(auth.login())
@csrf_exempt
def saml_callback(request):
    req = prepare_django_request(request)
    auth = OneLogin_Saml2_Auth(req, settings.SAML_SETTINGS)
    auth.process_response()

    errors = auth.get_errors()
    if not errors:
        if auth.is_authenticated():
            name_id = auth.get_nameid()
            attributes = auth.get_attributes()
            permissions = {key.replace("Permisison.", ""): value for key, value in attributes.items() if key.startswith("Permisison.")}
            return JsonResponse({"name_id": name_id, "attributes": attributes, "Permission":permissions})  # Modify as needed
        else:
            return JsonResponse({"error": "User not authenticated"}, status=401)
    else:
        return JsonResponse({"error": "SAML Response processing error", "details": auth.get_last_error_reason()}, status=400)
