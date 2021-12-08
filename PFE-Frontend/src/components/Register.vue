<template>
  <div class="section">
    <div class="container">
      <div class="row full-height justify-content-center">
        <div class="col-12 text-center align-self-center py-5">
          <div class="section pb-5 pt-5 pt-sm-2 text-center">
            <h6 class="mb-0 pb-3"><span>Connexion </span><span>Inscription</span></h6>
            <input class="checkbox" type="checkbox" id="reg-log" name="reg-log"/>
            <label for="reg-log"></label>
            <div class="card-3d-wrap mx-auto">
            <div class="card-3d-wrapper">
            <div class="card-front">
            <div class="center-wrap">
            <div class="section text-center">
            <h4 class="mb-4 pb-3">Connexion</h4>
            <div class="form-group">
              <input type="email" name="email" class="form-style" placeholder="Adresse e-mail" id="logemail" >
              <i class="input-icon fa fa-envelope"></i>
            </div>	
            <div class="form-group mt-4">
              <input type="password" name="password" class="form-style" placeholder="Mot de passe" id="logpass" >
              <i class="input-icon fa fa-lock"></i>
            </div>
            <div class="form-group mt-3"> <a href="#" class="btn mt-4">Envoyer</a> </div>
            <p class="mb-5 mt-4 text-center"> <a class="link" href="forgot">Mot de passe oublié?</a></p>
        </div>
      </div>
    </div>

      <div class="card-back">
        <div class="center-wrap">
          <div class="section text-center">
            <h4 class="mb-4 pb-3">Inscription</h4>
              <div class="form-group ">
                <input type="text" name="logname" class="form-style" placeholder="Nom" id="logname">
              <i class="input-icon fa fa-user" ></i>
              </div>	
              <div class="form-group mt-3">
                <input type="text" name="logemail" class="form-style" placeholder="Prénom" id="logemail" >
              <i class="input-icon fa fa-user" ></i>
              </div>	

            <div class="form-group mt-3">
              <input type="email" name="logpass" class="form-style" placeholder="Adresse e-mail" id="logpass" >
              <i class="input-icon fa fa-envelope"></i>
            </div>
            <div class="form-group mt-3">
              <input type="password" name="logpass" class="form-style" placeholder="Mot de passe" id="logpass" >
              <i class="input-icon fa fa-lock"></i>
            </div>
            <div class="form-group mt-3">
              <select id="inputCampus" class="form-style">
                <option value="" disabled selected>Sélectionne ton campus</option>
                <option value="0">Woluwe</option>
                <option value="1">Ixelles</option>
                <option value="2">Louvain-La-Neuve</option>

              </select>
              <i class=" input-icon fa fa-map-marker"></i>
            </div>
            <a href="#" class="btn mt-4">Envoyer</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>
  </div>
  </div>
</div>
</template>


<script>
export default {
  name: "Register",
  components: {
    
  },
  data() {
    return {
      prenom: "",
      nom: "",
      email: "",
      password: "",
      confirmPassword: "",
      error: "",
    };
  },
  methods: {
    async handleSubmit() {
      try {
        await fetch("http://localhost:8000/register",{
		method: 'POST',	
		body:JSON.stringify({
          firstname: this.prenom,
          lastname: this.nom,
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
<style scoped src="../assets/css/login.css"></style>