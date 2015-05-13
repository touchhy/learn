__author__ = 'bzhang'

import utility

rest = utility.Utility()
rest.login()
rest.token()
user = rest.get_login_user_info()
course = rest.create_one_course()
membership = rest.enroll(course['id'], user['id'], "P")
