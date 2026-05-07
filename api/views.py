from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from datetime import date
from .models import Project, Task
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer
from .permissions import IsAdmin, IsProjectMember, IsAssignedUserOrAdmin

User = get_user_model()


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    pass


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Project.objects.all()
        return Project.objects.filter(
            Q(created_by=user) | Q(members=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Project.objects.all()
        return Project.objects.filter(
            Q(created_by=user) | Q(members=user)
        ).distinct()


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.all()
        
        if user.role != 'ADMIN':
            queryset = queryset.filter(
                Q(project__created_by=user) | Q(project__members=user)
            ).distinct()
        
        project_id = self.request.query_params.get('project', None)
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        
        assigned_to = self.request.query_params.get('assigned_to', None)
        if assigned_to:
            queryset = queryset.filter(assigned_to_id=assigned_to)
        
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset

    def perform_create(self, serializer):
        serializer.save()


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAssignedUserOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Task.objects.all()
        return Task.objects.filter(
            Q(project__created_by=user) | Q(project__members=user)
        ).distinct()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    user = request.user
    
    if user.role == 'ADMIN':
        tasks = Task.objects.all()
        projects = Project.objects.all()
    else:
        tasks = Task.objects.filter(
            Q(project__created_by=user) | Q(project__members=user)
        ).distinct()
        projects = Project.objects.filter(
            Q(created_by=user) | Q(members=user)
        ).distinct()
    
    today = date.today()
    
    stats = {
        'total_tasks': tasks.count(),
        'total_projects': projects.count(),
        'completed_tasks': tasks.filter(status='DONE').count(),
        'in_progress_tasks': tasks.filter(status='IN_PROGRESS').count(),
        'todo_tasks': tasks.filter(status='TODO').count(),
        'overdue_tasks': tasks.filter(due_date__lt=today, status__in=['TODO', 'IN_PROGRESS']).count(),
        'my_assigned_tasks': tasks.filter(assigned_to=user).count(),
        'my_completed_tasks': tasks.filter(assigned_to=user, status='DONE').count(),
    }
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_list(request):
    if request.user.role != 'ADMIN':
        return Response({'detail': 'Permission denied'}, status=403)
    
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
