from django.urls import path
from .views import (
        home, 
        room, 
        roomCreate, 
        roomUpdate, 
        roomDelete, 
        loginPage, 
        logoutUser, 
        registerUser, 
        deleteMessage,
        userProfile,
        updateUser,
        topicsPage,
        activityPage
    )


urlpatterns = [
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', registerUser, name='register'),
    path('profile/<str:pk>/', userProfile, name='user-profile'),
    path('update-user/', updateUser, name='update-user'),
    path('topics/', topicsPage, name='topics'),
    path('activity/', activityPage, name='activity'),

    path('', home, name='home'),
    path('create/', roomCreate, name='room-create'),
    path('<str:pk>/update/', roomUpdate, name='room-update'),
    path('room_delete/<str:pk>/', roomDelete, name='room-delete'),
    path('message_delete/<str:pk>/', deleteMessage, name='message-delete'),
    path('room/<str:pk>/', room, name='room')
]
