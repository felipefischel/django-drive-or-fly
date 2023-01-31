from django.urls import path, include

from . import views

app_name = 'comparison'

urlpatterns =[
  path('',views.Index, name='index'),
  path('about/',views.About, name='about'),
  path('result/<int:trip_output_id>', views.Result, name='result'),
  path('compare/',views.Compare,name='compare'),
  path('autocomplete/', views.autocomplete, name="autocomplete")
  ]
