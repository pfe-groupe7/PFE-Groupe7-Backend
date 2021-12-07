<template>
  <form @submit.prevent="handleSubmit">
    <h3>Réinitialiser le mot de passe</h3>

    <div class="form-group">
      <label>Mot de passe</label>
      <input
        type="password"
        class="form-control"
        v-model="password"
        placeholder="Mot de passe"
      />
    </div>
    <div class="form-group">
      <label>Confirmer Mot de passe</label>
      <input
        type="password"
        class="form-control"
        v-model="confirm_password"
        placeholder="Mot de passe"
      />
    </div>

    <button class="btn btn-primary btn-block">Changer</button>
  </form>
</template>


<script>
import axios from "axios";

export default {
  name: "Reset",
  data() {
    return {
      password: "",
      confirm_password: "",
    };
  },
  methods: {
    async handleSubmit() {
      const response = await axios.post("reset", {
        password: this.password,
        confirm_password:this.confirm_password,
        token:this.$route.params.token
      });
      console.log(response);
      this.$router.push('/login');

    },
  },
};
</script>
