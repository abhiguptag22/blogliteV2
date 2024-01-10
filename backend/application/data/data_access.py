from application.data.models import User, PostItems, Followers, Following
from flask  import jsonify
from flask import current_app as app
import base64
from flask_caching import Cache


cache = Cache(app)

@cache.cached(5)
def get_all_users():
    res = User.query.all()
    return res

@cache.memoize(5)
def get_user_by_id(user_id):
    print("here in memoize", user_id)
    res = User.query.filter_by(id=user_id).first()
    return res

@cache.memoize(5)
def get_post_by_post_id(post_id, user_idm):
    res = PostItems.query.filter_by(id=post_id, user_id = user_idm).first()
    return res


@cache.memoize(5)
def get_profile_by_user_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    followersInst = Followers.query.filter_by(user_id=user_id).first()
    if followersInst:
        totalFollowers = len(followersInst.followers)
    else:
        totalFollowers = 0
    followingInst = Following.query.filter_by(user_id=user_id).first()
    if followingInst:
        totalFollowing = len(followingInst.following)
    else:
        totalFollowing = 0
    
    # try:
    if not (user.dob):
        return jsonify(profile_user_name=user.name ,city=user.city, profession=user.profession, dob="", doj=str(user.doj.date()), totalFollowers=totalFollowers, totalFollowing=totalFollowing)
    return jsonify(profile_user_name=user.name ,city=user.city, profession=user.profession, dob=str(user.dob.date()), doj=str(user.doj.date()),totalFollowers=totalFollowers, totalFollowing=totalFollowing)

@cache.memoize(5)
def get_propic_by_id(user_id):
    try:
        with open('image_files/'+str(user_id)+"/profilepic.jpg", 'rb') as f:
            image_data = f.read()
            profileImage = base64.b64encode(image_data).decode()
            f.close()
    except:
        with open('image_files/no_image.jpg', 'rb') as f:
            image_data = f.read()
            profileImage = base64.b64encode(image_data).decode()
            f.close()
    return jsonify(image=profileImage)



@cache.memoize(5)
def get_suggs_by_uid(user_idm):
    followings = Following.query.filter_by(user_id=user_idm).first()
    allUsers = get_all_users()
    res = []

    for eachUser in allUsers:
        if followings:
            if (eachUser.id != user_idm) and (eachUser.id not in followings.following):
                user_id = eachUser.id
                user_name = eachUser.name
                try:
                    with open('image_files/'+str(user_id)+"/profilepic.jpg", 'rb') as f:
                        image_data = f.read()
                        imagelink = base64.b64encode(image_data).decode()
                        f.close()
                except:
                    with open('image_files/no_image.jpg', 'rb') as f:
                        image_data = f.read()
                        imagelink = base64.b64encode(image_data).decode()
                        f.close()
                res.append({'user_id':user_id,'user_name':user_name, 'image':imagelink})
        else:
            if (eachUser.id != user_idm):
                user_id = eachUser.id
                user_name = eachUser.name
                try:
                    with open('image_files/'+str(user_id)+"/profilepic.jpg", 'rb') as f:
                        image_data = f.read()
                        imagelink = base64.b64encode(image_data).decode()
                        f.close()
                except:
                    with open('image_files/no_image.jpg', 'rb') as f:
                        image_data = f.read()
                        imagelink = base64.b64encode(image_data).decode()
                        f.close()
                res.append({'user_id':user_id,'user_name':user_name, 'image':imagelink})
    return res
