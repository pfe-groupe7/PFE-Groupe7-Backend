<template>
  <form @submit.prevent="handleSubmit">
    <error v-if="error" :error="error" />

    <h3>S'inscrire</h3>

    <div class="form-group">
      <label>Prénom</label>
      <input
        type="text"
        class="form-control"
        v-model="Prénom"
        placeholder="Prénom"
      />
    </div>

    <div class="form-group">
      <label>Nom</label>
      <input type="text" class="form-control" v-model="Nom" placeholder="Nom" />
    </div>
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
      <label>Password</label>
      <input
        type="password"
        class="form-control"
        v-model="password"
        placeholder="Mot de passe"
      />
    </div>
    <div class="form-group">
      <label>Confirm Password</label>
      <input
        type="password"
        class="form-control"
        v-model="Confirm_Password"
        placeholder="Confirmer le mot de passe"
      />
    </div>
    <button class="btn btn-primary btn-block">S'inscrire</button>
  </form>
</template>


<script>
import axios from "axios";
import Error from "./Error.vue";
export default {
  name: "Register",
  components: {
    Error,
  },
  data() {
    return {
      Prénom: "",
      Nom: "",
      email: "",
      password: "",
      Confirm_Password: "",
      error: "",
    };
  },
  methods: {
    async handleSubmit() {
      try {
        await axios.post("register", {
          Prénom: this.Prénom,
          Nom: this.Nom,
          email: this.email,
          password: this.password,
          Confirm_Password: this.Confirm_Password,
        });
        this.$router.push("/login");
      } catch (e) {
        this.error = "Une erreur est survenue!";
      }
    },
  },
};
</script>
