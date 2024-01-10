from flask_restful import Resource
from application.data.database import db
from flask import current_app as app
from flask import request, jsonify, send_file
import datetime
import secrets, base64
from application.data.models import User, PostItems, Followers, Following, token_required
import jwt, os
from flask_caching import Cache
from application.data import data_access
from flask import current_app as app
from application.jobs import tasks


cache = Cache(app)

# test_api_resource_fields = {
#     'msg':    fields.String,
# }

# class TestAPI(Resource):
#     @token_required
#     def get(self):
#         return jsonify(msg="hi")



class Registrations(Resource):
    def post(self):
        data = request.get_json()
        if (data['name'] and data['email'] and data['password']):
            already_exists = User.query.filter_by(email=data['email']).first()
            if ( not already_exists):
                newUser = User(name=data['name'], email=data['email'], password=data['password'])
                db.session.add(newUser)
                db.session.commit()
                
                return jsonify({"msg":"Registration successful"})
            else:
                return jsonify({"msg":"email already exists"})
        else:
            return jsonify({"msg":"Registration not successful"})

class Logins(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']
        if (email and password):
            aUser = User.query.filter_by(email=email, password=password).first()
            if aUser:
                auth_token = aUser.encode_auth_token(aUser.id, aUser.name)
                aUser.last_login = datetime.datetime.utcnow()
                db.session.commit()
                return jsonify(token=auth_token.decode('utf-8'))
            else:
                return jsonify(msg="incorrect")

class checkVal(Resource):
    def post(self):
        data = request.get_json()
        auth_token = data['auth_token']
        try:
            user = jwt.decode(auth_token, "SECRET", algorithms=["HS256"])
            if user['sub']:
                return user['sub']
        except:
            return False

class getProfileDetails(Resource):
    @token_required
    def get(self):
        user_id = request.headers['user_id']
        try:
            data_access.get_profile_by_user_id(user_id)
        except:
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

class updateProfile(Resource):
    @token_required
    def post(self):
        data = request.get_json()
        user_id = data['user_id']
        city = data['city']
        profession = data['profession']
        dob = data['dob']
        user = User.query.filter_by(id=user_id).first()
        try:
            user.city = city
            user.profession = profession
            user.dob = datetime.datetime.strptime(dob, "%Y-%m-%d")
            # db.session.add
            db.session.commit()
            return jsonify(msg='success')
        except:
            return jsonify(msg="something went wrong")

class updateFeedPost(Resource):
    @token_required
    def post(self):
        img = request.files.get('newImage')
        user_idm = request.form.get('user_id')
        caption = request.form.get('caption')
        post_id = request.form.get('post_id')
        postObj = data_access.get_post_by_post_id(post_id, user_idm)
        try:
            if caption:
                postObj.caption = caption
            if img:
                user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_idm+"/posts")
                file_name = secrets.token_hex(10)
                while True:
                    if os.path.isfile(str(user_folder)+'/{0}.jpg'.format(file_name)):
                        file_name = secrets.token_hex(10)
                    else:
                        img.save(str(user_folder)+'/{0}.jpg'.format(file_name))
                        break
                postObj.imagelink = file_name
            db.session.commit()
        except:
            return "something went wrong"
            

        return 200

class removePost(Resource):
    @token_required
    def get(self):
        post_id = request.headers['post_id']
        user_idm = request.headers['user_id']
        postObj = data_access.get_post_by_post_id(post_id, user_idm)
        if postObj:
            file_to_remove = postObj.imagelink
            file_path = 'image_files/{user_id}/posts/{file_name}.jpg'.format(user_id=user_idm, file_name=file_to_remove)
            os.remove(file_path)
            db.session.delete(postObj)
            db.session.commit()
            return 200
        return 400

class ProfilePicUpload(Resource):
    @token_required
    def post(self):
        data  = request.files.get('image')
        user_id = request.form.get('user_id')
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
        try:
            os.mkdir(user_folder)
        except:
            pass
        data.save(str(user_folder)+'/profilepic.jpg')
        return 200

class LoadProfilePicture(Resource):
    @token_required
    def get(self):
        user_id = request.headers['user_id']
        try:
            return data_access.get_propic_by_id(user_id)
        except:
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
class UploadPost(Resource):
    @token_required
    def post(self):
        image = request.files.get('image')
        caption = request.form.get('caption')
        user_id = request.form.get('user_id')
        user_name = request.form.get('user_name')
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_id+"/posts")
        try:
            os.mkdir(user_folder)
        except:
            pass
        file_name = secrets.token_hex(10)
        while True:
            if os.path.isfile(str(user_folder)+'/{0}.jpg'.format(file_name)):
                file_name = secrets.token_hex(10)
            else:
                image.save(str(user_folder)+'/{0}.jpg'.format(file_name))
                timestamp = datetime.datetime.utcnow()
                postItem = PostItems(user_id=user_id,user_name=user_name, caption=caption, imagelink=file_name, likes=0, timestamp=timestamp)
                db.session.add(postItem)
                userObj = User.query.filter_by(id=user_id).first()
                userObj.last_post = datetime.datetime.utcnow()
                db.session.commit()
                break 
        return 200

class getAllPosts(Resource):
    @token_required
    def get(self):
        user_idm = int(request.headers['user_id'])
        followingListRaw = Following.query.filter_by(user_id=user_idm).first()
        if followingListRaw:
            followingList = followingListRaw.following
            followingList.append(user_idm)
        else:
            followingList = [user_idm]
        all_posts = PostItems.query.filter(PostItems.user_id.in_(followingList)).all()
        res = []
        for eachPost in all_posts:
            imgLink = eachPost.toDict()['imagelink']
            user_id = eachPost.toDict()['user_id']
            res.append(eachPost.toDict())
            with open('image_files/'+str(user_id)+'/posts/'+imgLink+".jpg", 'rb') as f:
                image_data = f.read()
                res[-1]['image'] = base64.b64encode(image_data).decode()
                f.close()
            try:
                with open('image_files/'+str(user_id)+"/profilepic.jpg", 'rb') as f:
                    image_data = f.read()
                    res[-1]['profileImage'] = base64.b64encode(image_data).decode()
                    f.close()
            except:
                with open('image_files/no_image.jpg', 'rb') as f:
                    image_data = f.read()
                    res[-1]['profileImage'] = base64.b64encode(image_data).decode()
                    f.close()
        sortedRes = sorted(res, key=lambda x: x['timestamp'], reverse=True)
        return jsonify(sortedRes)

class getUserPosts(Resource):
    @token_required
    def get(self):
        user_id = request.headers['user_id']
        all_posts = PostItems.query.filter_by(user_id=user_id).all()
        res = []
        for eachPost in all_posts:
            imgLink = eachPost.toDict()['imagelink']
            user_id = eachPost.toDict()['user_id']
            res.append(eachPost.toDict())
            with open('image_files/'+str(user_id)+'/posts/'+imgLink+".jpg", 'rb') as f:
                image_data = f.read()
                res[-1]['image'] = base64.b64encode(image_data).decode()
                f.close()
            try:
                with open('image_files/'+str(user_id)+"/profilepic.jpg", 'rb') as f:
                    image_data = f.read()
                    res[-1]['profileImage'] = base64.b64encode(image_data).decode()
                    f.close()
            except:
                with open('image_files/no_image.jpg', 'rb') as f:
                    image_data = f.read()
                    res[-1]['profileImage'] = base64.b64encode(image_data).decode()
                    f.close()
        sortedRes = sorted(res, key=lambda x: x['timestamp'], reverse=True)
        # print(sortedRes)
        return jsonify(sortedRes) 

class Suggestion(Resource):
    @token_required
    def get(self):
        user_idm = int(request.headers['user_id'])
        res = data_access.get_suggs_by_uid(user_idm)
        return jsonify(res)


class Follow(Resource):
    @token_required
    def post(self):
        user_idm = int(request.headers['user_id'])
        f_user_id = int(request.headers['f_user_id'])

        try:
            allFollowings = Following.query.filter_by(user_id=user_idm).first()
            if allFollowings:
                temp = allFollowings.following.copy()
                if not (f_user_id in temp):
                    temp.append(f_user_id)
                    allFollowings.following = temp
            else:
                followingInst = Following(user_id=user_idm, following =[f_user_id])
                db.session.add(followingInst)
            
            allFollowers = Followers.query.filter_by(user_id=f_user_id).first()
            if allFollowers:
                temp = allFollowers.followers.copy()
                if not (user_idm in temp):
                    temp.append(user_idm)
                    allFollowers.followers = temp
            else:
                followersInst = Followers(user_id=f_user_id, followers =[user_idm])
                db.session.add(followersInst)

            db.session.commit()
            return 200
        except:
            return 500

class Unfollow(Resource):
    @token_required
    def post(self):
        f_user_id = int(request.headers['f_user_id'])
        user_idm = int(request.headers['user_id'])

        try:
            allFollowings = Following.query.filter_by(user_id=user_idm).first()
            temp = allFollowings.following.copy()
            temp.remove(int(f_user_id))
            allFollowings.following = temp
            allFollowers = Followers.query.filter_by(user_id=f_user_id).first()
            temp = allFollowers.followers.copy()
            print("heree")
            print(temp)
            temp.remove(int(user_idm))
            allFollowers.followers = temp
            print("here")
            db.session.commit()
            return 200
        except(Exception):
            return Exception


class getFollowersList(Resource):
    # @token_required
    def get(self):
        user_idm = int(request.headers['user_id'])
        followersListRaw = Followers.query.filter_by(user_id=user_id).first()
        if followersListRaw:
            allFollowers = followersListRaw.followers
            res = []
            for eachFollower in allFollowers:
                user = User.query.filter_by(id=int(eachFollower)).first()
                user_name = user.name
                user_id = user.id
                try:
                    with open('image_files/'+str(eachFollower)+"/profilepic.jpg", 'rb') as f:
                        image_data = f.read()
                        imagelink = base64.b64encode(image_data).decode()
                        f.close()
                except:
                    with open('image_files/no_image.jpg', 'rb') as f:
                        image_data = f.read()
                        imagelink = base64.b64encode(image_data).decode()
                        f.close()
                res.append({'user_id':user_id,'user_name':user_name, 'image':imagelink})
        return jsonify(res)

class getFollowingList(Resource):
    # @token_required
    def get(self):
        user_idm = int(request.headers['user_id'])
        followingListRaw = Following.query.filter_by(user_id=user_idm).first()
        if followingListRaw:
            allFollowing = followingListRaw.following
            res = []
            for eachFollowing in allFollowing:
                user = User.query.filter_by(id=int(eachFollowing)).first()
                user_name = user.name
                user_id = user.id
                try:
                    with open('image_files/'+str(eachFollowing)+"/profilepic.jpg", 'rb') as f:
                        image_data = f.read()
                        imagelink = base64.b64encode(image_data).decode()
                        f.close()
                except:
                    with open('image_files/no_image.jpg', 'rb') as f:
                        image_data = f.read()
                        imagelink = base64.b64encode(image_data).decode()
                        f.close()
                res.append({'user_id':user_id,'user_name':user_name, 'image':imagelink})
        return jsonify(res)

class getFollowStatus(Resource):
    @token_required
    def get(self):
        f_user_id = int(request.headers['f_user_id'])
        user_idm = int(request.headers['user_id'])
        followingInst = Following.query.filter_by(user_id=user_idm).first()
        if followingInst:
            if (f_user_id in followingInst.following):
                return True
            else:
                return False
        return False

class searchResults(Resource):
    @token_required
    def get(self):
        user_idm = int(request.headers['user_id'])
        searchInput = request.headers['q']
        allUsers = User.query.filter(User.name.ilike("%"+searchInput+"%")).all()
        res = []
        for eachUser in allUsers:
            user_name = eachUser.name
            user_id = eachUser.id
            if not (user_idm == eachUser.id):
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
        return jsonify(res)

class handleLike(Resource):
    def post(self):
        post_id = int(request.headers['post_id'])
        f_user_id = int(request.headers['f_user_id'])
        user_id = int(request.headers['user_id'])

        postObj = PostItems.query.filter_by(id=post_id, user_id=f_user_id).first()
        try:
            if user_id in postObj.likers:
                temp = postObj.likers.copy()
                temp.remove(user_id)
                postObj.likers = temp
            else:
                temp = postObj.likers.copy()
                temp.append(user_id)
                postObj.likers = temp
            postObj.likes = len(postObj.likers)
            db.session.commit()
            return 200
        except:
            return "error"

class export_csv(Resource):
    def get(self):
        user_id = int(request.headers['user_id'])
        task =  tasks.generate_csv.apply_async(args=[user_id])
        return task.id

class check_task_status(Resource):
    def get(self, task_id):
        # task_id = request.headers['task_id']
        task = tasks.generate_csv.AsyncResult(task_id)
        if task.ready():
            return send_file(task.result, as_attachment=True, mimetype='text/csv', download_name='post.csv')
        else:
            return "still in progress"


