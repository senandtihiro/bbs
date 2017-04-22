# #!/usr/bin/env python3
#
# import sys
# from os.path import abspath
# from os.path import dirname
# import app as bbs
#
# app = bbs.configured_app()
# # sys.path.insert(0, abspath(dirname(__file__)))
# # application = app.app
#
# # gunicorn appcorn:app
# # nohup gunicorn -b '0.0.0.0:80' appcorn:app &
#
# # wsgi


import app as bbs

app = bbs.configured_app()

# gunicorn appcorn:app
# nohup gunicorn -b '0.0.0.0:80' appcorn:app &

# wsgi
