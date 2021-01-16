import os
from decouple import config

print("MYSQL_USER:", config('MYSQL_PASSWORD'))



# HOST=localhost
# MYSQL_USER=root  
# MYSQL_PASSWORD=thaije20
# MYSQL_PORT=3306
# MYSQL_DB=Reddit
# MYSQL_AUTH_PLUGIN=mysql_native_password