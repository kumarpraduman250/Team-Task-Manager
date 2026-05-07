# Team Task Manager

A full-stack task management application built with Django REST Framework and React, featuring role-based access control, JWT authentication, and real-time dashboard statistics.

## 🚀 Features

### Authentication
- JWT-based authentication system
- User registration with role selection (Admin/Member)
- Secure login/logout functionality
- Token refresh mechanism

### Core Functionality
- **Project Management**: Create, view, update, delete projects
- **Task Management**: Create, assign, track task status and due dates
- **Role-based Access**: Different features for Admin vs Member users
- **Dashboard**: Real-time statistics and insights

### User Roles
- **Admin**: Full access to create projects, manage users, complete CRUD operations
- **Member**: View assigned tasks, update status, access project details

## 🛠 Tech Stack

### Backend
- **Framework**: Django 5.0.2
- **API**: Django REST Framework 3.14.0
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite (development) / PostgreSQL (production)
- **CORS**: django-cors-headers
- **Deployment**: Gunicorn + WhiteNoise

### Frontend
- **Framework**: React 18.2.0
- **Routing**: React Router DOM 6.3.0
- **HTTP Client**: Axios
- **Styling**: CSS with modern design
- **State Management**: React Context API

## 📋 API Endpoints

### Authentication
- `POST /api/login/` - User login
- `POST /api/signup/` - User registration
- `POST /api/token/refresh/` - Refresh JWT token
- `GET /api/profile/` - Get user profile

### Projects
- `GET /api/projects/` - List projects
- `POST /api/projects/` - Create project (Admin only)
- `GET /api/projects/{id}/` - Get project details
- `PUT /api/projects/{id}/` - Update project
- `DELETE /api/projects/{id}/` - Delete project

### Tasks
- `GET /api/tasks/` - List tasks with filters
- `POST /api/tasks/` - Create task
- `GET /api/tasks/{id}/` - Get task details
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task

### Dashboard
- `GET /api/dashboard/stats/` - Get dashboard statistics

## 🗄 Database Models

### User
```python
class User(AbstractUser):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
```

### Project
```python
class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Task
```python
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    due_date = models.DateField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd team-task-manager
```

2. **Backend Setup**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

3. **Frontend Setup**
```bash
cd frontend
npm install
npm start
```

### Default Credentials
- **Admin Username**: `admin`
- **Admin Password**: `admin123`
- **Admin Panel**: `http://localhost:8000/admin/`

## 🌐 Access Points

### Development
- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000/api/`
- **Admin Panel**: `http://localhost:8000/admin/`

### Production Deployment
- **Backend**: Deploy on Railway with PostgreSQL
- **Frontend**: Deploy on Vercel/Netlify or serve from Django

## 📊 Dashboard Features

The dashboard provides real-time statistics:
- Total tasks and projects
- Task status breakdown (Todo, In Progress, Done)
- Overdue task alerts
- Personal task statistics
- Quick action buttons for common tasks

## 🔐 Security Features

- JWT-based authentication
- Role-based access control
- CORS configuration
- Input validation and sanitization
- Secure password handling

## 🚀 Deployment

### Railway (Backend)
1. Push code to GitHub
2. Create new Railway project
3. Connect GitHub repository
4. Add PostgreSQL plugin
5. Set environment variables:
   - `SECRET_KEY`: Django secret key
   - `DEBUG`: False
   - `DATABASE_URL`: PostgreSQL connection string
   - `ALLOWED_HOSTS`: Railway domain

### Vercel (Frontend)
1. Build React app: `npm run build`
2. Deploy `build` folder to Vercel
3. Set environment variable for API URL

## 🧪 Testing

### Backend Tests
```bash
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📝 Development

### Adding New Features
1. **Backend**: Create models, serializers, views
2. **Frontend**: Create components, update routing
3. **API**: Add new endpoints with proper permissions
4. **Testing**: Write unit and integration tests

### Code Style
- **Python**: Follow PEP 8
- **JavaScript**: Use ESLint configuration
- **Components**: Keep components small and focused

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**: Check frontend URL in CORS settings
2. **Authentication Failures**: Verify JWT configuration
3. **Database Issues**: Run migrations and check models
4. **Build Errors**: Check dependencies and Node version

### Debug Mode
Enable Django debug mode:
```python
DEBUG = True
```

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check existing documentation
- Review troubleshooting section

---

**Built with ❤️ using Django and React**
