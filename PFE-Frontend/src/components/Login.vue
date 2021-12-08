<template>
  <form @submit.prevent="handleSubmit">

    <error v-if="error" :error="error"/>
    <h3>Connecter</h3>

    <div class="form-group">
      <label>Email</label>
      <input
        type="email"
        class="form-control"
        v-model="email"
        placeholder="Email"
      />
    </div>
    <div class="form-group">
      <label>Mot de passe</label>
      <input
        type="password"
        class="form-control"
        v-model="password"
        placeholder="Mot de passe"
      />
    </div>

    <button class="btn btn-primary btn-block">Connecter</button>

    <p class="forgot-password text-right">
      <router-link to="forgot">Mot de passe oublié?</router-link>
    </p>
  </form>
</template>

<script>
import Error from './Error.vue';
import {//DevURL,
PordURL
} from '../config';
export default {
  name: 'Login',
  components: {
    Error,
  },
  data() {
    return {
      email: '',
      password: '',
      error: '',
    };
  },
  methods: {
    async handleSubmit() {
      try {
		await fetch(PordURL+"login",{
		method: 'POST',	
		body:JSON.stringify({
          email: this.email,
          password: this.password,
        })}).then(response => response.json())
  .then(data => {localStorage.setItem("token", data.token);
        this.$store.dispatch("user", data.user);});
        this.$router.push("/");
      } catch (e) {console.log(e)
        this.error = 'Email ou mot de passe invalide!';
      }
    },
  },
};
</script>
