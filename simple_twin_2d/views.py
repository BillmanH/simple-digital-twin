from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import yaml

import connections.azureblob as azb
import connections.cmdbgraph as cmdb

from django.conf import settings
ms_identity_web = settings.MS_IDENTITY_WEB


def index(request):
    return render(request, "auth/status.html")

def default_statics(context):
    # appends common static files to context. Takes a dict and returns a dict. 
    context['css_page'] = azb.fetch_sas_url("simple_twin_2d.css")
    context['favicon'] = azb.fetch_sas_url("favicon.ico")
    return context

def twin_view_flat_3d(request):
    c = cmdb.CosmosdbClient()
    # http://localhost:8000/simple_twin_2d/3d/twin/?boundary_id=boundary17529430240082
    scene_id = request.GET.get('boundary_id')
    context = default_statics({})
    if scene_id:
        context['scene_id']=scene_id
        context['data'] = c.collect_anchors(scene_id)
        context['asset'] = c.collect_asset(scene_id)
        print(context['asset'])
        context['background_asset_sas']=azb.fetch_sas_url(f"{context['asset'][3]}")
        # scene_config = yaml.safe_load(open(f"./simple_twin_2d/configurations/{scene_id}.yml"))
        # context['scene_config'] = scene_config
        return render(request, "simple_twin_2d/twin_view_flat_3d.html", context)
    else:
        return render(request, "simple_twin_2d/list_twins.html")

def twin_view_flat_2d(request):
    # http://localhost:8000/simple_twin_2d/2d/twin/?boundary_id=boundary17529430240082
    c = cmdb.CosmosdbClient()
    scene_id = request.GET.get('boundary_id')
    context = default_statics({})
    if scene_id:
        context['data'] = c.collect_anchors(scene_id)
        context['asset'] = c.collect_asset(scene_id)
        context['scene_id']=scene_id
        context['background_asset_sas']=azb.fetch_sas_url(f"{context['asset'][3]}")
        # scene_config = yaml.safe_load(open(f"./simple_twin_2d/configurations/{scene_id}.yml"))
        # context['scene_config'] = scene_config
        return render(request, "simple_twin_2d/twin_view_flat_2d.html", context)
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