// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import VueResource from 'vue-resource'
import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon'
import VueNativeSock from 'vue-native-websocket'

import App from '@/App'
import router from '@/routing'
import store from '@/store'
// import ScreenApe from '@/plugin/screenape'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = true
Vue.use(BootstrapVue)
Vue.use(VueResource)
Vue.component('icon', Icon)

Vue.use(VueNativeSock, 'ws://' + window.location.hostname + '/gateway', {
  connectManually: true
})

// Vue.use(ScreenApe)

/* eslint-disable no-new */
export default new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
})
