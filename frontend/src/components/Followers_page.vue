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
        <div class="followers-heading shadow-div">
          <h4>
            People who are following you
          </h4>
        </div>
        <div class="followers-box shadow-div">
          <div class="follower-one d-flex" v-for="follower in allFollowers" :key="follower.key">
            <img :src="('data:image/jpg;base64,' + follower.image)">
            <h6 id="sug-h6"><router-link :to="'/profile/' + follower.user_id">{{ follower.user_name }}</router-link>
            </h6>
          </div>
        </div>
      </div>
      <div class="col-4"></div>
    </div>
  </div>
</template>

<script>


export default {
  name: 'Followers_page',
  data: function () {
    return {
      user_id: null,
      user_name: '',
      allFollowers: null,
      searchInput: "",
    }
  },
  methods: {
    handleHomeLink() {
      this.$router.push({ name: 'home' })
    },
    handleProfileLink() {
      this.$router.push({ name: 'profile' })
    },
    handleExportLink() {
      this.$router.push({name: 'export'})
    },
    handleLogOut() {
      localStorage.removeItem('token')
      this.$router.push({ name: 'login' })
    },
    handleSearch() {
      this.$router.push({ name: 'search', query: { q: this.searchInput } })
    },
  },
  beforeMount: async function () {
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
      fetch('http://localhost:5000/getFollowersList', { headers: { 'user_id': this.user_id, 'x-access-token':localStorage.getItem('token') } })
        .then(response => response.json()).then(data => {
          this.allFollowers = data
          console.log(data)
        }).catch(error => console.log(error))
    }).catch(error => {
      console.log(error)
      this.$router.push({ name: 'login' })
    })
  },
}
</script>
<style>
.followers-heading {
  margin-top: 75px;
  background-color: white;
  height: 45px;
}

.followers-heading h4 {
  display: flex;
  margin-left: 20px;
  padding: 7px;
  color: #000038
}

.follower-one {
  padding-top: 20px;
}

.follower-one img {
  height: 40px;
  width: 40px;
  border-radius: 50%;
  margin-left: 20px;
  margin-right: 10px;
}

.follower-one h6 {
  margin-top: 8px;
}

.follower-one h6 a {
  color: #000038;
  text-decoration: none;
}

.follower-one h6:hover {
  text-decoration: underline;
}


.followers-box {
  margin-top: 20px;
  background-color: white;
  min-height: 500px;
}
</style>