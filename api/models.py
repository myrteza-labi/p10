from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Modèle User
class User(AbstractUser):
    age = models.PositiveIntegerField()
    can_be_contacted = models.BooleanField()
    can_data_be_shared = models.BooleanField()

# Modèle Project
class Project(models.Model):
    BACK_END = 'BE'
    FRONT_END = 'FE'
    IOS = 'IOS'
    ANDROID = 'AND'
    TYPE_CHOICES = [
        (BACK_END, 'Back-end'),
        (FRONT_END, 'Front-end'),
        (IOS, 'iOS'),
        (ANDROID, 'Android'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=3)
    author_user = models.ForeignKey('api.User', on_delete=models.CASCADE, related_name='projects')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Modèle Contributor
class Contributor(models.Model):
    user = models.ForeignKey('api.User', on_delete=models.CASCADE)
    project = models.ForeignKey('api.Project', on_delete=models.CASCADE, related_name='contributors')
    permission = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.username} - {self.project.name}"

# Modèle Issue
class Issue(models.Model):
    BUG = 'BUG'
    FEATURE = 'FEATURE'
    TASK = 'TASK'
    TAG_CHOICES = [
        (BUG, 'Bug'),
        (FEATURE, 'Feature'),
        (TASK, 'Task'),
    ]

    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    TODO = 'TODO'
    IN_PROGRESS = 'INPROGRESS'
    FINISHED = 'FINISHED'
    STATUS_CHOICES = [
        (TODO, 'To Do'),
        (IN_PROGRESS, 'In Progress'),
        (FINISHED, 'Finished'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    tag = models.CharField(choices=TAG_CHOICES, max_length=7)
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=6)
    project = models.ForeignKey('api.Project', on_delete=models.CASCADE, related_name='issues')
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default=TODO)
    author_user = models.ForeignKey('api.User', on_delete=models.CASCADE, related_name='authored_issues')
    assignee_user = models.ForeignKey('api.User', on_delete=models.CASCADE, related_name='assigned_issues')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Modèle Comment
class Comment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    issue = models.ForeignKey('api.Issue', on_delete=models.CASCADE, related_name='comments')
    description = models.TextField()
    author_user = models.ForeignKey('api.User', on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.uuid} on {self.issue.title}"
