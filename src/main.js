import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
//import Buefy from 'buefy'
//import 'buefy/dist/buefy.css'
import vuetify from './plugins/vuetify'
import VueLetterAvatar from 'vue-letter-avatar';



Vue.config.productionTip = false
Vue.use(VueLetterAvatar);
//Vue.use(Buefy)
//Vue.use(Vuetify)

new Vue({
  router,
  store,
  vuetify,
  render: function (h) { return h(App) }
}).$mount('#app')
