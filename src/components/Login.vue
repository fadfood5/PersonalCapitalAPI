<template lang='pug'>
  Home(v-if='accounts', :accounts="accounts")
  .container(v-else)
    .login(v-if='!showTwoAuth')
      b-field(label="Email")
        b-input(maxlength="30" v-model='email' )
      b-field(label="Password")
        b-input(type="password" password-reveal="" maxlength="30" v-model='password')
      span(v-model='errorMessage')
      button.button.is-success(@click='login()') Login
    .twoauth(v-else)
      b-field(label="SMS Code")
        b-input(maxlength="4" v-model='smsCode')
      button.button.is-success(@click='submitTwoAuth()') Submit
</template>

<script>
import Home from './Home.vue';
export default {
  name: 'Login',
  components:{
    Home
  },
  data () {
    return {
      email:'',
      password:'',
      userData: null,
      errorMessage: '',
      smsCode: '',
      showTwoAuth: false,
      accounts: null
    }
  },
  methods: {
    login: function(){
      this.$http.post('http://localhost:8081/login',
        {email: this.email, password: this.password},
        {headers: {'Content-Type': 'application/json'}})
      .then(response => {
        console.log(response.data)
        this.userData = response.body;
        this.showTwoAuth = true;
      }, response => {
        // error callback
        this.errorMessage = 'Error logging in. Check email and/or password.';
      });
    },
    submitTwoAuth: function(){
      this.$http.post('http://localhost:8081/twoauth', {password: this.password, smsCode: this.smsCode}).then(response => {
        console.log(response.data);
        this.accounts = response.data.accounts;
      }, response => {
        // error callback
        this.errorMessage = 'Error logging in. Check your SMS code.';
      });
    }
  },
  created: function(){
  }
}
</script>

<style scoped>
</style>
