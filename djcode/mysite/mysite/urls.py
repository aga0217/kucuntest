from django.conf.urls import *
from django.contrib.auth.views import login,logout
from django.contrib.auth.decorators import login_required, permission_required
from views import *
from django.contrib import admin
from kucuntest.views import *
from django.conf import settings
from django.conf.urls.static import static


from django.views.generic import TemplateView
admin.autodiscover()


urlpatterns = patterns('',

    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout_view),
    url(r'^hello/$', hello),
    url(r'^demo/$', 'kucuntest.views.demo'),
    url(r'^time/$',cur_datetime),
    url(r'^time/plus/(\d{1,2})/$',hours_ahead),
    url(r'^templatetest/$',template_test),
    #url(r'^home/$', 'kucuntest.views.home'),
    #url(r'^mulu/$', 'kucuntest.views.mulu'),
    url(r'^gongyingshang/addgongyingshang/$', 'kucuntest.views.addgongyingshang'),
    url(r'^gongyingshang/editgongyingshang/(\d{1,3})/$', 'kucuntest.views.editgongyingshang'),
    url(r'^gongyingshang/editgongyingshangname/(\d{1,3})/$', 'kucuntest.views.editgongyingshangname'),
    url(r'^gongyingshang/gongyingshanglist/$', gongyingshanglist.as_view()),
    url(r'^pinlei/addpinlei/$', 'kucuntest.views.addpinlei'),
    url(r'^pinlei/pinleilist/$', pinleilist.as_view()),
    url(r'^pinlei/editpinlei/(\d{1,3})/$', 'kucuntest.views.editpinlei'),
    url(r'^hetong/addhetong/$', 'kucuntest.views.addhetong'),
    url(r'^hetong/hetonglist/$', hetonglist.as_view()),
    url(r'^hetong/edithetong/(?P<hetongno>[\.\w-]+)/$','kucuntest.views.edithetong'),
    url(r'^churuku/churukulist/(?P<hetongno>[\.\w-]+)/$', churukulist.as_view()),
    #url(r'^churuku/addchuruku/$' , 'kucuntest.views.addchurukumx'),
    url(r'^churuku/addchuruku/(?P<hetongno>[\.\w-]+)/$' , 'kucuntest.views.addchurukumx'),
    url(r'^churuku/editchuruku/(\d{1,3})/$', 'kucuntest.views.editchuruku'),
    url(r'^kucun/kucunlist/$', kucunlist.as_view()),
    #url(r'^churuku/editchuruku/(\d{1,3})/$' , 'kucuntest.views.editchuruku'),
    url(r'^fukuan/addfukuanmx/(?P<hetongno>[\.\w-]+)/$', 'kucuntest.views.addfukuanmx'),

    url(r'^fukuan/fukuangllist/$', fukuangllist.as_view()),
    url(r'^fukuan/fukuanmxlist/(?P<hetongno>[\.\w-]+)/$', fukuanmxlist.as_view()),
    url(r'^fukuan/editfukuanmx/(\d{1,3})/$', 'kucuntest.views.editfukuanmx'),
    url(r'^todo/createtodo/$', 'kucuntest.views.TodoCreate'),
    url(r'^todo/todolist/$', TodoList.as_view()),
    url(r'^todo/edittodo/(\d{1,3})/$', 'kucuntest.views.edittodo'),
    #url(r'^churukusearchlist/$', churukusearchlist.as_view()),
    #url(r'^churukusearchlist/$', churukusearchlist.as_view()),
    #url(r'^caozuochenggong/(\d{1})/$', 'kucuntest.views.caozuochenggong'),







    url(r'^admin/', include(admin.site.urls)),

    
)
static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
