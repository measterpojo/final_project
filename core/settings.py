import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q3f9p2ys^*==#4nysymd%1cuq#%=u8^5k8y^-$j4iodj^$(k0s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # myapps
    'core',
    'accounts',
    'blog',
    'blocker',
    'comments',
    'search',
    'profiles',
    'reactions',
    'flags',
    'followers',


    # 3rd party
    'crispy_forms'
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'db',
#         'PORT': 5432
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'accounts.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



PROFILE_APP_NAME = None
PROFILE_MODEL_NAME = None

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'root/static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


LOGIN_REDIRECT_URL = 'blog:index'
LOGOUT_REDIRECT_URL = 'blog:index'
LOGIN_URL = '/login'


PAGINATE_BY = 10

CACHES = {

    'default':{
        'BACKEND':
        'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION':'unique-snowflake',

    }

}



# BLOCKED

ALLOW_BLOCKING_USERS = False

SITE_ID = 1

# EMAIL


EMAIL_FIELD = ''

# REDIS
# if os.environ.get("DJANGO_REDIS_URL"):
#     CACHES = {
#         'default': {
#             'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#             'LOCATION': f'redis://{os.environ.get("DJANGO_REDIS_URL")}',
#         }
#     }

DEFAULT_PROFILE_PIC_LOC = '/static/avatars/default.jpg'


WRAP_CONTENT_WORDS = 30


MARKDOWN_EXTENSIONS = ['markdown.extensions.fenced_code']
MARKDOWN_EXTENSION_CONFIG = {}

# COMMENTS DEFAULTS 
COMMENT_USE_GRAVATAR = False

COMMENT_URL_PREFIX = 'comment-'
COMMENT_URL_SUFFIX = ''
COMMENT_URL_ID_LENGTH = 8
COMMENT_PER_PAGE = 10

COMMENT_ORDER_BY = ['-posted']

COMMENT_USE_GRAVATAR = False

COMMENT_FLAGS_ALLOWED = 5
COMMENT_SHOW_FLAGGED = False

COMMENT_RESPONSE_FOR_BLOCKED_USER = 'You cannot perform this action at the moment! Contact the admin for more details'
COMMENT_ALLOW_ANONYMOUS = False
COMMENT_ALLOW_SUBSCRIPTION = True
COMMENT_ALLOW_BLOCKING_USERS = False

FLAG_REASONS = [
    (1, ('Spam | Exists only to promote a service')),
    (2, ('Abusive | Intended at promoting hatred')),
]

