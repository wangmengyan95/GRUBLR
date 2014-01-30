from django.conf.urls import patterns, include, url
from Main.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Part2.views.home', name='home'),
    # url(r'^Part2/', include('Part2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login),
    url(r'^login$', login),
    url(r'^register',register),
    url(r'^home/$', home),
    url(r'^checkRegisterForm$',checkRegisterForm),
    url(r'^profile',profile),
    url(r'^editProfileForm',editProfileForm),
    url(r'^getProfile',getProfile),
    url(r'^personalPage/(.+)/$',personalPage),
    url(r'^logout$',logout),
    url(r'^thumbUpGrumblr/$',thumbUpGrumblr),
    url(r'^relationship/([A-Za-z]+)/$',relationship),
    url(r'^followFriend/$',followFriend),
    url(r'^blockUser/$',blockUser),
    url(r'^deBlockUser/$',deBlockUser),
    url(r'^deFollowFriend/$',deFollowFriend),
    url(r'^getAvatar/(.+)$', getAvatar, name='getAvatar'),
    url(r'^getSelfAvatar/$', getSelfAvatar),
    url(r'^getGrumblrImage/(.+)$', getGrumblrImage, name='getGrumblrImage'),
    url(r'^searchGrumblr/$',searchGrumblr),
    url(r'^home/postGrumblrComment/$',postGrumblrComment),
    url(r'^home/getGrumblrComment/$',getGrumblrComment),
    url(r'^home/postGrumblr/$', postGrumblr),
    url(r'^home/([A-Za-z]+)/$',selectCertainGrumblar),
    url(r'^refreshGrumblrList/$',refreshGrumblrList),
    url(r'^changePassword/$',changePassword),
    url(r'^findPassword/$',findPassword),
)
