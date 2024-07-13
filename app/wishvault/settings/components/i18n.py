from wishvault.settings.vars import env

LANGUAGE_CODE = env('LANGUAGE_CODE')

TIME_ZONE = env('TIME_ZONE')

USE_I18N = env('USE_I18N') == "True"

USE_TZ = env('USE_TZ') == "True"







