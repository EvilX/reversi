<template>
  <div id="login">
    <div class="row justify-content-md-center">
      <div class="col-md-8">
        <button type="button" class="btn btn-primary float-right" v-on:click="newGame">New game</button>
        <h2>Games</h2>
        <table class="table" v-if="$root.state.games_count > 0">
            <tr>
              <th>Players</th>
              <th>&nbsp;</th>
            </tr>
            <tr v-for="game in $root.state.games" v-bind:key="game.uuid">
                <td>
                    <span v-for="player in game.players" v-bind:key="player.uuid">{{ player.username }}<br/></span>
                </td>
                <td>
                    <button v-if="!game.is_running" type="button" class="btn btn-light" v-on:click="selectGame(game.uuid)">Enter</button>
                </td>
            </tr>
        </table>
        <table class="table" v-else>
            <tr>
                <td>No games. Create a new one.</td>
            </tr>
        </table>
      </div>
      <div class="col-md-4">
        <h2>Players online ({{ $root.state.players_count }})</h2>
        <table class="table" v-if="$root.state.players_count > 0">
          <tr v-for="player in $root.state.players" v-bind:key="player.uuid">
            <td>{{ player.username }}</td>
          </tr>
        </table>
        <table class="table" v-else>
            <tr>
                <td>No players online.</td>
            </tr>
        </table>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Dashboard',
  components: {},
  methods: {
    newGame () {
      this.$root.api.newGame()
    },
    selectGame (gameUUID) {
      this.$root.api.enterGame(gameUUID)
    }
  }
}
</script>

<style>
</style>
