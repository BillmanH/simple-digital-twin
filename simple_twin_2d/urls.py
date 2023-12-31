from django.urls import path, include
from . import views
from django.conf.urls.static import static

from ms_identity_web.django.msal_views_and_urls import MsalViews
from django.conf import settings
msal_urls = MsalViews(settings.MS_IDENTITY_WEB).url_patterns()


urlpatterns = [
    # Root
    path('', views.index, name='index'),

    # Twin Views
    # path('/list_twins/', views.list_twins, name='list_twins'),
    path('simple_twin_2d/2d/twin/', views.twin_view_flat_2d, name='twin_view_flat_2d'),
    path('simple_twin_2d/3d/twin/', views.twin_view_flat_2d, name='twin_view_flat_3d'),

    # Generic AAD Tests, not needed in production application
    path('token_details', views.token_details, name='token_details'),
    path('sign_in_status', views.index, name='status'),
    path(f'{settings.AAD_CONFIG.django.auth_endpoints.prefix}/', include(msal_urls)),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]