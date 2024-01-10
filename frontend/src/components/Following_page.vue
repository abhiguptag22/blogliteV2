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
            <b-dropdown-item @click="handleExportLink">Export as csv</b-dropdown-item>
            <b-dropdown-item @click="handleLogOut">Log out</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-navbar>
    </div>
    <div class="row">
      <div class="col-4"></div>
      <div class="col-4">
        <div class="following-heading shadow-div">
          <h4>
            People you are following
          </h4>
        </div>
        <div class="following-box shadow-div">
          <div v-for="(following, index) in allFollowing" :key="index">
            <div class="following-one d-flex" v-if="following.hidden">
              <img :src="('data:image/jpg;base64,' + following.image)">
              <h6 id="sug-h6"><router-link :to="'/profile/' + following.user_id">{{ following.user_name }}</router-link>
              </h6>
              <div class="follow ms-auto mx-3">
                <input type="button" :value="following.follow_unfollow" id="follow-btn"
                  @click="handleUnfollow(following.user_id, index)">
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-4"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Following_page',
  data: function () {
    return {
      user_id: null,
      user_name: '',
      allFollowing: null,
      searchInput: "",
    }
  },
  methods: {
    handleHomeLink() {
      this.$router.push({ name: 'home' })
    },
    handleExportLink() {
      this.$router.push({ name: 'export' })
    },
    handleProfileLink() {
      this.$router.push({ name: 'profile' })
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
  beforeMount: function () {
    fetch('http://localhost:5000/checkval', {
      method: 'POST',
      body: JSON.stringify({
        auth_token: localStorage.getItem('token')
      }),
      headers: {
        "Content-type": "application/json; charset-UTF-8",
      }
    }).then(response => response.json()).then(data => {
      this.user_name = data[1]
      this.user_id = data[0]
      fetch('http://localhost:5000/getFollowingList', { headers: { 'user_id': this.user_id, 'x-access-token': localStorage.getItem('token') } })
        .then(response => response.json()).then(data => {
          for (let i = 0; i < data.length; i++) {
            data[i].hidden = true
            data[i].follow_unfollow = 'Unfollow'
          }
          this.allFollowing = data
          console.log(data)
        }).catch(error => console.log(error))
    }).catch(error => {
      console.log(error)
      this.$router.push({ name: 'login' })
    })
  }
}
</script>
<style>
.following-heading {
   margin-top: 75px;
   background-color: white;
   height: 45px;
 }

 .following-heading h4 {
   display: flex;
   margin-left: 20px;
   padding: 7px;
   color: #000038
 }

 .following-one {
   padding-top: 20px;
 }

 .following-one img {
   height: 40px;
   width: 40px;
   border-radius: 50%;
   margin-left: 20px;
   margin-right: 10px;
 }

 .following-one h6 {
   margin-top: 8px;
 }

 .following-one h6 a {
   color: #000038;
   text-decoration: none;
 }

 .following-one h6:hover {
   text-decoration: underline;
 }

 .following-box {
   margin-top: 20px;
   background-color: white;
   min-height: 500px;
 }
</style>