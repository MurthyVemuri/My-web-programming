from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('' ,
	url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'login.views.index'),
    url(r'^accounts/login/', 'login.views.login'),
    url(r'^accounts/game/', 'login.views.game'),
    url(r'^accounts/auth/' , 'login.views.auth_view'),
    url(r'^accounts/logout/' , 'login.views.logout'),
    url(r'^accounts/loggedin/', 'login.views.loggedin' , name='loggedin'),
    url(r'^accounts/invalid/' , 'login.views.invalied_login'),
    url(r'^accounts/start_game/$', 'login.views.start_game'),
    url(r'^accounts/play/$', 'login.views.play'),
    url(r'^accounts/success/$', 'login.views.success'),
    url(r'^accounts/register/' , 'login.views.register_user'),
    url(r'^accounts/register_sucesss/' , 'login.views.register_sucesss'),
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
