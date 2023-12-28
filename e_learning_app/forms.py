from django import forms
from .models import User,ReadingState ,InteractionHistory ,Grade ,Course ,Submission,Enrollment,Material,Assignment

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'      

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = '__all__'

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = '__all__'

class InteractionHistoryForm(forms.ModelForm):
    class Meta:
        model = InteractionHistory
        fields = '__all__'

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'

class ReadingStateForm(forms.ModelForm):
    class Meta:
        model = ReadingState
        fields = '__all__'

        
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = '__all__'
