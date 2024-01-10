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
                    <b-nav-item>Profile</b-nav-item>
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
                        <img :src="('data:image/jpg;base64,' + profileImage)" @click="changeProfile">
                        <input type="file" id="file" @change="onImageSelected">
                    </div>
                    <div>
                        <h4 style="display: flex; justify-content:center; margin-top: 10px;">{{ user_name }}</h4>
                    </div>
                    <hr>
                    <div class="edit-profile">
                        <p v-b-modal.modal-prevent-closing size="sm">Edit Profile</p>
                        <b-modal id="modal-prevent-closing" ref="modal" title="Edit your profile" @show="resetModal"
                            @hidden="resetModal" @ok="handleOk">
                            <form ref="edi-profile-form" @submit.stop.prevent="handleEdiProfileOk">
                                <b-form-group label="City">
                                    <b-form-input id="City" v-model="ucity" required></b-form-input>
                                </b-form-group>

                                <b-form-group label="Profession">
                                    <b-form-input id="profession" v-model="uprofession" required></b-form-input>
                                </b-form-group>

                                <b-form-group label="Date of Birth">
                                    <b-form-datepicker id="dob-input" v-model="udob" required
                                        class="mb-2"></b-form-datepicker>
                                </b-form-group>
                            </form>
                            <p v-if="profile_modal_error">Error</p>

                        </b-modal>
                    </div>
                    <div class="profile-data">
                        <p> <span>City</span>{{ city }}</p>
                        <p><span>Date of Birth</span>{{ dob }}</p>
                        <p><span>Profession</span>{{ profession }}</p>
                        <p><span>Joined On</span>{{ doj }}</p>

                    </div>
                </div>
                <div class="follow-box shadow-div">
                    <div class="followers">
                        <p @click="followersPage">Followers : {{ totalFollowers }}</p>
                    </div>
                    <div class="following">
                        <p @click="followingPage">Following : {{ totalFollowing }}</p>
                    </div>
                </div>
            </div>
            <div class="col-5">
                <div class="myposts shadow-div">
                    <h4>My Posts</h4>
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
                                <p class="text-muted" style="margin-top: -3px; margin-left: 5px;">
                                    {{ timeDifference(eachPost.timestamp) }}</p>
                            </div>
                        </div>
                        <div class="edit_remove">
                            <div style="display: flex;">
                                <img src="../assets/icons/edit.png" alt="edit">&nbsp;
                                <p v-b-modal="'modal-prevent-closing-feed' + eachPost.id" size="sm"
                                    @click="setPost_id(eachPost.id, eachPost.caption)">Edit</p>
                                <b-modal :id="'modal-prevent-closing-feed' + eachPost.id" ref="modal-2"
                                    title="Edit your blog" @show="resetModalFeed" @hidden="resetModalFeed"
                                    @ok="handleOkFeed">
                                    <form ref="edit-blog-form" @submit.stop.prevent="handleEdiProfileOkFeed">
                                        <b-form-group label="Change Caption">
                                            <b-form-input id="caption" v-model="ucaption" :value="eachPost.caption"
                                                required></b-form-input>
                                        </b-form-group>

                                        <b-form-group label="Change Picture">
                                            <b-form-file id="picture" v-model="upicture" placeholder=""></b-form-file>
                                        </b-form-group>
                                    </form>
                                    <p v-if="profile_modal_feed_error">Error</p>
                                </b-modal>

                            </div>
                            <div style="display: flex;" v-b-modal="'delete-modal' + eachPost.id">
                                <img src="../assets/icons/remove.png" alt="remove">&nbsp;
                                <p>Delete</p>
                            </div>
                            <b-modal :id="'delete-modal' + eachPost.id" title="Delete Blog" @ok=removePost(eachPost.id)>
                                <p class="my-4">Are you sure you want to delete this blog? If yes, click OK.</p>
                            </b-modal>
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
                        <img v-else src="../assets/icons/edit.png" alt="">
                    </div>
                </div>
            </div>
            <div class="col-2"></div>
        </div>
    </div>
</template>
<script>


export default {
    name: 'Profile_page',
    data: function () {
        return {
            city: "",
            dob: null,
            doj: null,
            joined_on: null,
            profession: "",
            profile_modal_error: false,
            profile_modal_feed_error: false,
            user_name: "",
            user_id: null,
            ucity: "",
            udob: null,
            ucaption: "",
            upicture: null,
            uprofession: "",
            changedPic: null,
            profileImage: null,
            allPosts: null,
            noPosts: 1,
            totalFollowers: "",
            totalFollowing: "",
            post_id: null,
            searchInput: "",

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
        },
    },
    methods: {
        resetModal() {
            this.ucity = ""
            this.udob = null
            this.uprofession = ""
            this.profile_modal_error = false
        },

        handleEdiProfileOk() {
            if (this.ucity == "" || this.udob == null || this.uprofession == "") {
                console.log(this.udob)
                this.profile_modal_error = true
            }
            else {
                this.$nextTick(async () => {
                    this.$bvModal.hide('modal-prevent-closing')
                    const pRequest = await fetch("http://localhost:5000/updateProfile", {
                        method: 'POST',
                        body: JSON.stringify({
                            user_id: this.user_id,
                            city: this.ucity,
                            profession: this.uprofession,
                            dob: this.udob
                        }),

                        headers: {
                            "Content-type": "application/json; charset-UTF-8",
                            'x-access-token': localStorage.getItem('token')
                        }
                    })
                    const pResponse = await pRequest.json()
                    console.log(pResponse)

                    const qRequest = await fetch(`http://localhost:5000/getProfileDetails/${this.user_id}`, { headers: { 'user_id': this.user_id, 'x-access-token': localStorage.getItem('token') } })
                    const qResponse = await qRequest.json()
                    if (qResponse) {
                        this.city = qResponse.city
                        this.profession = qResponse.profession
                        this.dob = qResponse.dob
                        this.doj = qResponse.doj
                    }
                })
            }
        },
        handleOk(bvModalEvent) {
            bvModalEvent.preventDefault()
            this.handleEdiProfileOk()

        },
        setPost_id(post_id, caption) {
            this.post_id = post_id
            this.ucaption = caption
        },
        resetModalFeed() {
            this.upicture = null
            this.profile_modal_error = false

        },

        handleEdiProfileOkFeed() {
            if (this.ucaption == "" && this.upicture == null) {
                this.profile_modal_feed_error = true
                console.log("here")
            }
            else {
                this.$nextTick(async () => {
                    this.$bvModal.hide('modal-prevent-closing-feed')
                    const fd = new FormData()
                    fd.append('user_id', this.user_id)
                    fd.append('post_id', this.post_id)
                    fd.append('caption', this.ucaption)
                    fd.append('newImage', this.upicture)
                    const pRequest = await fetch("http://localhost:5000/updateFeedPost", {
                        headers: { 'x-access-token': localStorage.getItem('token') },
                        method: 'POST',
                        body: fd
                    })
                    const pResponse = await pRequest.json()
                    console.log(pResponse)
                    fetch(`http://localhost:5000/getUserPosts/${this.user_id}`, { headers: { 'user_id': this.user_id, 'x-access-token': localStorage.getItem('token') } })
                        .then(response => response.json()).then(data => {
                            this.allPosts = data
                            this.noPosts = data.length
                        })
                        .catch(error => console.log(error))
                })
            }
        },
        handleOkFeed(bvModalEvent2) {
            bvModalEvent2.preventDefault()
            this.handleEdiProfileOkFeed()
        },
        openDeleteModal() {
            this.$refs.deleteModal.show()
        },
        removePost(post_id) {
            console.log(post_id)
            fetch(`http://localhost:5000/removePost/${post_id}`, { headers: { 'post_id': post_id, 'user_id': this.user_id, 'x-access-token': localStorage.getItem('token') } })
                .then(response => response.json()).then(data => console.log(data))
                .catch(error => console.log(error))
        },
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
        handleLogOut() {
            localStorage.removeItem('token')
            this.$router.push({ name: 'login' })
        },
        toggleDropdown() {
            this.showDropdown = !this.showDropdown
        },
        changeProfile() {
            document.getElementById('file').click();
        },
        onImageSelected(event) {
            this.changedPic = event.target.files[0]
            console.log(this.changedPic)
            const fd = new FormData()
            fd.append('image', this.changedPic)
            fd.append('user_id', this.user_id)
            fetch("http://localhost:5000/profilePicUpload", {
                headers: { 'x-access-token': localStorage.getItem('token') },
                method: "POST",
                body: fd
            })
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
        handleLike(post_id, f_user_id) {
            console.log(post_id, f_user_id)
            fetch("http://localhost:5000/handleLike", { method: "POST", headers: { 'post_id': post_id, 'f_user_id': f_user_id, 'user_id': this.user_id } })
                .then(response => response.json()).then(data => {
                    console.log(data)
                    fetch(`http://localhost:5000/getUserPosts/${this.user_id}`, { headers: { 'user_id': this.user_id, 'x-access-token': localStorage.getItem('token') }, })
                        .then(response => response.json()).then(data => {
                            this.allPosts = data
                            this.noPosts = data.length
                        })
                        .catch(error => console.log(error))
                })
                .catch(error => console.log(error))
        },
    },
    mounted: async function () {
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
            const pRequest = await fetch(`http://localhost:5000/getProfileDetails/${this.user_id}`, { headers: { 'user_id': this.user_id, 'x-access-token': localStorage.getItem('token') } })
            const pResponse = await pRequest.json()
            if (pResponse) {
                this.city = pResponse.city
                this.profession = pResponse.profession
                this.dob = pResponse.dob
                this.doj = pResponse.doj
                this.totalFollowers = pResponse.totalFollowers
                this.totalFollowing = pResponse.totalFollowing
            }
        }
        fetch(`http://localhost:5000/getUserPosts/${this.user_id}`, { headers: { 'user_id': this.user_id, 'x-access-token': localStorage.getItem('token') }, })
            .then(response => response.json()).then(data => {
                this.allPosts = data
                this.noPosts = data.length
            })
            .catch(error => console.log(error))

        fetch(`http://localhost:5000/loadProfilePic/${this.user_id}`, { headers: { 'user_id': this.user_id, 'x-access-token': localStorage.getItem('token') }, })
            .then(response => response.json()).then(data => {
                this.profileImage = data.image
            })
            .catch(error => {
                console.log(error)
            })
    }
}
</script>

<style scoped>
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

.edit_remove p:hover {
    font-size: 1rem;
    cursor: pointer;
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

.follow-box :hover {
    background-color: #000038;
    color: white;
    cursor: pointer;
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

.three-dot {
    margin-inline-start: auto;
    margin-top: 20px;
    margin-right: 5px;
}

.three-dot img {
    height: 35px;
    width: auto;
}

.edit_remove {
    margin-inline-start: auto;
    margin-top: 20px;
    margin-right: 5px;
    display: flex;
}

.edit_remove div {
    margin-right: 20px;
}

.edit_remove img {
    height: 15px;
    width: auto;
}

.edit_remove p {
    text-decoration: underline;
    font-size: 0.8rem;
}

.dropdown-menu {
    background-color: transparent !important;
    border: none !important;
}

#file {
    display: none;
}
</style>