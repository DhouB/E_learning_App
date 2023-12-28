from django.urls import path, include
from rest_framework import routers
from .views import *
from . import views

#router=routers.DefaultRouter()
#router.register(r'user', UserViewSet, basename='user')
#router.register(r'StudentFeatures', StudentViewSet, basename='student_features')
#router.register(r'TutorFeatures', TutorViewSet, basename='tutor_features')
#router.register(r'AdministratorFeatures', AdministratorViewSet, basename='administrator_features')


urlpatterns = [
    #path('', include(router.urls)),
    #path('',views.SignupPage,name='signup'),
    #path('login/',views.LoginPage,name='login'),
    #path('logout/',views.LogoutPage,name='logout'),
    #path('tutor_page/', TutorViewSet.as_view(), name='tutor_page')
    #path('tutors/<int:pk>/tutor_page/', TutorViewSet.as_view({'get': 'tutor_page'}), name='tutor_page'),
    #path('tutors/<int:pk>/create_course/', TutorViewSet.as_view({'post': 'create_course'}), name='create_course'),
    #path('tutors/<int:pk>/upload_material/', TutorViewSet.as_view({'post': 'upload_material'}), name='upload_material'),
    #path('tutors/<int:pk>/create_assignment/', TutorViewSet.as_view({'post': 'create_assignment'}), name='create_assignment'),
    #path('tutors/<int:pk>/evaluate_student/', TutorViewSet.as_view({'post': 'evaluate_student'}), name='evaluate_student'),
    #path('tutors/<int:pk>/mark_absent_students/', TutorViewSet.as_view({'post': 'mark_absent_students'}), name='mark_absent_students'),
#
#
#
    #path('student/<int:pk>/student_page/', StudentViewSet.as_view({'get': 'student_page'}), name='student_page'), 
    #path('student/<int:pk>/enroll_course/', StudentViewSet.as_view({'post': 'enroll_course'}), name='enroll_course'), 
    #path('student/<int:pk>/list_course_materials/', StudentViewSet.as_view({'get': 'list_course_materials'}), name='list_course_materials'),
    #path('student/<int:pk>/enrolled_courses/', StudentViewSet.as_view({'get': 'enrolled_courses'}), name='enrolled_courses'), 
    #path('student/<int:pk>/view_grades/', StudentViewSet.as_view({'get': 'view_grades'}), name='view_grades'),   
    #path('student/<int:pk>/post_interaction_history/', StudentViewSet.as_view({'post': 'post_interaction_history'}), name='post_interaction_history'),
    #path('student/<int:pk>/track_interaction_history/', StudentViewSet.as_view({'get': 'track_interaction_history'}), name='track_interaction_history'),   
    #path('student/<int:pk>/save_reading_state/', StudentViewSet.as_view({'post': 'save_reading_state'}), name='save_reading_state'), 
]
 