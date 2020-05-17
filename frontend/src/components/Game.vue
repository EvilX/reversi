<template>
  <div id="game">
    <div class="row">
      <div class="col-md-5">
        <board></board>
      </div>
      <div class="col-md-7">
        <chat></chat>
      </div>
    </div>
    <div class="row">
      <div class="col-md-6">
        <button type="button" class="btn btn-danger" v-on:click="exitGame">Exit and back</button>
      </div>
    </div>
  </div>
</template>

<script>
import Board from './Board'
import Chat from './Chat'

export default {
  name: 'GameView',
  components: {
    board: Board,
    chat: Chat
  },
  methods: {
    exitGame () {
      this.$root.api.exitGame()
    }
  }
}
</script>

<style>
#game {
  margin-top: 40px;
}
</style>
