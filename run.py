import os
import sys

if __name__ == "__main__":
    api = sys.argv[1]
    if api == 'user':
        from src import app_user
        app_user.app.run('127.0.0.1', 5000, debug=True, ssl_context='adhoc')
    elif api == 'admin':
        from src import app_admin
        app_admin.app.run('127.0.0.1', 8000, debug=True, ssl_context='adhoc')
    else:
        print('api is not selected')
