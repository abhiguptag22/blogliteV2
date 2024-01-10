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
                    <b-nav-item @click="handleProfileLink">Profile</b-nav-item>
                    <b-nav-item-dropdown :text="user_name">
                        <b-dropdown-item>Export as csv</b-dropdown-item>
                        <b-dropdown-item @click="handleLogOut">Log out</b-dropdown-item>
                    </b-nav-item-dropdown>
                </b-navbar-nav>
            </b-navbar>
        </div>
        <div class="row">
            <div class="col-3"></div>
            <div class="col-6">
                <div class="export-heading d-flex " style="align-items: center; justify-content: space-between;">
                    <h4 style="text-align: left; vertical-align: middle;">Export your blogs</h4>
                    <h5 style="text-align: right;" @click="requestExport">Click here to make a request</h5>
                </div>
                <div class="download-area">
                    <h6 id="d-text">Your download file is ready. Click Below to download it.</h6>
                    <div v-if="enableButton"><a :href="'http://localhost:5000/checkTaskStatus/'+taskId"><button id="download-btn">Download</button></a></div>
                </div>
            </div>
            <div class="col-3"></div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'Export_Blogs',
    data: function () {
        return {
            user_id: null,
            user_name: "",
            searchInput: "",
            taskId : "",
            enableButton: false
        }
    },
    methods: {
        handleHomeLink() {
            this.$router.push({ name: 'home' })
        },
        handleProfileLink() {
            this.$router.push({ name: 'profile' })
        },
        requestExport() {
            fetch("http://localhost:5000/exportCsv", {
                headers: {
                    'user_id': this.user_id
                }
            }).then(response => response.json()).then(data => {
                this.taskId=data
                localStorage.setItem("taskId", this.taskId)
                document.getElementById('d-text').innerText = "Your request has been sent. Refresh or check again in few minutes to download your file."
            })
        },
        handleUnfollow(f_user_id, index) {
            fetch(`http://localhost:5000/unfollow/${f_user_id}`, {
                method: 'POST',
                headers: {
                    'f_user_id': f_user_id,
                    'user_id': this.user_id,
                    'x-access-token': localStorage.getItem('token')
                }
            }).then(response => response.json()).then(data => console.log(data))
                .catch(error => console.log(error))
            this.allFollowing[index].follow_unfollow = "Unfollowed"
            setTimeout(() => {
                this.allFollowing[index].hidden = false
            }, 3000);
        },
        handleLogOut() {
            localStorage.removeItem('token')
            this.$router.push({ name: 'login' })
        },
        handleSearch() {
            this.$router.push({ name: 'search', query: { q: this.searchInput } })
        },
    },
    mounted: async function () {
        fetch('http://localhost:5000/checkval', {
            method: 'POST',
            body: JSON.stringify({
                auth_token: localStorage.getItem('token')
            }),
            headers: {
                "Content-type": "application/json; charset-UTF-8",
            }
        }).then(response => response.json()).then(async data => {
            this.user_name = data[1]
            this.user_id = data[0]
            if (localStorage.getItem('taskId')) {
                this.enableButton = true
                this.taskId = localStorage.getItem('taskId')
            }
            else {
                this.enableButton = false
                document.getElementById("d-text").innerText = "Click on the above link to generate a request."
            }
        }).catch(error => {
            console.log(error)
            this.$router.push({ name: 'login' })
        })
    }
}
</script>

<style>
.export-heading {
     margin-top: 75px;
     background-color: white;
     min-height: 50px;
 }

 .export-heading h4 {
     margin-left: 20px;
     font-size: 1.6rem;
     color: #000038;
 }

 .export-heading h5 {
     margin-right: 20px;
     font-size: 1.2rem;
     color: #000038;
 }

 .export-heading h5:hover {
     text-decoration: underline;
     cursor: pointer;
     font-size: 1.3rem;
 }

 .download-area {
     background-color: white;
     margin-top: 20px;
     min-height: 220px;
     align-items: center;
     padding: 70px;
 }

 .download-area h6 {
     margin: auto;
     color: #000038;
 }

 #download-btn {
     margin-top: 35px !important;
     background-color: #000038;
     color: white;
 }
</style>