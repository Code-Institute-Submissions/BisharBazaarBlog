# Import necessary modules
from pathlib import Path
import os
import dj_database_url

# Check if env.py file exists and import its content
if os.path.isfile('env.py'):
    import env

# Define base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key for cryptographic signing
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-i##z=f-3@)^#d92lbo6^qf+nr28)vk5v5m@&7ezdcc6vpg_#u2')

# Debug mode (should be False in production)
DEBUG = False

# List of allowed hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.herokuapp.com']

# Installed apps for the project
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'django_summernote',
    'cloudinary',
    'BazaarApp',
    'about',
]

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Root URL configuration
ROOT_URLCONF = 'BisharBazaarBlog.urls'

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Adjust this line to point to your templates directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'BisharBazaarBlog.wsgi.application'

# Database URL obtained from ElephantSQL
DATABASE_URL = "postgres://nlovytsr:wbExrZs22LkixXwa74-2lEtuMFZzcpsn@delicate-quince.db.elephantsql.com/nlovytsr"

# Parse the DATABASE_URL
db_from_env = dj_database_url.config(default=DATABASE_URL)

# Update the DATABASES setting to use the parsed URL
DATABASES = {
    'default': db_from_env
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms configuration for Bootstrap 5
CRISPY_TEMPLATE_PACK = 'bootstrap5'  # Add this line to specify Bootstrap 5 template pack
