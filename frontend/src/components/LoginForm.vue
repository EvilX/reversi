<template>
  <div id="login">
    <div class="row justify-content-md-center">
      <div class="col-md-6 panel">
        <h2>Enter the game</h2>
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <input type="text" v-model="username" class="form-control" id="username" placeholder="Enter your name">
          </div>
          <button type="submit" class="btn btn-primary">Start!</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'LoginForm',
  components: {},
  data () {
    return {
      'username': ''
    }
  },
  methods: {
    handleLogin () {
      this.$root.api.login(this.username)
    }
  }
}
</script>

<style>
</style>
