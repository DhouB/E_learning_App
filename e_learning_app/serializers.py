from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role']
           

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    tutor = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='Tutor'), required=False)   
 
class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='Student'), required=False)     

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields ='__all__'

    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='Student'), required=False)    

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields ='__all__'
        
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='Student'), required=False)    

class InteractionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InteractionHistory
        fields = '__all__'

class ReadingStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingState
        fields = '__all__'
        
