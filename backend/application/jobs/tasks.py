from application.jobs.workers import celery
from application.data.models import PostItems, User, Followers, Following
import datetime
from flask_mail import Mail, Message
import csv
from celery.schedules import crontab
from flask import current_app as app, render_template



@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hours=17, minutes=30), send_email_task.s(), name='Every day at 05:30' )
    sender.add_periodic_task(crontab(day_of_month=1), send_monthly_report.s(), name='On 1st of every month' )

@celery.task
def sayHello():
    return "hello"

mail = Mail()

@celery.task
def send_email_task():
    with app.app_context():
        mail.init_app(app)
        allUsers = User.query.all()
        for eachUser in allUsers:
            now = datetime.datetime.utcnow()
            last_login = eachUser.last_login
            last_post = eachUser.last_post
            if (now-last_login).days >= 1:
                message = "Hi {name}!\nIt's been a while since you last logged in to Blog Lite or posted anything. Please do log in to see latest updates.".format(name=eachUser.name)
                msg = Message(
                            'Blog Lite Login Reminder',
                            sender ='abhigupta.g2@yahoo.com',
                            recipients = [eachUser.email]
                        )
                msg.body = message
                mail.send(msg)
            elif (now-last_post).days >=1:
                message = "Hi {name}!\n It's been a while since you or last posted anything. Please do log in to see latest updates and share.".format(name=eachUser.name)
                msg = Message(
                            'Blog Lite Login Reminder',
                            sender ='abhigupta.g2@yahoo.com',
                            recipients = [eachUser.email]
                        )
                msg.body = message
                mail.send(msg)

        return 'Sent'

@celery.task
def send_monthly_report():
    with app.app_context():
        mail.init_app(app)
        allUsers = User.query.all()
        for eachUser in allUsers:
            name = eachUser.name
            allPosts = PostItems.query.filter_by(user_id=eachUser.id).all()
            total_posts=0
            total_likes=0
            if allPosts:
                total_posts = len(allPosts)
                for post in allPosts:
                    total_likes += post.likes
            followers = Followers.query.filter_by(user_id=eachUser.id).first()
            total_followers = 0
            if followers:
                total_followers = len(followers.followers)
            following = Following.query.filter_by(user_id=eachUser.id).first()
            total_following = 0
            if following:
                total_following = len(following.following)

            message = render_template("report.html", name=name, total_likes = total_likes, total_posts=total_posts, total_followers=total_followers, total_following=total_following)
            msg = Message(
                        'Blog Lite Monthly Report',
                        sender ='abhigupta.g2@yahoo.com',
                        recipients = [eachUser.email]
                    )
            msg.html = message
            mail.send(msg)





@celery.task
def generate_csv(user_id):
    allPosts = PostItems.query.filter_by(user_id=user_id).all()
    csv_file = 'posts_{}.csv'.format(user_id)
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Id', 'Caption','No. of Likes', 'Post Creation Time', 'Has Image'])
        for eachPost in allPosts:
            if eachPost.imagelink:
                hasImage="Yes"
            else:
                hasImage= "No"
            writer.writerow([eachPost.id, eachPost.caption, eachPost.likes, eachPost.timestamp.date(), hasImage])
    return csv_file

