<template>
  <form @submit.prevent="handleSubmit">
    <error v-if="error" :error="error" />

  <div class="login-wrap p-3 md-5">
    <div class="d-flex">
      <div class="w-100">
        <h3>S'inscrire</h3>
      </div>
    </div>
  </div>

  <div class="form-group">
    <input type="text" class="form-control" required="" v-model="Prénom" placeholder="Prénom"/>
  </div>

  <div class="form-group mt-3">
    <input type="text" class="form-control" required="" v-model="Nom" placeholder="Nom" />
  </div>
  <div class="form-group mt-3">
      <input type="email" class="form-control" v-model="email" placeholder="Email" />
  </div>
    <div class="form-group mt-3">
      <input type="email" class="form-control" v-model="Password" placeholder="Mot de passe" />
      <span toggle="#password-field" class="fa fa-fw field-icon toggle-password fa-eye"></span>

    </div>
   <div class="form-group mt-3">
      <input type="email" class="form-control" v-model="Confirm_Password" placeholder="Confirmez votre mot de passe" />
  </div>
   <div class="form-group mt-4">
    <button type="submit" class="form-control btn btn-primary rounded submit px-3">S'inscrire</button>
  </div>
  </form>
</template>


<script>
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
        await fetch("http://localhost:8000/register",{
		method: 'POST',	
		body:JSON.stringify({
          firstname: this.Prénom,
          lastname: this.Nom,
          email: this.email,
          password: this.password,	moderator:'False',
        })
		});
        this.$router.push("/login");
      } catch (e) {
        this.error = "Une erreur est survenue!";
      }
    },
  },
};
</script>
