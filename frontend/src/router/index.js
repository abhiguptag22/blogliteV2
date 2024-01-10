import Vue from 'vue'
import VueRouter from 'vue-router'
//import HomeView from '../views/HomeView.vue'
import blog_feed from "../components/Blog_feed.vue"
import Login_page from "@/components/Login_page.vue"
import Signup_page from "@/components/Signup_page.vue"
import Profile_page from "@/components/Profile_page.vue"
import Followers_page from "@/components/Followers_page.vue"
import Following_page from "@/components/Following_page.vue"
import Search_results from "@/components/Search_results.vue"
import profile_by_id from "@/components/Profile_by_id.vue"
import Export_Blogs from "@/components/Export_blog.vue"
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: blog_feed
  },
  {
    path : '/profile',
    name : 'profile',
    component: Profile_page
  },
  {
    path : '/profile/:id',
    name : 'profile_by_id',
    component: profile_by_id
  },
  {
    path: '/export',
    name: 'export',
    component: Export_Blogs
  },
  {
    path : '/followers',
    name : 'followers',
    component : Followers_page
  },
  {
    path : '/following',
    name : 'following',
    component : Following_page,
  },
  {
    path : '/login',
    name:  'login',
    component: Login_page
  },
  {
    path : '/search',
    name : 'search',
    component : Search_results,
    props: true
  },
  {
    path : '/sign_up',
    name:  'sign_up',
    component: Signup_page
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
