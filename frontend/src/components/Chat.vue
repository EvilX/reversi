<template>
  <div class="row">
    <div class="col-md-12">
      <div class="row">
        <div class="col-md-12 chat-messages">
          <p v-for="message in $root.state.game.messages" v-bind:key="message.index">
            <strong v-if="message.author">{{ message.author }}&nbsp;</strong>{{ message.text }}
          </p>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <form @submit.prevent="handleMessage">
            <div class="row" style="margin-top: 20px;">
              <div class="col">
                <input type="text" v-model="message" class="form-control" id="message" placeholder="Message" v-on:click="handleMessage">
              </div>
              <div class="col">
                <button type="submit" class="btn btn-primary">Send</button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Chat',
  data () {
    return {
      'message': ''
    }
  },
  methods: {
    handleMessage () {
      if (this.message.trim()) {
        this.$root.api.chat(this.message)
        this.message = ''
      }
    }
  }
}
</script>

<style scoped>
  .chat-messages {
    height: 300px;
    overflow-y: auto;
  }
</style>
