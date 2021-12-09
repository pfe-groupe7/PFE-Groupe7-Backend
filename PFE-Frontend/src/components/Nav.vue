<template>
<div class="main">
  <nav id="navbar" class="navbar navbar">
    <a class="navbar-brand" href="/">
      <img src="../assets/images/vincilogo.png" height="100" alt="vinci market logo">
    </a>
      
      <form class="form-inline">
        <div class="flexbox">
          <div class="search">
            <div>
              <input type="text" placeholder="Recherche...">
            </div>
          </div>
        </div>
      </form>
        
        <ul class="navbar-nav ml-auto" v-if="!user">
         
          <li class="nav-item">
            <router-link to="/login" class="nav-link">Connexion</router-link>
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