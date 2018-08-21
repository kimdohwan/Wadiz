from django.urls import path

from .. import apis

app_name = 'user'

urlpatterns = [
    path('', apis.UserList.as_view()),
    path('signin/', apis.AuthToken.as_view()),
    path('detail/<int:pk>/', apis.UserDetail.as_view()),
    path('signup/', apis.UserList.as_view(), name='signup'),
    path('activate/<str:uidb64>/<str:token>/', apis.UserActivate.as_view(), name='activate'),
    path('change-info/', apis.UserDetail.as_view()),
    path('myinfo/', apis.UserInfo.as_view()),
]
