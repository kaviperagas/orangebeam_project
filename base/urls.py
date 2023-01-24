from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcomePage, name="welcome"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('user-home/', views.userHome, name="user-home"),
    path('users/<str:pk>/', views.users, name="users"),
    path('create-users/', views.createUser, name="create-users"),
    path('update-users/<str:pk>/', views.updateUser, name="update-users"),
    path('delete-users/<str:pk>/', views.deleteUser, name="delete-users"),
    path('home/', views.home, name="home"),
    path('projects/<str:pk>/', views.projects, name="projects"),
    path('create-targetfloor/<str:pk>/',
         views.createTargetFloor, name="create-targetfloor"),
    path('update-targetfloor/<str:pk>/',
         views.updateTargetFloor, name="update-targetfloor"),
    path('create-actualfloor/<str:pk>/',
         views.createActualFloor, name="create-actualfloor"),
    path('update-actualfloor/<str:pk>/',
         views.updateActualFloor, name="update-actualfloor"),
    path('load-blocks/', views.load_blocks, name='load-blocks'),
    path('load-zones/', views.load_zones, name='load-zones'),
    path('load-floors/', views.load_floors, name='load-floors'),
    path('create-projects/', views.createProject, name="create-projects"),
    path('update-projects/<str:pk>/', views.updateProject, name="update-projects"),
    path('delete-projects/<str:pk>/', views.deleteProject, name="delete-projects"),
    path('menu/', views.menuPage, name="menu"),
]
