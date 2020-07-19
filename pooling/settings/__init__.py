import os
from .base import *
# you need to set "DJANGO_ENV = 'prod'" as an environment variable
# in your OS (on which your website is hosted)

if os.environ.get('DJANGO_ENV','') == 'prod':
  	from .prod import *
elif os.environ.get('DJANGO_ENV','') == 'stage':
  	from .stage import *
else :
	from .dev import *