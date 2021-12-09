<template>
<div class="main">
  <nav id="navbar" class="navbar ">
    <a class="navbar-brand" href="/">
      <img src="../assets/images/vincilogo.png" height="100" alt="vinci market logo">
    </a>
      <div class="nav-item dropdown">
          <a class="btn mt-1 nav-link dropdown-toggle" data-toggle="dropdown">Catégories</a>
          <div class="dropdown-menu">
            <a href="#" class="dropdown-item">Maison et jardin</a>
            <a href="#" class="dropdown-item"> Famille</a>
            <a href="#" class="dropdown-item">Vêtements et accessoires</a>
            <a href="#" class="dropdown-item">Loisirs et hobbys</a>
            <a href="#" class="dropdown-item">Electronique</a>
          </div>
			</div>
      <form class="form-inline">
        <div class="flexbox">
          <div class="search">
            <div>
              <input type="text" placeholder="Recherche...">
            </div>
          </div>
        </div>
      </form>
        <router-link to="/createAd"><a class="btn mt-1">
         Publier une annonce &nbsp; <i class="fa fa-paper-plane" aria-hidden="true"></i></a>
</router-link>
        <ul class="navbar-nav ml-auto" v-if="!user">
          <li class="nav-item">
            <router-link to="/login" class="nav-link"><i id="userIcon" class="fa fa-user-circle" aria-hidden="true"></i></router-link>
          </li>
        </ul>
           <ul class="navbar-nav ml-auto" v-if="user">
          <li class="nav-item">
            <a href="javascript:void(0)" @click="handleClick" class="nav-link">Déconnecter</a>
          </li>
        </ul>
  </nav>
</div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: 'Nav',
  methods:{
     handleClick(){
       localStorage.removeItem('token');
       this.$store.dispatch('user',null);
       this.$router.push('/');
     }
  },
  computed:{
    ...mapGetters(['user'])
  }
  
}
</script>
<style scoped src="../assets/css/navbar.css"></style>