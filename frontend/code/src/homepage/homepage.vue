<template>
  <div class="row justify-content-md-center">
    <div class="col-lg-12">
      <div v-if="status == Statuses.NOT_CONNECTED">
        Not connected
        <b-btn variant="primary" @click="onConnect">
          Connect
        </b-btn>
      </div>

      <div v-if="status == Statuses.CONNECTING">
        <icon name="sync" scale="2" spin></icon>
        Connecting...
      </div>

      <div v-if="status == Statuses.CONNECTED">
        Connection: ok
      </div>

      <div v-if="status == Statuses.RUNNING">
        <div>Connection: ok</div>
        <div>Handshake: ok</div>
      </div>



      <div v-if="status == Statuses.DISCONNECTED || status == Statuses.ERROR">
        <div>
          <icon name="sync" scale="2" spin></icon>
        </div>
        <div>
          Connecting or network problems...
        </div>
        <b-btn variant="primary" @click="onConnect">
          Reconnect
        </b-btn>
      </div>

    </div>
  </div>
</template>

<script>
  import {ScreenApe, Statuses} from '../plugin/screenape'
  import uuidv4 from 'uuid/v4'

  export default {
    extends: ScreenApe,
    data () {
      return {
        Statuses: Statuses
      }
    },
    methods: {
      onConnect () {
        this.$connect()
      },
      sendCommand (name, params) {
        params = params || {}
        let commandId = uuidv4()
        let command = {
          type: 'command',
          name: name,
          command_id: commandId,
          params: params
        }
        this.$socket.sendObj(command)
      }
    },
    // created () {
    //   this.view = 'connecting'
    //   let backend = new this.$screenApeConnection(this.$root)
    //   backend.connect()

    //   this.$options.sockets.onopen = (data) => {
    //     this.view = 'connected'
    //     this.connected = true
    //     let payload = {
    //       type: 'handshake',
    //       protocol_version: '1.0'
    //     }
    //     this.$socket.send(JSON.stringify(payload))
    //     console.log('Connection established')
    //   }
    //   this.$options.sockets.onmessage = (event) => {
    //     let data = JSON.parse(event.data)
    //     if (this.handshaked) {
    //       console.log(data)
    //     } else {
    //       if (data['type'] === 'handshake' && data['result'] === 'ok') {
    //         this.handshaked = true
    //         this.browser_id = data['browser_id']
    //         console.log('Handshake ok')
    //       } else {
    //         console.log('Handshake failed, disconnecting')
    //         console.log(data)
    //         this.$disconnect()
    //       }
    //     }
    //   }
    //   this.$options.sockets.onclose = () => {
    //     console.log('Connection closed')
    //     this.connected = false
    //     this.view = 'network_problems'
    //   }
    //   this.$options.sockets.onerror = () => {
    //     console.log('Connection error')
    //     this.connected = false
    //     this.view = 'network_problems'
    //   }
    //   // this.$connect()
    // },
    components: {
    }
  }
</script>

