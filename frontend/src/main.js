// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import VueRouter from 'vue-router'
import GameView from './components/Game'
import Dashboard from './components/Dashboard'
import LoginForm from './components/LoginForm'
import ReveriAPI from './api'

Vue.config.productionTip = false
Vue.use(VueRouter)

const routes = [
  { name: 'Game', path: '/game', component: GameView },
  { name: 'Login', path: '/login', component: LoginForm },
  { name: 'Dashboard', path: '/', component: Dashboard }
]

const router = new VueRouter({
  routes
})

const app = new Vue({
  router,
  data () {
    return {
      api: new ReveriAPI(this),
      state: {
        inGame: false,
        game: {
          index: undefined,
          running: false,
          board: [],
          score: [0, 0],
          order: false,
          messages: []
        },
        games: {},
        games_count: 0,
        players: {},
        players_count: 0,
        username: ''
      }
    }
  }
}).$mount('#app')

router.beforeEach((to, from, next) => {
  if (to.name === 'Login' && app.api) {
    console.log(app.api)
    app.api.connect()
    next()
  }
  if (to.name !== 'Login' && !app.api.authenticated) {
    next({name: 'Login'})
  } else if (from.name === 'Game' && app.api.authenticated && app.state.inGame) {
    app.api.exitGame()
  } else {
    next()
  }
})

if (router.currentRoute.path !== '/login') {
  router.replace('/login')
}
