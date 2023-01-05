<!--
 * Layouts-index
 * @author: zrhooks
 * @since: 2022-07-14
 * index.vue
-->
<template>
  <n-layout>
    <n-message-provider>
      <n-layout-header class="app-header pywebview-drag-region">
        <header-vue></header-vue>
      </n-layout-header>
      <n-layout-content class="app-content" content-style="padding: 10px;">
        <slot></slot>
      </n-layout-content>
    </n-message-provider>
  </n-layout>
</template>

<script setup >
import {
  NMessageProvider,
  NLayout,
  NLayoutHeader,
  NLayoutSider,
  NLayoutContent,
  NButton,
} from "naive-ui";

import headerVue from "./components/header.vue";
</script>

<style scoped>
.app-header {
  padding: 5;
  height: 40px;
  display: flex;

  margin-bottom: 10px;
}

.app-content {
  height: calc(100vh - 40px - 10px);
}

.n-layout {
  background-color: unset;
}
</style>
