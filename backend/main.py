import os
from flask import Flask, jsonify, render_template
from flask_restful import  Api
from application.config import LocalDevelopmentConfig
from application.data.database import db
from flask import current_app as app
from application.data.models import User
import os
from flask_security import Security, SQLAlchemySessionUserDatastore
from application.data.models import Role
from flask_cors import CORS
from flask_mail import Mail, Message
from application.jobs import workers
from application.jobs import tasks


app = None
api = None
mail = None
cache = None
celery = None
def create_app():
    app = Flask(__name__, template_folder="templates")
  
    print("Staring Local Development")
    app.config.from_object(LocalDevelopmentConfig)
    app.config['MAIL_SERVER']='smtp.mail.yahoo.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'abhigupta.g2@yahoo.com'
    app.config['MAIL_PASSWORD'] = 'mnjkiftpvwttcuph'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    db.init_app(app)
    # mail = Mail(app)
    app.app_context().push()
    # Setup Flask-Security
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)  
    api = Api(app)
    CORS(app)
    db.create_all()
    app.app_context().push()
    celery = workers.celery
    celery.conf.update(
      broker_url = app.config['CELERY_BROKER_URL'], 
      result_backend = app.config['CELERY_RESULT_BACKEND'])  
    celery.Task = workers.ContextTask
    app.app_context().push()
    return app, api, celery

app,api, celery= create_app()



from application.controller.api import UploadPost, Registrations, Logins, checkVal, getProfileDetails
from application.controller.api import updateProfile, ProfilePicUpload, LoadProfilePicture, getAllPosts
from application.controller.api import Suggestion, Follow, Unfollow, getFollowersList, getFollowingList
from application.controller.api import getUserPosts, getFollowStatus, searchResults, updateFeedPost, removePost
from application.controller.api import handleLike, export_csv, check_task_status

api.add_resource(Registrations, '/signup')
api.add_resource(Logins, '/logins')
api.add_resource(UploadPost, '/uploadPost')
api.add_resource(checkVal, '/checkval')
api.add_resource(getProfileDetails, '/getProfileDetails/<int:user_id>')
api.add_resource(updateProfile, '/updateProfile')
api.add_resource(ProfilePicUpload, '/profilePicUpload')
api.add_resource(LoadProfilePicture, '/loadProfilePic/<int:user_id>')
api.add_resource(getAllPosts, '/getAllPosts')
api.add_resource(Suggestion, '/suggestions')
api.add_resource(Follow, '/follow/<int:f_user_id>')
api.add_resource(Unfollow, '/unfollow/<int:f_user_id>')
api.add_resource(getFollowersList, '/getFollowersList')
api.add_resource(getFollowingList, '/getFollowingList')
api.add_resource(getUserPosts, '/getUserPosts/<int:user_id>')
api.add_resource(getFollowStatus, '/getFollowStatus/<int:f_user_id>')
api.add_resource(searchResults, '/searchResults')
api.add_resource(updateFeedPost, '/updateFeedPost')
api.add_resource(removePost, '/removePost/<int:post_id>')
api.add_resource(handleLike, '/handleLike')
api.add_resource(export_csv, '/exportCsv')
api.add_resource(check_task_status, '/checkTaskStatus/<task_id>')




if __name__ == '__main__':
  # Run the Flask app
  app.run(
    debug=True
  )
