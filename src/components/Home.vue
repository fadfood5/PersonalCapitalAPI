<template lang='pug'>
  .container
    h1 Accounts
    .tile.is-vertical.left(v-for='i in accounts')
        .card
            .tile
                .tile.is-vertical
                    h4 {{i.name}}
                    h5 {{i.accountType}}
                .tile.is-pulled-right
                    h6 {{i.balance}}
</template>

<script>
export default {
  name: 'hello',
  data () {
    return {
    }
  },
  methods: {
  },
  created: function(){
  },
  props: ['accounts']
}
</script>

<style scoped>
.left{
    text-align: left;
}
</style>
