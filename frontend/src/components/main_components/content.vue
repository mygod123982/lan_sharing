<!--
 * components\main_components-content
 * @author: zrhooks
 * @since: 2022-10-24
 * content.vue
-->
<template>
  <div class="components_main_components_content">
    <div class="file_box" v-for="file in files_list" :key="file.dir_id">
      <div class="left">
        {{ file.name }}
      </div>
      <div class="right">
        <n-icon
          color="#ff7400"
          :component="file.is_pause ? 
                      NotStartedOutlined:
                      PauseCircleOutline"
          size="40"
          :depth="1"
          @click="update_file(file.id, false)"
        />
        <n-icon
          color="#ff7400"
          :component="CloseCircleOutline"
          size="40"
          :depth="1"
          @click="update_file(file.dir_id, true)"
        />
      </div>
      <div class="bottom">
        <div class="c_t">创建时间：{{ file.create_time }}</div>
        <div class="w_t">写入时间：{{ file.write_time }}</div>
      </div>
    </div>
    <slot name="default"></slot>
  </div>
</template>

<script setup >
import { NIcon } from "naive-ui";
import {NotStartedOutlined} from '@vicons/material'
import { PauseCircleOutline, CloseCircleOutline } from "@vicons/ionicons5";
import { inject, watchEffect } from "vue";
const files_list = inject("files_list");
const update_file = inject("update_file")

watchEffect(files_list, () => {
  console.log(files_list.value);
});


console.log("inject_shares", files_list.value.length);
</script>

<style scoped lang="scss">
.components_main_components_content {
  width: 100%;
  height: calc(100% - 45px);
  background-color: #eee;
  overflow: hidden;
  overflow: overlay;
  padding-right: 10px;
  &::-webkit-scrollbar {
    width: 5px;
    height: 2px;
    background-color: #fff; /* or add it to the track */
  }

  &::-webkit-scrollbar-thumb {
    border-radius: 10px;
    box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
    background-color: rgb(123, 162, 201);
  }

  .file_box {
    display: grid;
    border-radius: 7px;
    margin-bottom: 10px;
    padding: 5px;
    background-color: #fff;
    grid-template-rows: 1fr 1fr;
    grid-template-columns: 1fr 100px;
    grid-template-areas:
      "a b"
      "c b";

    & > .left {
      grid-area: a;
      font-size: 18px;
      line-height: 30px;
      font-weight: 600;
      color: #2080f0;
    }

    & > .right {
      grid-area: b;
      grid-template-columns: 1fr 1fr;
      display: grid;
      align-items: center;
    }

    & > .bottom {
      grid-area: c;
      display: grid;
      grid-template-columns: 1fr 1fr;
      font-size: 12px;
      line-height: 24px;
      color: #c1c2c3;
    }
  }
}
</style>
