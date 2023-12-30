from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests

from django.conf import settings
ms_identity_web = settings.MS_IDENTITY_WEB


def index(request):
    return render(request, "auth/status.html")

def twin_view_flat(request):
    # http://localhost:8000/simple_twin_2d/twin/?scene_id=pnid1
    scene_id = request.GET.get('scene_id')
    if scene_id:
        return render(request, "simple_twin_2d/twin_view_flat.html", context={'scene_id': scene_id})
    else:
        return render(request, "simple_twin_2d/list_twins.html")
    

@ms_identity_web.login_required
def token_details(request):
    return render(request, 'auth/token.html')


@ms_identity_web.login_required
def call_ms_graph(request):
    ms_identity_web.acquire_token_silently()
    graph = 'https://graph.microsoft.com/v1.0/users'
    authZ = f'Bearer {ms_identity_web.id_data._access_token}'
    results = requests.get(graph, headers={'Authorization': authZ}).json()

    # trim the results down to 5 and format them.
    if 'value' in results:
        results ['num_results'] = len(results['value'])
        results['value'] = results['value'][:5]

    return render(request, 'auth/call-graph.html', context=dict(results=results))