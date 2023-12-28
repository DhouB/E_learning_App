from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Course, Enrollment, Material, Assignment, Submission, Grade, InteractionHistory, ReadingState
from .serializers import UserSerializer, CourseSerializer, EnrollmentSerializer, MaterialSerializer, AssignmentSerializer, SubmissionSerializer, GradeSerializer, InteractionHistorySerializer, ReadingStateSerializer
from django.shortcuts import get_object_or_404 , render
from django.core.exceptions import ObjectDoesNotExist
from twilio.rest import Client
import logging
from twilio.twiml.voice_response import VoiceResponse
from .forms import *

from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse

from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        # Get user details from the form
        role = request.POST.get('role', 'Student')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')

        # Hash the password
        hashed_password = make_password(password)

        # Create a new user
        user = User(role=role, username=username, password=hashed_password, email=email, date_joined=timezone.now())
        user.save()

        # Redirect to login page or another page after successful signup
        return redirect('login')

    # Render the signup form
    return render(request, 'signup.html')



def login(request):
    if request.method == 'POST':
        # Get login credentials from the form
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # Find the user in the database
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # User not found
            return render(request, 'login.html', {'error': 'Invalid username or password'})

        # Check if the entered password matches the hashed password
        if check_password(password, user.password):
            # Successful login
            if user.role == 'Student':
                student_page_url = reverse('student_page', kwargs={'pk': user.pk})
                return redirect(student_page_url)  # Redirect to the student page
            elif user.role == 'Tutor':
                tutor_page_url = reverse('tutor_page', kwargs={'pk': user.pk})
                return redirect(tutor_page_url)  # Redirect to the tutor page
            elif user.role == 'Administrator':
                admin_page_url = reverse('admin_page', kwargs={'pk': user.pk})
                return redirect(admin_page_url)  # Redirect to the tutor page
        else:
            # Incorrect password
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    # Render the login form
    return render(request, 'login.html')



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Redirect to the login page after successful registration
            login_url = reverse('login')  # Adjust 'login' to the actual URL name for your login page
            return redirect(login_url)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

        
    @action(methods=['post'], detail=False)
    def login_user(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        # Fetch the user by email
        user = User.objects.filter(email=email).first()

        if user and user.password == password:
            # Manually set user session
            request.session['email'] = user.id

            # You can return additional data or a success message
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)



    @action(methods=['post'], detail=False)
    def logout_user(self, request):
        # Manually clear the user's session
        request.session.flush()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    


    @action(methods=['get'], detail=False)
    def user_list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({'users': serializer.data})
   


    @action(methods=['post'], detail=False)
    def user_detail(self, request):
        email = request.data.get('email')

        if email is None:
            return Response({'message': 'User email not provided'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, email=email)
        serializer = UserSerializer(user)
        return Response({'user': serializer.data})
    



    @action(methods=['post'], detail=False)
    def user_edit(self, request):
        email = request.data.get('email')
        if email is None:
            return Response({'message': 'User email not provided'}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'POST':
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'user': serializer.data})
            else:
                return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user)
        return Response({'serializer': serializer.data})




    @action(methods=['post'], detail=False)
    def user_delete(self, request):
        email = request.data.get('email')
        if email is None:
            return Response({'message': 'User email not provided'}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

#tutor
    @action(detail=True, methods=['post'])
    def add_material(self, request, pk=None):
        course = self.get_object()
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
#administrator
    @action(detail=True, methods=['delete'])
    def remove_student(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student')

        try:
            enrollment = Enrollment.objects.get(course=course, student__id=student_id)
            enrollment.delete()
            return Response({"detail": "Student removed from the course."})
        except Enrollment.DoesNotExist:
            return Response({"detail": "Student not found in the course."}, status=404)



class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer




class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    #for student
    @action(detail=True, methods=['get'])
    def get_reading_state(self, request, pk=None):
        material = self.get_object()
        student = request.user
        try:
            reading_state = ReadingState.objects.get(student=student, material=material)
            serializer = ReadingStateSerializer(reading_state)
            return Response(serializer.data)
        except ReadingState.DoesNotExist:
            return Response({"detail": "Reading state not found."}, status=404)



    @action(detail=True, methods=['post'])
    def update_reading_state(self, request, pk=None):
        material = self.get_object()
        student = request.user
        serializer = ReadingStateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=student, material=material)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


# for tutor
    @action(detail=True, methods=['post'])
    def evaluate_submission(self, request, pk=None):
        assignment = self.get_object()
        submission_id = request.data.get('submission')
        grade_data = {
            'student': Submission.objects.get(id=submission_id).student,
            'assignment': assignment,
            'grade': request.data.get('grade'),
            'feedback': request.data.get('feedback'),
        }
        grade_serializer = GradeSerializer(data=grade_data)
        if grade_serializer.is_valid():
            grade_serializer.save()
            return Response(grade_serializer.data)
        return Response(grade_serializer.errors, status=400)
    

#for student
    @action(detail=True, methods=['get'])
    def get_submission(self, request, pk=None):
        assignment = self.get_object()
        student = request.user
        try:
            submission = Submission.objects.get(assignment=assignment, student=student)
            serializer = SubmissionSerializer(submission)
            return Response(serializer.data)
        except Submission.DoesNotExist:
            return Response({"detail": "Submission not found."}, status=404)


    @action(detail=True, methods=['post'])
    def submit_assignment(self, request, pk=None):
        assignment = self.get_object()
        student = request.user
        serializer = SubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=student, assignment=assignment)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)




class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    #permission_classes = [IsStudent]

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    #permission_classes = [IsTutor]

class InteractionHistoryViewSet(viewsets.ModelViewSet):
    queryset = InteractionHistory.objects.all()
    serializer_class = InteractionHistorySerializer
    #permission_classes = [IsStudent]

class ReadingStateViewSet(viewsets.ModelViewSet):
    queryset = ReadingState.objects.all()
    serializer_class = ReadingStateSerializer
    #permission_classes = [IsStudent]




class StudentViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role="Student")
    serializer_class = UserSerializer
    template_name = 'student_page.html'

    @action(detail=False, methods=['get'])
    def student_page(self, request, pk=None):
        student = self.get_object()
        context = {
            'student': student,
            'all_courses': Course.objects.all(),
            'all_enrollments': Enrollment.objects.all(),
            'all_materials': Material.objects.all(),
            'all_grades': Grade.objects.all(),
            'all_interactions': InteractionHistory.objects.all(),
            'all_assignments': Assignment.objects.all(),
            'all_readingstate': ReadingState.objects.all(),
        }
        return render(request, self.template_name, context)
    
#enroll course
    @action(detail=True, methods=['post'])
    def enroll_course(self, request, pk=None):
        student = self.get_object()
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=student)
            student_page_url = reverse('student_page', kwargs={'pk': student.pk})
            return redirect(student_page_url)  # Redirect to the tutor page
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#enrolled course
    @action(detail=True, methods=['get'])
    def enrolled_courses(self, request, pk=None):
        student = self.get_object()
        enrollments = Enrollment.objects.filter(student=student)
        serializer = EnrollmentSerializer(enrollments, many=True)
        context = {'enrollments': serializer.data}
        return render(request, 'student_page.html', context)
    

#liste course
    @action(detail=True, methods=['get'])
    def list_course_materials(self, request, pk=None):
        student = self.get_object()

        enrollments = student.enrollments.all()

        materials = Material.objects.filter(course__in=enrollments.values_list('course', flat=True))
        serializer = MaterialSerializer(materials, many=True)
        context = {'materials': serializer.data}
        return render(request, 'student_page.html', context)
        
#submit assignment
    @action(detail=True, methods=['post'])
    def submit_assignment(self, request, pk=None):
        student = self.get_object()
        serializer = SubmissionSerializer(data=request.data)

        if serializer.is_valid():
            # Ensure that the student is enrolled in the course related to the assignment
            assignment = serializer.validated_data.get('assignment')
            if not Enrollment.objects.filter(student=student, course=assignment.course).exists():
                    return render(request, 'student_page.html', {'error': 'Student not enroled in the course'})

            # Save the submission with the associated student
            serializer.save(student=student)
            # Get the URL for the student_page view and include the student's pk
            student_page_url = reverse('student_page', kwargs={'pk': student.pk})
            return redirect(student_page_url)  # Redirect to the tutor page
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#view grades
    @action(detail=True, methods=['get'])
    def view_grades(self, request, pk=None):
        student = self.get_object()

        # Get submissions for the student
        submissions = Submission.objects.filter(student=student)

        # Retrieve grades and feedback for the submitted assignments
        grades = Grade.objects.filter(student=student, assignment__in=submissions.values_list('assignment', flat=True))
        serializer = GradeSerializer(grades, many=True)
        context = {'grades': serializer.data}
        return render(request, 'student_page.html', context)
    
#post interaction
    @action(detail=True, methods=['post'])
    def post_interaction_history(self, request, pk=None):
        student = self.get_object()
        serializer = InteractionHistorySerializer(data=request.data)

        if serializer.is_valid():
            # Ensure that the student is enrolled in the course related to the material
            material = serializer.validated_data.get('material')
            if not Enrollment.objects.filter(student=student, course=material.course).exists():
                    return render(request, 'student_page.html', {'error': 'Student not enroled in the course'})

            # Save the interaction history with the associated student
            serializer.save(student=student)
            # Get the URL for the student_page view and include the student's pk
            student_page_url = reverse('student_page', kwargs={'pk': student.pk})
            return redirect(student_page_url)  # Redirect to the student_page with the student's pk

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#track interaction
    @action(detail=True, methods=['get'])
    def track_interaction_history(self, request, pk=None):
        student = self.get_object()

        # Get interaction history for the student
        interaction_history = InteractionHistory.objects.filter(student=student)
        serializer = InteractionHistorySerializer(interaction_history, many=True)
        context = {'interaction_history': serializer.data}
        return render(request, 'student_page.html', context)
        #return Response(serializer.data)
#save reading state
    @action(detail=True, methods=['post'])
    def save_reading_state(self, request, pk=None):
        student = self.get_object()
        serializer = ReadingStateSerializer(data=request.data)

        if serializer.is_valid():
            # Ensure that the student is enrolled in the course related to the material
            material = serializer.validated_data.get('material')
            if not Enrollment.objects.filter(student=student, course=material.course).exists():
                return Response({'error': 'Student is not enrolled in the course'}, status=status.HTTP_403_FORBIDDEN)

            # Save the reading state with the associated student
            serializer.save(student=student)
            # Get the URL for the student_page view and include the student's pk
            student_page_url = reverse('student_page', kwargs={'pk': student.pk})
            return redirect(student_page_url)  # Redirect to the student_page with the student's pk

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class TutorViewSet (viewsets.ModelViewSet):
    queryset = User.objects.filter(role="Tutor")
    serializer_class = UserSerializer
    template_name = 'tutor_page.html'

    @action(detail=True, methods=['get'])
    def tutor_page(self, request, pk=None):
        tutor = self.get_object()
        context = {
            'tutor': tutor, 
            'all_courses': Course.objects.all(), 
            'all_students': User.objects.filter(role="Student"), 
            'all_assignments': Assignment.objects.all()
        }
        return render(request, self.template_name, context)


    #Create and manage courses.
    @action(detail=True, methods=['post'])
    def create_course(self, request, pk=None):
        tutor = self.get_object()
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tutor=tutor)
            tutor_page_url = reverse('tutor_page', kwargs={'pk': tutor.pk})
            return redirect(tutor_page_url)  # Redirect to the tutor page
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    #Create assignment.
    @action(detail=True, methods=['post'])
    def create_assignment(self, request, pk=None):
        tutor = self.get_object()
        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            tutor_page_url = reverse('tutor_page', kwargs={'pk': tutor.pk})
            return redirect(tutor_page_url)  # Redirect to the tutor page
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    #Upload course materials, including labs and documents in PDF format.
    @action(detail=True, methods=['post'])
    def upload_material(self, request, pk=None):
        tutor = self.get_object()
        serializer = MaterialSerializer(data=request.data)

        if serializer.is_valid():
            # Ensure that the tutor is the owner of the course related to the material
            course = serializer.validated_data.get('course')
            if course.tutor != tutor:
                return Response({'error': 'Tutor does not own the course'}, status=status.HTTP_403_FORBIDDEN)

            # Save the material with the associated course
            serializer.save()
            tutor_page_url = reverse('tutor_page', kwargs={'pk': tutor.pk})
            return redirect(tutor_page_url)  # Redirect to the tutor page

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

    #Evaluate and provide feedback on student assignments
    @action(detail=True, methods=['post'])
    def evaluate_student(self, request, pk=None):
        tutor = self.get_object()
        serializer = GradeSerializer(data=request.data)

        if serializer.is_valid():
            # Ensure that the tutor is the owner of the assignment being graded
            assignment = serializer.validated_data.get('assignment')
            if assignment.course.tutor != tutor:
                return Response({'error': 'Tutor does not own the assignment'}, status=status.HTTP_403_FORBIDDEN)

            serializer.save()

            tutor_page_url = reverse('tutor_page', kwargs={'pk': tutor.pk})
            return redirect(tutor_page_url)  # Redirect to the tutor page

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @action(detail=True, methods=['post'])
    def mark_absent_students(self, request, pk=None):
        tutor = self.get_object()

        # Example using Twilio (replace with your actual Twilio credentials):
        twilio_account_sid = 'AC20b42b8800734d036379cc38ab641517'
        twilio_auth_token = '87d3620cb8b751ba24214709f52388b1'
        twilio_from_number = '+21626870170'

        # Initialize the Twilio client
        twilio_client = Client(twilio_account_sid, twilio_auth_token)

        try:
            # Implement logic to initiate a voice call using Twilio
            call = twilio_client.calls.create(
                to='+21650804571',
                from_=twilio_from_number,
                url='http://demo.twilio.com/docs/voice.xml'  # Replace with your TwiML URL or TwiML response
            ) 

            return Response({'message': 'Voice call initiated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the Twilio error
            logging.error(f'Twilio Error: {str(e)}')

            # Return a response with an error message
            return Response({'error': 'Failed to initiate voice call'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Initiate voice calls to mark students as absent.
    #def initiate_voice_call (request):
    #    response = VoiceResponse()
    #    response.say("Hello, this is your attendance call. Please press a key to confirm your attendance. ") 
    #    response.gather(numDigits=1, action='/confirm_attendance/') 
    #    return HttpResponse(str(response), content_type='text/xml')
    #
    #def confirm_attendance(request):
    #    digit_pressed = request.GET.get('Digits')
    #    return HitpResponse("Confirmation processed. ")
    #
    #def trigger_voice_call(request):
    #    account_sid = "AC7ee59b1d490616ad7071cb36b1c109a8"
    #    auth_token = f4a5989c7566da12eff15f72578e883a"
    #    client = Client (account_sid, auth_token)
    #    call = client.calls. create(
    #        url=request.build_absolute_uri(reverse('initiate_voice_call')), 
    #        to="+1234567890",
    #        from_="+14435946087,
    #    )
    #    return HttpResponse(f"Voice call SID: {call.sid}")






class AdministratorViewSet (viewsets.ModelViewSet):
    queryset = User.objects.filter(role='Administrator')
    serializer_class = UserSerializer  
    template_name = 'admin_page.html' 

    @action(detail=True, methods=['get'])
    def admin_page(self, request, pk=None):
        admin = self.get_object()
        context = {
            'admin': admin, 
            'all_users': User.objects.all(),
            'all_submissions': Submission.objects.all(),
            'all_enrollments': Enrollment.objects.all(),
            'all_interactions': InteractionHistory.objects.all(),
            'all_assignments' : Assignment.objects.all(),
            'all_students': User.objects.filter(role="Student"),

        }
        return render(request, self.template_name, context)
    


    @action(detail=True, methods=['get'])
    def monitor_enrollments(self, request, pk=None):
        enrollments = Enrollment.objects.all()
        serializer = EnrollmentSerializer(enrollments, many=True)
        context = {'enrollments': serializer.data}
        return render(request, self.template_name, context)
    


    @action(detail=True, methods=['get'])
    def monitor_submissions(self, request, pk=None):
        submissions = Submission.objects.all()
        serializer = SubmissionSerializer(submissions, many=True)
        context = {'submissions': serializer.data}
        return render(request, self.template_name, context)
    

    @action(detail=True, methods=['get'])
    def monitor_interaction_history(self, request, pk=None):
        interaction_history = InteractionHistory.objects.all()
        serializer = InteractionHistorySerializer(interaction_history, many=True)
        context = {'interaction_history': serializer.data}
        return render(request, self.template_name, context)
    
    
    # Manage user accounts and roles
    @action(methods=['get'], detail=True)
    def user_list(self, request, pk=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        context = {'users': serializer.data}
        return render(request, self.template_name, context)
   



    @action(methods=['post'], detail=True)
    def user_edit(self, request, pk=None):
        admin = self.get_object()
        email = request.data.get('email')
    
        if email is None:
            return render(request, self.template_name, {'message': 'User email not provided'}, status=404)
    
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return render(request, self.template_name, {'message': 'User not found'}, status=404)
    
        if request.method == 'POST':
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                admin_page_url = reverse('admin_page', kwargs={'pk': admin.pk})
                return redirect(admin_page_url)  # Redirect to the tutor page
            else:
                return render(request, self.template_name, {'errors': serializer.errors}, status=400)
    
        return redirect(admin_page_url)  # Redirect to the tutor page



    @action(methods=['post'], detail=True)
    def user_delete(self, request,pk=None):
        admin = self.get_object()
        email = request.data.get('email')

        if email is None:
            return Response({'message': 'User email not provided'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            user = User.objects.get(email=email)
            user.delete()
            admin_page_url = reverse('admin_page', kwargs={'pk': admin.pk})
            return redirect(admin_page_url)  # Redirect to the tutor page
        
        except ObjectDoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        
    

    
    @action(detail=True, methods=['post'])
    def manage_grade(self, request, pk=None):
        admin = self.get_object()
        student_id = request.data.get('student')
        assignment_id = request.data.get('assignment')

        # Check if a grade already exists for this student and assignment
        existing_grade = Grade.objects.filter(student_id=student_id, assignment_id=assignment_id).first()

        if existing_grade:
            # If a grade exists, update the existing grade
            serializer = GradeSerializer(existing_grade, data=request.data)
        else:
            # If no grade exists, create a new grade
            serializer = GradeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            tutor_page_url = reverse('tutor_page', kwargs={'pk': admin.pk})
            return redirect(tutor_page_url)  # Redirect to the tutor page

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)