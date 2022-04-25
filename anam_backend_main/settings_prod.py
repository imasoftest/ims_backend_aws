DEBUG = False
ALLOWED_HOSTS = ['5.39.81.217']
# ALLOWED_HOSTS = ['192.232.213.37', 'standomsports.com']
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/IMSAdmin/static'
# MEDIA_ROOT = '/var/www/IMSAdmin/media'
# STATIC_ROOT = 'C:/Users/Ambition/Documents/standom/static'
# MEDIA_ROOT = 'C:/Users/Ambition/Documents/standom/static/upload'
# MEDIA_URL = '/media/'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
print("Debug Flase")
