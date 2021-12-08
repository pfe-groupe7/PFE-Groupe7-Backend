import Vue from "vue";
import Router from "vue-router";
Vue.use(Router);
import Home from "./components/Home.vue";
import Register from "./components/Register.vue";
import Forgot from "./components/Forgot.vue";
import Reset from './components/Reset.vue'

export default new Router({
  mode: "history",
  routes: [
    { path: "/", component: Home },
    { path: "/register", component: Register },
    { path: "/forgot", component: Forgot },
    {path:"/reset/:token",component:Reset}
  ],
});
