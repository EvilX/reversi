<template>
  <div class="row">
    <div class="col-lg-12">
      <span class="red">&nbsp;</span><span class="score">{{ $root.state.game.score[0] }}</span><span class="score" v-if="$root.state.game.index === 0">(You)</span>&nbsp;&nbsp;&nbsp;
      <span class="blue">&nbsp;</span><span class="score">{{ $root.state.game.score[1] }}</span><span class="score" v-if="$root.state.game.index === 1">(You)</span>

      <div class="row" v-if="!$root.state.game.running">
        <div class="col-md-12">
          <span class="turn">Waiting the second player...</span>
        </div>
      </div>

      <div class="row" v-if="$root.state.game.running">
        <div class="col-md-12">
          <span v-if="$root.state.game.order" class="turn">Your turn</span>
          <span v-else-if="!$root.state.game.order" class="turn">Wait...</span>
        </div>
      </div>

      <div class="row" v-if="$root.state.game.running">
        <div class="col-md-12">
          <div class="board">
            <div class="line" v-for="line in $root.state.game.board" v-bind:key="line.line">
              <div class="cell" v-for="cell in line.values" v-bind:key="cell.index" v-on:click="clickCell(cell.x, cell.y)">
                <div class="red" v-if="cell.value === 0">&nbsp;</div>
                <div class="blue" v-else-if="cell.value === 1">&nbsp;</div>
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
  name: 'Board',
  methods: {
    clickCell (x, y) {
      if (this.$root.state.game.order) {
        this.$root.api.turn(x, y)
      }
    }
  }
}
</script>

<style scoped>
  .board {
    width: 250px;
    margin: 20px;
    padding: 3px;
  }

  .board .line {
    height: 30px;
    float: left;
  }

  .board .line .cell {
    width: 30px;
    height: 30px;
    border: 1px solid #aaaaaa;
    float: left;
    text-align: center;
    padding-top: 4px;
  }

  .red {
    height: 20px;
    width: 20px;
    background-color: red;
    border-radius: 50%;
    display: inline-block;
  }
  .blue {
    height: 20px;
    width: 20px;
    background-color: blue;
    border-radius: 50%;
    display: inline-block;
  }
  .score {
    font-size: 1.2em;
    font-weight: bold;
    margin-left: 5px;
  }
  .turn {
    margin: 20px 0px;
    font-size: 1.2em;
    font-weight: bold;
  }
</style>
