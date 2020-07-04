import os
from .base import *
# you need to set "DJANGO_SETTINGS_MODULE = 'prod'" as an environment variable
# in your OS (on which your website is hosted)

if os.environ['DJANGO_SETTINGS_MODULE'] == 'prod':
  	from .prod import *
elif os.environ['DJANGO_SETTINGS_MODULE'] == 'stage':
  	from .stage import *
else :
	from .dev import *