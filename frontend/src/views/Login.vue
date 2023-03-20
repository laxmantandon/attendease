<template>
  <v-container fluid fill-height class="mt-10">
    <v-row justify="center" align="center">
      <v-col cols="12" xs="11" sm="10" md="6" lg="4" xl="6">
        <v-sheet elevation="10" class="ma-6 pa-6" rounded="lg">
        <h2>Sign-in</h2>
        <br>
          <v-form ref="form">
            <v-text-field variant="outlined" v-model="email" :rules="emailRules" label="Email" required
              append-inner-icon="mdi-account"
            ></v-text-field>

            <v-text-field variant="outlined" v-model="password" :rules="passRules" label="Password"
            :append-inner-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
            :type="show1 ? 'text' : 'password'"
            @click:append-inner="show1 = !show1"
              required></v-text-field>

            <v-checkbox v-model="checkbox" :rules="[v => !!v || 'You must agree to continue!']" label="Do you agree?"
              required></v-checkbox>

            <div class="d-flex flex-column">
              <v-btn color="success" class="mt-4" block @click="login">
                Login
              </v-btn>

            </div>
          </v-form>
        </v-sheet>
      </v-col>
    </v-row>
    <v-snackbar  v-model="snack" :timeout="5000" :color="snackColor" location="top right">
					{{ snackText }}
    </v-snackbar>
  </v-container>

</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      snack: false,
			snackColor: "",
			snackText: "",
      show1: false,
      email: null,
      password: null,
      valid: true,
      name: '',
      emailRules: [
        v => !!v || 'Email Id is required',
        v => ((/^[a-z.-]+@[a-z.-]+\.[a-z]+$/i.test(v))) || 'Invalid Email Id',
      ],
      passRules: [
        v => !!v || 'Password is required',
      ],
      select: null,
      items: [
        'Item 1',
        'Item 2',
        'Item 3',
        'Item 4',
      ],
      checkbox: false,
    };
  },
  inject: ["$auth"],
  async mounted() {
    if (this.$route?.query?.route) {
      this.redirect_route = this.$route.query.route;
      this.$router.replace({ query: null });
    }
  },
  methods: {
    async login() {
      const { valid } = await this.$refs.form.validate()
      if (valid) {
        if (this.email && this.password) {
          let req = {
            usr: this.email,
            pwd: this.password
          }
          await axios.post('/api/method/login', req)
            .then(r => {
              if (r.status === 200){
                this.snack = true;
                this.snackColor = 'green';
                this.snackText = 'Login Success';
                this.$auth.isLoggedIn = true;
                this.$router.push({ name: "Home" });
              }
            })
            .catch(e => {
              this.snack = true;
              this.snackColor = 'red';
              this.snackText = e.response.data.message;
            })
          // let res = await this.$auth.login(this.email, this.password);
          // console.log(res)
          // if (!res.exc) {
          //   this.$router.push({ name: "Home" });
          // } else{
          //   alert("wrong credentials")
          // }
        }
      }

    },
  },
};
</script>
