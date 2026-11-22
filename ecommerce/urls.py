from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('admin/', include('ecommerce.admin.urls')),
    path('account/', include('ecommerce.accounts.urls')),
    path('',include('ecommerce.ui.urls')),
    path('payments/',include('ecommerce.payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # In production DEBUG=False, Django does not serve MEDIA_URL automatically.
    # WhiteNoise serves /static/; uploaded media on the persistent disk must be
    # served explicitly via this view.
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),
    ]