<!--
 * components-main
 * @author: zrhooks
 * @since: 2022-10-21
 * main.vue
-->
<template>
  <div class="components_main">
    <my-side></my-side>
    <my-content></my-content>
  </div>
</template>

<script setup >
import mySide from './main_components/side.vue'
import myContent from './main_components/content.vue'
</script>

<style scoped lang="scss">
.components_main {
  background-color: #f2f4f6;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 0px 20px 20px;
  box-sizing: border-box;
  border-radius: 10px;
}

</style>
