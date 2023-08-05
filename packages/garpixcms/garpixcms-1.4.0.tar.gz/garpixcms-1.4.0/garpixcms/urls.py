from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.i18n import i18n_patterns
from garpix_page.views.page import PageView
from multiurl import ContinueResolving, multiurl
from django.http import Http404
from django.conf import settings
from garpix_auth.views import LogoutView, LoginView
from garpix_auth.rest.obtain_auth_token import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.ENABLE_GARPIX_AUTH:
    urlpatterns += [
        path('logout/', LogoutView.as_view(url='/'), name="logout"),
        path('login/', LoginView.as_view(), name="authorize"),
        path('token-auth/', obtain_auth_token),
    ]

urlpatterns += i18n_patterns(
    multiurl(
        path('', PageView.as_view()),
        re_path(r'^(?P<url>.*?)$', PageView.as_view(), name='page'),
        re_path(r'^(?P<url>.*?)/$', PageView.as_view(), name='page'),
        catch=(Http404, ContinueResolving),
    ),
    prefix_default_language=settings.USE_DEFAULT_LANGUAGE_PREFIX,
)
