# import os
from decouple import config
print("MYSQL_USER:", config('REDDIT_USERNAME'))
# # HOST=localhost
# # MYSQL_USER=root  
# # MYSQL_PASSWORD=thaije20
# # MYSQL_PORT=3306
# # MYSQL_DB=Reddit
# # MYSQL_AUTH_PLUGIN=mysql_native_password

import pandas as pd