from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import yaml
import json

import connections.azureblob as azb
import connections.cmdbgraph as cmdb

from django.conf import settings
import json
ms_identity_web = settings.MS_IDENTITY_WEB

flat_3d_scene_config = yaml.safe_load(open(f"./simple_twin_2d/configurations/flat_3d_scene.yml"))

def index(request):
    context = {'available_properties':flat_3d_scene_config['search_properties']['available_properties']}
    return render(request, "simple_twin_2d/home_search.html", context)

def search(request):
    formData = json.loads(request.body.decode("utf-8"))
    context = {'formData': formData}
    
    return HttpResponse(json.dumps(context), content_type="application/json")
    

def default_statics(context):
    # appends common static files to context. Takes a dict and returns a dict. 
    context['css_page'] = azb.fetch_sas_url("simple_twin_2d.css")
    context['favicon'] = azb.fetch_sas_url("favicon.ico")
    return context

# TODO: Skipping ms_auth for the demo. Will need to add it back in.
# @ms_identity_web.login_required
def twin_view_flat_3d(request):
    # http://localhost:8000/simple_twin_2d/3d/twin/?boundary_id=boundary17529430240082
    boundary_id = request.GET.get('boundary_id')
    gui_on_off = request.GET.get('gui','off')
    context = default_statics({'gui':gui_on_off})
    context['scene_config'] = flat_3d_scene_config['rendering']
    if boundary_id:
        context['boundary_id']=boundary_id
        # `data` and `asset` are pulled from the graph.
        # TODO: cmdb and other connectors should reverence the other module to keep this view generic
        # cmdb and azb are hard coded here for simplicity.
        c = cmdb.CosmosdbClient()
        context['data'] = c.collect_anchors(boundary_id)
        context['asset'] = c.collect_asset(boundary_id)
        # The path for the background asset is in the flat_3d_scene_config.yml file. 
        context['background_asset_sas']=azb.fetch_sas_url(f"{context['asset'][0]['objects'][1][flat_3d_scene_config['node_context']['asset_path']][0]}")
        return render(request, "simple_twin_2d/twin_view_flat_3d.html", context)
    else:
        return render(request, "simple_twin_2d/list_twins.html")


# TODO: Skipping ms_auth for the demo. Will need to add it back in.
# @ms_identity_web.login_required
def twin_view_flat_2d(request):
    # http://localhost:8000/simple_twin_2d/2d/twin/?boundary_id=boundary17529430240082
    c = cmdb.CosmosdbClient()
    boundary_id = request.GET.get('boundary_id')
    context = default_statics({})
    context['scene_config'] = flat_3d_scene_config['rendering']
    if boundary_id:
        context['data'] = c.collect_anchors(boundary_id)
        context['asset'] = c.collect_asset(boundary_id)
        context['boundary_id']=boundary_id
        context['background_asset_sas']=azb.fetch_sas_url(f"{context['asset'][0]['objects'][1][flat_3d_scene_config['node_context']['asset_path']][0]}")

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