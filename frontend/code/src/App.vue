<template>
  <div>
    <h1>Hello!</h1>

    <div class="container" id="content_container">
      <router-view></router-view>
    </div>

    <homepage></homepage>

  </div>
</template>

<script>
  import Homepage from '@/homepage/homepage'

  export default {
    name: 'app',
    components: {
      Homepage
    }
  }
</script>
