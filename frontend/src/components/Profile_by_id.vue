<template>
    <div class="container-fluid">
        <div class="row">
            <b-navbar type="dark" class="top-nav">
                <b-navbar-nav class="me-auto mx-5">
                    <b-navbar-brand>Blog Lite</b-navbar-brand>
                    <b-nav-form class="mx-5">
                        <div class="d-flex">
                            <b-form-input class="mr-sm-2" placeholder="Search" v-model="searchInput"></b-form-input>
                            <b-button class="mx-2 search" type="submit" @click="handleSearch">Search</b-button>
                        </div>
                    </b-nav-form>
                </b-navbar-nav>
                <b-navbar-nav class="ms-auto mx-5">
                    <b-nav-item @click="handleHomeLink">Home</b-nav-item>
                    <b-nav-item @click="handleProfile">Profile</b-nav-item>
                    <b-nav-item-dropdown :text="user_name">
                        <b-dropdown-item @click="handleExportLink">Export as csv</b-dropdown-item>
                        <b-dropdown-item @click="handleLogOut">Log out</b-dropdown-item>
                    </b-nav-item-dropdown>
                </b-navbar-nav>
            </b-navbar>
        </div>
        <div class="row d-flex mt-3">
            <div class="col-2"></div>
            <div class="col-3">
                <div class="profile-box shadow-div">
                    <div class="profile-box-photo">
                        <img :src="('data:image/jpg;base64,' + profileImage)">
                    </div>
                    <div>
                        <h4 style="display: flex; justify-content:center; margin-top: 10px;">{{ profile_user_name }}
                        </h4>
                    </div>
                    <div style="display: flex; justify-content:center; margin-top: 10px;">
                        <input type="button" :value=follow_unfollow id="follow-btn"
                            @click="handleFollow($route.params.id)">
                    </div>
                    <hr>
                    <div class="profile-data">
                        <p> <span>City</span>{{ city }}</p>
                        <p><span>Date of Birth</span>{{ dob }}</p>
                        <p><span>Profession</span>{{ profession }}</p>
                        <p><span>Joined On</span>{{ doj }}</p>

                    </div>
                </div>
                <div class="follow-box shadow-div">
                    <div class="followers">
                        <p>Followers : {{ totalFollowers }}</p>
                    </div>
                    <div class="following">
                        <p>Following : {{ totalFollowing }}</p>
                    </div>
                </div>
            </div>
            <div class="col-5">
                <div class="myposts shadow-div">
                    <h4>{{ profile_user_name }}'s Posts</h4>
                    <h6>No. of Posts : {{ noPosts }}</h6>
                </div>
                <div class="no-posts" v-if="!noPosts">There are no posts to show</div>
                <div class="feed-item shadow-div" v-for="eachPost in allPosts" :key="eachPost.key">
                    <div class="feed-item-first d-flex">
                        <img :src="('data:image/jpg;base64,' + eachPost.profileImage)" class="feed-prof-img" alt="img">
                        <div class="name-time">
                            <h4><router-link :to="'/profile/' + eachPost.user_id">{{ eachPost.user_name }}</router-link>
                            </h4>
                            <div class="d-flex">
                                <img class="icon" src="../assets/workwise/img/Time_50px.png">
                                <p class="text-muted" style="margin-top: -3px; margin-left: 5px;">{{
                                    timeDifference(eachPost.timestamp)
                                }}</p>
                            </div>
                        </div>
                    </div>
                    <div>
                        <p class="feed-caption">{{ eachPost.caption }}</p>
                    </div>
                    <div class="feed-img">
                        <img :src="('data:image/jpg;base64,' + eachPost.image)" alt="Image">
                    </div>
                    <p class="feed-caption">No. of Likes : {{ eachPost.likes }}</p>
                    <div style="margin-left:20px; margin-right:20px;">
                        <hr>
                    </div>
                    <div class="feed-like ms-auto" @click="handleLike(eachPost.id, eachPost.user_id)">
                        <img v-if="unliked(eachPost.likers)" src="../assets/icons/sheart.png" alt="">
                        <img v-else src="../assets/icons/wheart.png" alt="">
                    </div>
                </div>
            </div>
            <div class="col-2"></div>
        </div>
    </div>
</template>
<script>

export default {
    name: 'Profile_by_id',
    data: function () {
        return {
            city: "",
            dob: null,
            doj: null,
            joined_on: null,
            profession: "",
            user_name: "",
            user_id: null,
            profileImage: null,
            profile_user_name: "",
            allPosts: null,
            noPosts: 1,
            follow_unfollow: "",
            totalFollowers: "",
            totalFollowing: "",
            searchInput: "",
            allLikedPosts: [],

        }
    },
    computed: {
        timeDifference: function () {
            return timestamp => {
                const currentDate = new Date()
                const postDate = new Date(timestamp)
                const difference = currentDate - postDate

                const minute = 1000 * 60
                const hour = minute * 60
                const day = hour * 24
                const year = day * 365

                let result;
                if (difference >= year) {
                    result = `${Math.floor(difference / year)} years ago`
                } else if (difference >= day) {
                    result = `${Math.floor(difference / day)} days ago`
                } else if (difference >= hour) {
                    result = `${Math.floor(difference / hour)} hours ago`
                } else {
                    result = `${Math.floor(difference / minute)} minutes ago`
                }
                return result
            }
        }
    },
    methods: {
        unliked(likers) {
            const numbers = likers
            if (numbers.includes(this.user_id)) {
                return 0
            }
            return 1
        },
        handleHomeLink() {
            this.$router.push({ name: 'home' })
        },
        handleExportLink() {
            this.$router.push({ name: 'export' })
        },
        handleProfile() {
            this.$router.push({ name: 'profile' })
        },
        handleLogOut() {
            localStorage.removeItem('token')
            this.$router.push({ name: 'login' })
        },
        followersPage() {
            this.$router.push({ name: 'followers' })
        },
        followingPage() {
            this.$router.push({ name: 'following' })
        },
        handleSearch() {
            this.$router.push({ name: 'search', query: { q: this.searchInput } })
        },
        handleFollow(f_user_id) {
            if (document.getElementById('follow-btn').value == "follow") {
                fetch(`http://localhost:5000/follow/${f_user_id}`, {
                    method: 'POST',
                    headers: {
                        'f_user_id': f_user_id,
                        'user_id': this.user_id,
                        'x-access-token': localStorage.getItem('token')
                    }
                }).then(response => response.json()).then(data => {
                    if (data) {
                        console.log(data);
                        document.getElementById("follow-btn").value = "Following..."
                    }
                })
                    .catch(error => console.log(error))
                setTimeout(() => {
                    document.getElementById("follow-btn").value = "Unfollow"
                }, 1000);
            }
            else {
                fetch(`http://localhost:5000/unfollow/${f_user_id}`, {
                    method: 'POST',
                    headers: {
                        'f_user_id': f_user_id,
                        'user_id': this.user_id,
                        'x-access-token': localStorage.getItem('token')
                    }
                }).then(response => response.json()).then(data => {
                    console.log(data)
                    document.getElementById('follow-btn').value = "Unfollowing..."
                })
                    .catch(error => console.log(error))
                setTimeout(() => {
                    document.getElementById('follow-btn').value = "Follow"
                }, 1000);
            }

        },

        handleLike(post_id, f_user_id) {
            console.log(post_id, f_user_id)
            fetch("http://localhost:5000/handleLike", { method: "POST", headers: { 'post_id': post_id, 'f_user_id': f_user_id, 'user_id': this.user_id } })
                .then(response => response.json()).then(data => {
                    console.log(data)
                    fetch(`http://localhost:5000/getUserPosts/${this.$route.params.id}`, { headers: { 'user_id': this.$route.params.id, 'x-access-token': localStorage.getItem('token') }, })
                        .then(response => response.json()).then(data => {
                            this.allPosts = data
                            this.noPosts = data.length
                        })
                        .catch(error => console.log(error))
                })
                .catch(error => console.log(error))
        },
    },
    beforeMount: async function () {
        const jRequest = await fetch("http://localhost:5000/checkval", {
            method: 'POST',
            body: JSON.stringify({
                auth_token: localStorage.getItem('token')
            }),
            headers: {
                "Content-type": "application/json; charset-UTF-8",
            }
        })
        const jResponse = await jRequest.json()
        if (!jResponse) {
            console.log("login not successful")
            this.$router.push({ name: 'login' })
        }
        else {
            this.user_name = jResponse[1]
            this.user_id = jResponse[0]
            const pRequest = await fetch(`http://localhost:5000/getProfileDetails/${this.$route.params.id}`, {
                headers: {
                    'x-access-token': localStorage.getItem('token'),
                    'user_id': this.$route.params.id
                }
            })
            const pResponse = await pRequest.json()
            console.log(pResponse)
            if (pResponse) {
                this.profile_user_name = pResponse.profile_user_name
                this.city = pResponse.city
                this.profession = pResponse.profession
                this.dob = pResponse.dob
                this.doj = pResponse.doj
                this.totalFollowers = pResponse.totalFollowers
                this.totalFollowing = pResponse.totalFollowing
            }
        }

        fetch(`http://localhost:5000/getUserPosts/${this.$route.params.id}`, { headers: { 'user_id': this.$route.params.id, 'x-access-token': localStorage.getItem('token') }, })
            .then(response => response.json()).then(data => {
                this.allPosts = data
                this.noPosts = data.length
            })
            .catch(error => console.log(error))

        fetch(`http://localhost:5000/loadProfilePic/${this.user_id}`, { headers: { 'user_id': this.user_id, 'x-access-token': localStorage.getItem('token') } })
            .then(response => response.json()).then(data => {
                this.profileImage = data.image
            })
            .catch(error => {
                console.log(error)
            })

        fetch(`http://localhost:5000/getFollowStatus/${this.$route.params.id}`, { headers: { 'f_user_id': this.$route.params.id, 'user_id': this.user_id, 'x-access-token': localStorage.getItem('token') } })
            .then(response => response.json()).then(data => {
                if (data == true) {
                    this.follow_unfollow = "unfollow"
                }
                else {
                    this.follow_unfollow = "follow"
                }
            })
            .catch(error => console.log(error))
    }
}
</script>

<style>
.profile-box {
    width: 315.8px;
    min-height: 375px;
    background-color: white;
    text-align: left;
    margin-left: 20px;
    margin-right: 20px;
    margin-top: 60px;
    padding-bottom: 10px;
    position: fixed;
    color: #000038;
}

.profile-box-photo {
    display: flex;
    justify-content: center;
}

.profile-box-photo img {
    height: 150px;
    border-radius: 50%;
    margin-top: 20px;
    border: 2px solid black;
    padding: 5px;
}

.edit-profile {
    margin-right: 10px;
    display: flex;
    justify-content: flex-end;
}

.edit-profile p {
    font-size: small;
    text-decoration: underline;
}

.profile-data {
    margin-left: 30px;
}

.profile-data span {
    display: inline-block;
    width: 40%;
    position: relative;
    padding-right: 10px;
}

.profile-data span::after {
    content: ":";
    position: absolute;
    right: 10px;
}

.follow-box {
    background-color: white;
    width: 315.8px;
    margin-top: 525px;
    height: 100px;
    text-align: left;
    margin-left: 20px;
    margin-right: 20px;
    position: fixed;
    color: #000038;
}

.followers {
    height: 50px;
    text-align: center;
    border-bottom: 1px solid rgb(163, 149, 149);
    padding: 12px;
}

.following {
    height: 50px;
    text-align: center;
    padding: 12px;
}

.followers,
.following p {
    font-weight: 200;
}

.myposts {
    background-color: white;
    display: flex;
    height: 50px;
    width: 654px;
    margin-top: 60px;
    align-items: center;
    justify-content: space-between;
}

.myposts h4 {
    text-align: left;
    margin-left: 20px;
    width: 50%;
}

.myposts h6 {
    text-align: right;
    margin-right: 20px;
    width: 50%;
}

.no-posts {
    margin-top: 50px;
    font-size: 1.5rem;
    color: gray;
}

.three-dot {
    margin-inline-start: auto;
    margin-top: 20px;
    margin-right: 5px;
}

.three-dot img {
    height: 35px;
    width: auto;
}

#file {
    display: none;
}
</style>