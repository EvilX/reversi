/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': '[iI]gnored' }] */
import Vue from 'vue'

const socketUrl = 'ws://172.17.192.225:8081'

export default class ReveriAPI {
  constructor (app) {
    this.app = app
    this.field = []
    this.authenticated = false
    this.connect()
  }

  connect () {
    let self = this
    this.authenticated = false
    this.socket = new WebSocket(socketUrl)
    this.socket.addEventListener('open', function () {
      console.log('Connected')
    })
    this.socket.addEventListener('close', function () {
      if (self.authenticated) {
        self.app.$router.replace('/login')
      } else {
        self.connect()
      }
    })
    this.socket.addEventListener('message', function (event) {
      self.receiveData(self, event)
    })
  }

  remoteMethodCall (methodName, payload) {
    this.socket.send(JSON.stringify({
      'method': methodName,
      'payload': payload
    }))
  }

  login (username) {
    this.remoteMethodCall('login', {
      'username': username
    })
  }

  newGame () {
    this.remoteMethodCall('new_game', {})
  }

  enterGame (gameUUID) {
    this.remoteMethodCall('enter_game', {
      game_uuid: gameUUID
    })
  }

  exitGame () {
    this.remoteMethodCall('exit', {})
    this.app.state.inGame = false
  }

  chat (message) {
    this.remoteMethodCall('chat', {
      'text': message
    })
  }

  turn (x, y) {
    if (this.index !== this.order) {
      return
    }
    this.remoteMethodCall('turn', {
      'x': x,
      'y': y
    })
  }

  receiveData (sender, event) {
    let msg = JSON.parse(event.data)

    if (msg['message'] === 'start' && !sender.authenticated) {
      sender.processStart(sender, sender.app.state, msg['payload'])
    }

    if (msg['message'] === 'dashboard') {
      sender.app.$router.replace('/')
      sender.app.state.game.messages = []
    }

    // Rooms
    if (msg['message'] === 'rooms') {
      sender.processRooms(sender, sender.app.state, msg['payload'])
    }

    if (msg['message'] === 'room_update') {
      sender.processRoomUpdate(sender, sender.app.state, msg['payload'])
    }

    if (msg['message'] === 'room_delete') {
      sender.processRoomDelete(sender, sender.app.state, msg['payload'])
    }

    // Players
    if (msg['message'] === 'players') {
      sender.processPlayers(sender, sender.app.state, msg['payload'])
    }

    if (msg['message'] === 'player_update') {
      sender.processPlayerUpdate(sender, sender.app.state, msg['payload'])
    }

    if (msg['message'] === 'player_delete') {
      sender.processPlayerDelete(sender, sender.app.state, msg['payload'])
    }

    // Game
    if (msg['message'] === 'game_enter') {
      sender.processGameEnter(sender, sender.app.state, msg['payload'])
    }

    if (msg['message'] === 'game_start') {
      sender.processGameStart(sender, sender.app.state)
    }

    if (msg['message'] === 'game_stop') {
      sender.processGameStop(sender, sender.app.state)
    }

    if (msg['message'] === 'game_chat') {
      sender.processChat(sender, sender.app.state, msg['payload'])
    }
    if (msg['message'] === 'game_state') {
      sender.processGameState(sender, sender.app.state, msg['payload'])
    }

    if (msg['message'] === 'error') {
      sender.processError(sender, sender.app.state, msg['payload'])
    }
  }

  processStart (sender, state, payload) {
    // The first message after the user is logged in.
    state.username = payload['username']
    sender.authenticated = true
    sender.app.$router.replace('/')
  }

  processRooms (sender, state, payload) {
    state.games = payload
    state.games_count = Object.keys(state.games).length
  }

  processRoomUpdate (sender, state, payload) {
    Vue.set(state.games, payload.uuid, payload)
    state.games_count = Object.keys(state.games).length
  }

  processRoomDelete (sender, state, payload) {
    Vue.delete(state.games, payload['uuid'])
    state.games_count = Object.keys(state.games).length
  }

  processPlayers (sender, state, payload) {
    state.players = payload
    state.players_count = Object.keys(state.players).length
  }

  processPlayerUpdate (sender, state, payload) {
    Vue.set(state.players, payload.uuid, payload)
    state.players_count = Object.keys(state.players).length
  }

  processPlayerDelete (sender, state, payload) {
    Vue.delete(state.players, payload['uuid'])
    state.players_count = Object.keys(state.players).length
  }

  processGameEnter (sender, state, payload) {
    state.inGame = true
    state.game.index = payload['index']
    state.game.gameUUID = payload['game_uuid']
    state.game.running = false
    sender.app.$router.push('/game')
  }

  processGameStart (sender, state) {
    state.game.running = true
  }

  processGameStop (sender, state) {
    state.game.running = false
  }

  processChat (sender, state, payload) {
    state.game.messages.unshift({
      'author': payload['author'],
      'text': payload['text'],
      'index': state.game.messages.length + 1
    })
  }

  processGameState (sender, state, payload) {
    state.game.board = payload['board']
    state.game.score[0] = payload['score'][0]
    state.game.score[1] = payload['score'][1]
    state.game.order = payload['order'] === state.game.index
  }

  processError (sender, state, payload) {
    console.log(payload)
  }
}
