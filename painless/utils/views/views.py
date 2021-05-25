from django.shortcuts import render
from django.http import HttpResponse


def page_robots(request):
    lines = [
        "User-agent: *",
        "Disallow: /",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def page_not_found(request, exception, template_name='errors/HTTP404.html'):
    return render(request, template_name, status=404)


def server_error(request, template_name='errors/HTTP500.html'):
    return render(request, template_name, status=500)


def permission_denied(request, exception, template_name='errors/HTTP403.html'):
    return render(request, template_name, status=403)
