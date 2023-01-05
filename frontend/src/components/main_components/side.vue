<!--
 * components\main_components-side
 * @author: zrhooks
 * @since: 2022-10-24
 * side.vue
-->
<template>
  <div class="components_main_components_side">
    <n-button type="info" @click="openFileDialog" :disabled="!is_share">
      <template #icon>
        <n-icon>
          <share-outline></share-outline>
        </n-icon>
      </template>
      选择文件分享
    </n-button>

    <n-switch @update-value="updatefn" :default-value="true" :value="is_share" size="large" :rail-style="checkStyle" />
  </div>
</template>

<script setup >
import { NIcon, NButton, NSwitch, useMessage} from "naive-ui";
import { ShareOutline } from "@vicons/ionicons5";
import {ref, inject} from 'vue'
const isOpen = ref(false)
const message = useMessage()
const is_share = inject("is_share")
const change_is_share = inject('change_is_share')
const checkStyle = ({focused, checked}) => {
  const style = {};
  !checked ? (style.background = "#d03050") :  (style.background = "#2080f0")
  return style;
};

const openFileDialog = async (e) => {
  if (isOpen.value) return
  isOpen.value = true
  setTimeout(() => isOpen.value = false, 4000)
  const val = await window.pywebview.api.open_file_dialog()
  isOpen.value = false
  if (!val) return 
  message.warning("文件已经分享了")
}


const updatefn = (val) => {
  console.log('switch val:', val)
  change_is_share(val)
}

</script>

<style scoped>
.components_main_components_side {
  height: 45px;
  width: 100%;
  margin-right: 20px;
  border-radius: 10px;
  display: grid;
  justify-items: right;
  align-items: center;
  grid-template-columns: 1fr 150px 20px;
}
</style>
