from django.urls import path
from users import api

urlpatterns = [ 
    path('create/', api.CreateUserView.as_view(), name='create'),
    path('token/', api.CreateTokenView.as_view(), name='token'),
    path('user/', api.RetrieveUpdateUserView.as_view(), name='user'),
    path('logout/', api.LogoutView.as_view(), name='logout'),
]




