<!--
 * views-main
 * @author: zrhooks
 * @since: 2022-12-16
 * main.vue
-->
<template>
  <div class="views_main">
    <my-layouts>
      <my-main></my-main>
    </my-layouts>
  </div>
</template>

<script setup >
import myLayouts from '@/Layouts/index.vue'
import myMain from '@/components/main.vue'
import { io } from "socket.io-client";
import {computed, nextTick, provide, ref, onUnmounted} from 'vue'

const inject_shares = ref([])
const is_share = ref(true)
const is_share_lock = ref(false)
const socket = io("ws://127.0.0.1:5001/ws_sharing", {
  transports: ["websocket"]
});

const update_file = ( id, is_del = true) => {
  socket.emit("update_file_status", {
    id,
    is_del
  })
}

const change_is_share = (val) => {
  // is_share.value = !val
  socket.emit("change_share", val)
}

provide('files_list', inject_shares)
provide("update_file", update_file)
provide("is_share", computed(() => is_share.value))
provide("change_is_share", change_is_share)

socket.on('ws_connect', ({data}) => {
  console.log(data)
  data.forEach(element => {
    inject_shares.value.push(element)
  });
})

socket.on("select_file_result", ({data}) => {
  inject_shares.value = data
})

socket.on("change_share", ({data}) => {
  console.log("change_前", is_share.value)
  if (is_share_lock.value) return
  is_share_lock.value = true
  nextTick(() => is_share_lock.value = false)
  console.log("想要改变", !!data)
  is_share.value = !!data
  console.log("change_后", is_share.value)
})

const get_latest_data = () => {
  socket.emit('notice_web')
}

let clearTimer = setInterval(get_latest_data, 500)

onUnmounted(() => {
    clearInterval(clearTimer)
    socket.offAny()
    socket.close()
})
</script>

<style scoped></style>
