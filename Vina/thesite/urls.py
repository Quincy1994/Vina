__author__ = 'fen'
from django.conf.urls import patterns, url
from thesite.views import login, figure, register, index, details, logout, helppage, redirect, datasample, datasamplea, datasampleb, datasamplec, datasampled, datasamplee,tyr


urlpatterns = patterns('',
                       url(r'^$', login, name="login"),
                       url(r'^login', login, name='login'),
                       url(r'^logout', logout, name='logout'),
                       url(r'^index', index, name='index'),
                       url(r'^register/$', register, name='register'),
                       url(r'^help/$', helppage, name='help'),
                       url(r'^redirect/$', redirect, name='redirect'),
                       url(r'^figure/$', figure, name='figure'),
                       url(r'^datasample/$', datasample, name='datasample'),
                       url(r'^downloada/$', datasamplea, name='datasamplea'),
                       url(r'^downloadb/$', datasampleb, name='datasampleb'),
                       url(r'^downloadc/$', datasamplec, name='datasamplec'),
                       url(r'^downloadd/$', datasampled, name='datasampled'),
                       url(r'^downloade/$', datasamplee, name='datasamplee'),
                       url(r'^details/$', details, name='details'),
                       url(r'^tyr/$',tyr,name='tyr'))