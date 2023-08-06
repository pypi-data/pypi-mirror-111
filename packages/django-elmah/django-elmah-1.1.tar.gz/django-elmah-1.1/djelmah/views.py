from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST
from tastypie.models import ApiKey
from models import DjelmahLog

# LOGS

@require_GET
def index(request):
    return HttpResponseRedirect('/djelmah/logs')

@require_GET
def log_index(request):
    hosts = DjelmahLog.objects.values_list('host', flat=True).distinct()
    logs = DjelmahLog.objects.all().order_by('-datetime')

    if request.GET:
        selected_host = request.GET.get('host', None)

        start_date = request.GET.get('start_date', None)
        start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
    
        end_date = request.GET.get('end_date', None)
        end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
    else:
        selected_host = None
        end_date = datetime.today()
        start_date = end_date - timedelta(days=30)

    if selected_host:
        logs = logs.filter(host=selected_host)

    if start_date:
        logs = logs.filter(datetime__gte=start_date)

    if end_date:
        logs = logs.filter(datetime__lte=end_date + timedelta(days=1))

    context = {
        'selected_host': selected_host,
        'start_date': start_date,
        'end_date': end_date,
        'hosts': hosts,
        'logs': logs,
    }

    return render(request, 'djelmah/logs.html', context)

@require_GET
def log_detail(request, log_id):
    log = get_object_or_404(DjelmahLog, pk=log_id)
    return HttpResponse(log.raw_html)

@require_POST
def delete_log(request):
    log_id = request.POST['log_id']
    log = get_object_or_404(DjelmahLog, pk=log_id)

    log.delete()

    return HttpResponse()

@require_GET
def log_test(request):
    raise Exception("It Works!")

# API KEYS

@require_GET
def api_keys(request):
    keys = ApiKey.objects.all().order_by('user__username')
    users = User.objects.exclude(
        id__in=keys.values_list('user_id', flat=True)
    ).order_by('last_name', 'first_name')

    context = {
        'keys': keys,
        'users': users,
    }

    return render(request, 'djelmah/keys.html', context)

@require_POST
def create_api_key(request):
    user_id = request.POST['user_id']
    user = get_object_or_404(User, pk=user_id)

    key, created = ApiKey.objects.update_or_create(
        user=user, defaults={ 'key': None }
    )

    return HttpResponse()

@require_POST
def revoke_api_key(request):
    key_id = request.POST['key_id']
    key = get_object_or_404(ApiKey, pk=key_id)

    key.delete()

    return HttpResponse()
