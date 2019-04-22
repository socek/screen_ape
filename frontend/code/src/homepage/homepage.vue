<template>
  <div class="row justify-content-md-center">
    <div class="col-lg-12">
      <div v-if="status == Statuses.NOT_CONNECTED">
        Not connected
        <b-btn variant="primary" @click="startConnection">
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

        <b-btn variant="primary" @click="sendMessage">
          Send Sample Message
        </b-btn>
      </div>

      <div v-if="status == Statuses.DISCONNECTED || status == Statuses.ERROR">
        <div>
          Connecting or network problems...
        </div>
        <b-btn variant="primary" @click="startConnection">
          Reconnect
        </b-btn>
      </div>

    </div>
  </div>
</template>

<script>
  import {ScreenApe} from '../plugin/screenape'

  export default {
    extends: ScreenApe,
    methods: {
      sendMessage () {
        this.sendJSON({
          type: 'action',
          name: 'zupa'
        })
      }
    }
  }
</script>
