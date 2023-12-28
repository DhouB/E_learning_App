"""
URL configuration for ds2_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from e_learning_app.views import *
from e_learning_app import views


urlpatterns = [
    #path('', index, name='index'),
    path('signup', signup, name='signup'),
    path('', login, name='login'),
    #path('index/', login, name='index'),

    path('<int:pk>/student_page/', StudentViewSet.as_view({'get': 'student_page'}), name='student_page'),
    path('enroll_course/<int:pk>/', StudentViewSet.as_view({'post': 'enroll_course'}), name='enroll_course'),
    path('submit_assignment/<int:pk>/', StudentViewSet.as_view({'post': 'submit_assignment'}), name='submit_assignment'),
    path('list_course_materials/<int:pk>/', StudentViewSet.as_view({'get': 'list_course_materials'}), name='list_course_materials'),
    path('enrolled_courses/<int:pk>/', StudentViewSet.as_view({'get': 'enrolled_courses'}), name='enrolled_courses'), 
    path('view_grades/<int:pk>/', StudentViewSet.as_view({'get': 'view_grades'}), name='view_grades'),   
    path('post_interaction_history/<int:pk>/', StudentViewSet.as_view({'post': 'post_interaction_history'}), name='post_interaction_history'),
    path('track_interaction_history/<int:pk>/', StudentViewSet.as_view({'get': 'track_interaction_history'}), name='track_interaction_history'),   
    path('save_reading_state/<int:pk>/', StudentViewSet.as_view({'post': 'save_reading_state'}), name='save_reading_state'),


    path('<int:pk>/tutor_page/', TutorViewSet.as_view({'get': 'tutor_page'}), name='tutor_page'),
    path('create_course/<int:pk>/', TutorViewSet.as_view({'post': 'create_course'}), name='create_course'),
    path('upload_material/<int:pk>/', TutorViewSet.as_view({'post': 'upload_material'}), name='upload_material'),
    path('create_assignment/<int:pk>/', TutorViewSet.as_view({'post': 'create_assignment'}), name='create_assignment'),
    path('evaluate_student/<int:pk>/', TutorViewSet.as_view({'post': 'evaluate_student'}), name='evaluate_student'),
    path('mark_absent_students/<int:pk>/', TutorViewSet.as_view({'post': 'mark_absent_students'}), name='mark_absent_students'),


    path('<int:pk>/admin_page/', AdministratorViewSet.as_view({'get': 'admin_page'}), name='admin_page'),
    path('monitor_enrollments/<int:pk>/', AdministratorViewSet.as_view({'get': 'monitor_enrollments'}), name='monitor_enrollments'),
    path('monitor_submissions/<int:pk>/', AdministratorViewSet.as_view({'get': 'monitor_submissions'}), name='monitor_submissions'),
    path('monitor_interaction_history/<int:pk>/', AdministratorViewSet.as_view({'get': 'monitor_interaction_history'}), name='monitor_interaction_history'),
    path('user_list/<int:pk>/', AdministratorViewSet.as_view({'get': 'user_list'}), name='user_list'),
    path('user_edit/<int:pk>/', AdministratorViewSet.as_view({'post': 'user_edit'}), name='user_edit'),
    path('user_delete/<int:pk>/', AdministratorViewSet.as_view({'post': 'user_delete'}), name='user_delete'),
    path('manage_grade/<int:pk>/', AdministratorViewSet.as_view({'post': 'manage_grade'}), name='manage_grade'),
]
