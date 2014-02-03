from django.conf.urls import patterns, include, url

from django.contrib import admin
from rest_framework import routers
from qa_api import views

admin.autodiscover()

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet)
router.register(r'questions', views.QuestionViewSet)

urlpatterns = patterns('',
    # Examples:
	# url(r'^$', 'qa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^', include(router.urls)),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
