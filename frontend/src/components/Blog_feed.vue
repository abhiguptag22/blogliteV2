<template>
  <div class="container-fluid">
    <div class="row">
      <b-navbar class="top-nav" type="dark">
        <b-navbar-nav class="me-auto mx-5">
          <b-navbar-brand>Blog Lite</b-navbar-brand>
          <b-nav class="mx-5">
            <div class="d-flex">
              <b-input class="mr-sm-2" placeholder="Search" v-model="searchInput"></b-input>
              <b-button class="mx-2 search" type="submit" @click="handleSearch">Search</b-button>
            </div>
          </b-nav>
        </b-navbar-nav>
        <b-navbar-nav class="ms-auto mx-5">
          <b-nav-item>Home</b-nav-item>
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
      <div class="col-3 align-items-center">
        <div class="suggestion-box center shadow-div">
          <div class="sug-head">
            <h4>Suggestions</h4>
          </div>
          <hr style="border-top: 3px solid">
          <div class="all-sugs">
            <div v-for="(suggestion, index) in suggestions" :key="index">
              <div class="person d-flex" v-if="suggestion.hidden">
                <img :src="('data:image/jpg;base64,' + suggestion.image)" alt="Image" id="sug-img">
                <h6 id="sug-h6"><router-link :to="'/profile/' + suggestion.user_id">{{
                  suggestion.user_name
                }}</router-link>
                </h6>

                <div class="follow ms-auto mx-3">
                  <input type="button" :value="suggestion.follow_unfollow" id="follow-btn"
                    @click="handleFollow(suggestion.user_id, index)">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-5">
        <div class="post-tab shadow-div d-flex">
          <img class="prof-img" :src="('data:image/jpg;base64,' + profileImage)">
          <input type="text" v-model="caption" placeholder="Caption" class="post-input">
          <div class="d-flex">
            <input type="file" id="input-file" name='image' @change="onFileSelected">
            <input type="button" value="Post" id="post-btn" @click="onUpload">

          </div>
        </div>
        <div class="no-posts" v-if="!noPosts">There are no posts to show</div>
        <div class="feed-item shadow-div" v-for="eachPost in allPosts" :key="eachPost.key">
          <div class="feed-item-first d-flex">
            <img :src="('data:image/jpg;base64,' + eachPost.profileImage)" class="feed-prof-img" alt="img">
            <div class="name-time">
              <h4><router-link :to="'/profile/' + eachPost.user_id">{{ eachPost.user_name }}</router-link></h4>
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
  name: "blog_feed",
  data() {
    return {
      searchInput: "",
      selectedFile: null,
      caption: "",
      user_name: "",
      user_id: "",
      profileImage: null,
      allPosts: null,
      postImages: null,
      suggestions: null,
      noPosts: 1
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
    onFileSelected(event) {
      this.selectedFile = event.target.files[0]
    },

    unliked(likers) {
      const numbers = likers
      if (numbers.includes(this.user_id)) {
        return 0
      }
      return 1
    },

    onUpload() {
      console.log(this.selectedFile)
      const fd = new FormData()
      fd.append('image', this.selectedFile)
      fd.append('caption', this.caption)
      fd.append('user_id', this.user_id)
      fd.append('user_name', this.user_name)
      fetch("http://localhost:5000/uploadPost", {
        method: "POST",
        body: fd,
        headers: {
          'x-access-token': localStorage.getItem('token')
        }
      }).then(
        this.caption = "",
        document.getElementById("input-file").value = null,
        fetch(`http://localhost:5000/getAllPosts`, { headers: { 'user_id': this.user_id, 'x-access-token': localStorage.getItem('token') } })
          .then(response => response.json()).then(data => {
            this.allPosts = data
            this.noPosts = data.length
          })
          .catch(error => console.log(error)))
    },

    handleLogOut() {
      localStorage.removeItem('token')
      this.$router.push({ name: 'login' })
    },

    handleExportLink() {
      this.$router.push({ name: 'export' })
    },

    handleProfile() {
      this.$router.push({ name: 'profile' })
    },

    handleFollow(f_user_id, index) {
      fetch(`http://localhost:5000/follow/${f_user_id}`, {
        method: 'POST',
        headers: {
          'f_user_id': f_user_id,
          'user_id': this.user_id,
          'x-access-token': localStorage.getItem('token')
        }
      }).then(response => response.json()).then(data => console.log(data))
        .catch(error => console.log(error))
      this.suggestions[index].follow_unfollow = "following"
      setTimeout(() => {
        this.suggestions[index].hidden = false
      }, 1000);
    },

    handleSearch() {
      this.$router.push({ name: 'search', query: { q: this.searchInput } })
    },

    handleLike(post_id, f_user_id) {
      console.log(post_id, f_user_id)
      fetch("http://localhost:5000/handleLike", { method: "POST", headers: { 'post_id': post_id, 'f_user_id': f_user_id, 'user_id': this.user_id } })
        .then(response => response.json()).then(data => {
          console.log(data)
          fetch(`http://localhost:5000/getAllPosts`, { headers: { 'user_id': this.user_id, 'x-access-token': localStorage.getItem('token') } })
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
        'x-access-token': localStorage.getItem('token')
      }
    })
    const jResponse = await jRequest.json()
    console.log(jResponse)
    if (!jResponse) {
      console.log("login not successful")
      this.$router.push({ name: 'login' })
    }
    else {
      this.user_id = jResponse[0]
      this.user_name = jResponse[1]
      fetch(`http://localhost:5000/loadProfilePic/${this.user_id}`, { headers: { 'user_id': this.user_id, 'x-access-token': localStorage.getItem('token') } })
        .then(response => response.json()).then(data => {
          this.profileImage = data.image
        })
        .catch(error => {
          console.log(error)
        })
    }
    fetch(`http://localhost:5000/getAllPosts`, { headers: { 'user_id': this.user_id, 'x-access-token': localStorage.getItem('token') } })
      .then(response => response.json()).then(data => {
        this.allPosts = data
        this.noPosts = data.length
      })
      .catch(error => console.log(error))

    fetch(`http://localhost:5000/suggestions`, { headers: { 'user_id': this.user_id, 'x-access-token': localStorage.getItem('token') } })
      .then(response => response.json()).then(data => {
        for (let i = 0; i < data.length; i++) {
          data[i].hidden = true
          data[i].follow_unfollow = 'Follow'
        }
        this.suggestions = data
      })
      .catch(error => console.log(error))
  }
}

</script>
<style>
.navbar-expand {
  color: white;
  position: fixed !important;
}

.navbar-nav .nav-link {
  color: white;
}

.top-nav {
  background-color: #000039 !important;
  position: fixed I !important;
}

.search {
  background-color: #000039 !important;
  color: white;
}

.suggestion-box {
  width: 315.8px;
  height: 375px;
  background-color: white;
  text-align: left;
  margin-left: 20px;
  margin-right: 20px;
  margin-top: 60px;
  position: fixed;
  /* margin-right: auto; */
  /* margin-left: 70px; */
}

.sug-head h4 {
  margin-top: 20px;
  margin-left: 20px;
  display: inline-block;
  color: #000038;
  font-weight: bold;
  text-align: left;
}

.post-tab {
  background-color: white;
  height: 120px;
  width: 654px;
  align-items: center;
  margin-left: auto;
  margin-top: 60px;
  margin-right: auto;
  border-bottom: 2px solid #000039;
}

.feed-item {
  background-color: white;
  min-height: 20px;
  width: 654px;
  margin-left: auto;
  margin-right: auto;
  margin-top: 20px;
  margin-bottom: 20px;
}

.feed-item h4 {
  font-weight: 200;
  color: #000038;
  margin-top: 20px;
  margin-left: 5px;
  margin-bottom: 5px;
  font-weight: bold;
  font-size: 1.1rem;
}

.feed-item h4 a {
  color: #000038;
  text-decoration: none;
}

.feed-item h4:hover {
  text-decoration: underline;
  cursor: pointer;
}

.icon {
  height: 17px;
}

.feed-caption {
  color: #666666;
  margin-top: 17px;
  margin-left: 20px;
  text-align: left;
}

.feed-img img {
  margin-left: 20px;
  margin-right: 20px;
  margin-bottom: 20px;
  max-width: -webkit-fill-available;
}

.feed-like img {
  height: 40px;
  margin-bottom: 10px;
}

.prof-img {
  height: 53px;
  width: 53px;
  border-radius: 50%;
  margin-left: 20px;
  margin-right: 10px;
}

.feed-prof-img {
  height: 53px;
  width: 53px;
  border-radius: 50%;
  margin-left: 20px;
  margin-right: 10px;
  margin-top: 20px;
}

.person {
  margin-bottom: 20px;
}

.person h6 a {
  color: #000038;
  text-decoration: none;
}

.person h6:hover {
  text-decoration: underline;
}

#sug-img {
  height: 40px;
  width: 40px;
  border-radius: 50%;
  margin-left: 20px;
  margin-right: 10px;
}

#sug-h6 {
  margin-top: 8px;
}

.post-input {
  height: 66px;
  margin-right: 10px;
}

#input-file {
  padding-top: 35px;
}

#post-btn {
  margin-left: -51px;
  margin-top: 25px;
  width: 30%;
  height: 40px;
  background-color: #000038;
  color: white;
}

#follow-btn {
  background-color: #000038;
  color: white;
}

#follow-btn:hover {
  background-color: #1d4c01;
}

.shadow-div {
  /* border-radius: 15px; */
  box-shadow: 3px 3px 3px 3px #ccc;
}
</style>