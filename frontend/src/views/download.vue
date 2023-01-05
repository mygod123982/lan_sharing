<!--
 * views-download
 * @author: zrhooks
 * @since: 2022-12-16
 * download.vue
-->
<template>
  <div class="views_download">
    <header class="views_download_header">
      方 &nbsp; 略 &nbsp; 分 &nbsp; 享
    </header>

    <main class="views_download_main">
      <div class="file_box" v-for="file in inject_shares" :key="file.dir_id">
        <div class="left">
          {{ file.name }}
        </div>
        <div class="right">
          <n-icon
            :color="downloadProcess_list[file.dir_id] ? '#eee':'#ff7400'"
            :component="CloudDownloadOutline"
            size="40"
            :disable="downloadProcess_list[file.dir_id]"
            :depth="1"
            @click="downloadFile(file.dir_id, file.name, file.type)"
          />
        </div>
        <div class="bottom">
          <div class="c_t">创建时间：{{ file.create_time }}</div>
          <div class="w_t">写入时间：{{ file.write_time }}</div>
        </div>
        <n-progress
          v-show="downloadProcess_list[file.dir_id]"
          class="progress"
          type="line"
          :color="themeVars.warningColor"
          :rail-color="changeColor(themeVars.warningColor, { alpha: 0.2 })"
          :percentage="downloadProcess_list[file.dir_id]"
          :indicator-text-color="themeVars.warningColor"
        />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from "vue";
import { io } from "socket.io-client";
import { NIcon, useThemeVars, NProgress } from "naive-ui";
import { CloudDownloadOutline } from "@vicons/ionicons5";
import { onBeforeRouteLeave } from "vue-router";
import { changeColor } from 'seemly'
import axios from "axios";
const themeVars = useThemeVars()
const url_base = location.hostname;
const socket = io(`ws://${url_base}:5001/ws_sharing`, {
  transports: ["websocket"],
});

const downloadProcess_list = ref({});
const downloadProcess = (id) => {
  return (progress) => {
    const step = Math.round((progress.loaded / progress.total) * 100);
    downloadProcess_list.value[id] = step || 1;
    console.log("id --", id);
    console.log("step --", step);
    if (step >= 100) {
      setTimeout(() => delete downloadProcess_list.value[id], 1000)
    }
  };
};

const downloadFile = async (id, name, type) => {
  if (downloadProcess_list.value[id]) return 
  downloadProcess_list.value[id] = 1
  const { data: blob } = await axios({
    url: `http://${url_base}:5001/download?id=${id}`,
    method: "get",
    responseType: "blob",
    onDownloadProgress: downloadProcess(id),
  });
  console.log(blob);
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  document.body.append(a);
  a.href = url;
  a.download = name + "." + type;
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};
const inject_shares = ref([]);

socket.on("ws_connect", ({ data }) => {
  console.log(data);
  data.forEach((element) => {
    if (element.is_pause) return
    inject_shares.value.push(element);
  });
});

socket.on("select_file_result", ({ data }) => {
  inject_shares.value = data.filter(ele => !ele.is_pause);
});

const get_latest_data = () => {
  socket.emit("notice_web");
};

setInterval(get_latest_data, 500);

onBeforeRouteLeave(() => {
  return false;
});
onUnmounted(() => {
  clearInterval(clearTimer);
  socket.offAny();
  socket.close();
});
</script>

<style>
#app {
  border-width: 0px;
}
</style>
<style scoped lang="scss">
.views_download {
  width: 100vw;
  height: 100vh;
  background-color: #2376b7;
  padding: 45px 20px 20px;
  position: relative;
  &_header {
    position: absolute;
    width: 100%;
    top: 0;
    left: 0;
    line-height: 45px;
    font-size: 20px;
    font-weight: 700;
    text-align: center;
    color: #f2f3f4;
  }

  &_main {
    width: calc(100vw - 40px);
    height: calc(100vh - 65px);
    background-color: #f0f4f3;
    border-radius: 20px;
    padding: 50px;
    box-sizing: border-box;
    overflow: hidden;
    overflow: overlay;
    position: relative;
    &::-webkit-scrollbar {
      position: absolute;
      width: 10px;
      height: 2px;
      background-color: #2376b7; /* or add it to the track */
    }

    &::-webkit-scrollbar-thumb {
      border-radius: 10px;
      box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
      background-color: rgb(123, 162, 201);
    }

    .file_box {
      display: grid;
      position: relative;
      border-radius: 7px;
      margin-bottom: 10px;
      padding: 5px;
      background-color: #fff;
      grid-template-rows: 1fr 1fr 10px;
      grid-template-columns: 1fr 100px;
      grid-template-areas:
        "a b"
        "c b"
        "d b";

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
        line-height: 30px;
        color: #c1c2c3;
      }

      & > .progress {
        position: absolute;
        bottom: -8px;
        height: 8px;
        left: 0px;
        grid-area: c;
        color: #c1c2c3;
      }
    }
  }
}
</style>
