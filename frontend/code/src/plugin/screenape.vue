<script>
export const Statuses = {
  NOT_CONNECTED: 0,
  CONNECTING: 1,
  CONNECTED: 2, // conected but not handshaked
  RUNNING: 3,
  DISCONNECTED: 4,
  ERROR: 5
}

export const MessageTypes = {
  HANDSHAKE: 'handshake',
  ACTION: 'action',
  COMMAND_STATUS: 'command_status'
}

class MessageHandler {
  constructor (component, data) {
    this.component = component
    this.payload = JSON.parse(event.data)
  }

  _validateHandshake () {
    return this.payload['type'] === MessageTypes.HANDSHAKE && this.payload['result'] === 'ok'
  }

  _isConnectionRunning () {
    return this.component.status === Statuses.RUNNING
  }

  _isAction () {
    return this.payload['type'] === MessageTypes.ACTION
  }

  _isCommandStatus () {
    return this.payload['type'] === MessageTypes.COMMAND_STATUS
  }

  _parseAction () {
    console.log('Action!', this.payload)
  }

  _commandStatus () {
    console.log('Command Status!', this.payload)
  }

  parse () {
    if (this._isConnectionRunning()) {
      if (this._isAction()) {
        this._parseAction()
      } else if (this.isCommand()) {
        this._commandStatus()
      }
    } else {
      if (this._validateHandshake()) {
        this.component.setStatus('RUNNING', 'Handshake is ok')
      } else {
        this.component.setStatus('DISCONNECTED', 'Handshake failed')
        this.component.$disconnect()
      }
    }
  }
}

export let ScreenApe = {
  data () {
    return {
      status: Statuses.NOT_CONNECTED
    }
  },
  created () {
    this.$options.sockets.onopen = (data) => {
      this.sendJSON({
        type: 'handshake',
        protocol_version: '1.0'
      })
      this.setStatus('ESTABLISHED', 'Connection established')
    }

    this.$options.sockets.onclose = () => {
      this.setStatus('DISCONNECTED', 'Disconnected')
    }

    this.$options.sockets.onerror = () => {
      this.setStatus('ERROR', 'Lost connection!')
    }

    this.$options.sockets.onmessage = (event) => {
      (new MessageHandler(this, event.data)).parse()
    }
  },
  methods: {
    sendJSON (payload) {
      return this.$socket.send(JSON.stringify(payload))
    },
    setStatus (status, message) {
      this.status = Statuses[status]
      if (message) { console.log(message) }
    },
    startConnection () {
      this.$connect()
    }
  }
}
</script>
