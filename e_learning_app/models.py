from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    role = models.CharField(max_length=20, choices=[('Student', 'Student'), ('Tutor', 'Tutor'), ('Administrator', 'Administrator')], default='Student')
    username = models.CharField(max_length=20,blank=False, null=False,default="")
    password = models.CharField(blank=False, null=False, max_length=100,default="0000")
    email = models.EmailField(default="@gmail.com", max_length=100, null=False, blank=False, unique=True)
    date_joined = models.DateField(default=timezone.now)


    class Meta:
        db_table='User' 

    def __str__(self):
        return self.username  # Assuming you want to display the username    


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Tutor'})
    enrollment_capacity = models.PositiveIntegerField()



class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.email} - {self.course.title}"  # Identify users by email




class Material(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    upload_date = models.DateField(auto_now_add=True)
    document_type = models.CharField(max_length=50, choices=[('PDF', 'PDF'), ('DOC', 'Word Document'), ('LAB', 'Lab Report')])  # e.g., PDF



class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()


    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Student'})




class Submission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Student'})
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submission_content = models.TextField()
    submission_date = models.DateField(auto_now_add=True)



class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Student'})
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='grades')
    grade = models.FloatField()
    feedback = models.TextField()




class InteractionHistory(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Student'})
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=50)  # e.g., upload, read
    interaction_date = models.DateField(auto_now_add=True)



class ReadingState(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Student'})
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    read_state = models.FloatField()  # e.g., percentage completed
    last_read_date = models.DateField(auto_now=True)  # Update on each read


