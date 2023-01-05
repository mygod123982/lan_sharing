<!--
 * Layouts\components-header
 * @author: zrhooks
 * @since: 2022-07-15
 * header.vue
-->
<template>
  <div class="Layouts_components_header">
    <div class="icons">
      <n-icon-wrapper
        :size="18"
        :border-radius="9"
        color="#ed4c54"
        class="icon_close_wrap"
        @click="close_window"
        @mouseleave="BackElhide('icon_close', 'icon_close_wrap', '#ed4c54')"
        @mouseenter="Elshow('icon_close', 'icon_close_wrap', '#ed4c54')"
      >
        <n-icon
          :size="16"
          color="#fff"
          :component="CloseSharp"
          class="icon_close hide"
        />
      </n-icon-wrapper>
      <n-icon-wrapper
        :size="18"
        :border-radius="9"
        color="#a365c9"
        class="icon_mini_wrap"
        @click="min_window"
        @mouseleave="BackElhide('icon_mini', 'icon_mini_wrap', '#a365c9')"
        @mouseenter="Elshow('icon_mini', 'icon_mini_wrap', '#a365c9')"
      >
        <n-icon
          :size="16"
          color="#fff"
          :component="MinimizeRound"
          class="icon_mini hide"
        />
      </n-icon-wrapper>
    </div>
  </div>
</template>

<script setup >
import { onMounted, nextTick } from "vue";
import { NIcon, NIconWrapper } from "naive-ui";
import { CloseSharp } from "@vicons/ionicons5";
import { MinimizeRound } from "@vicons/material";
import anime from "animejs/lib/anime.es.js";

const BackElhide = (className, wrapperClassName, color) => {
  try {
    console.log(`${className} hide`);
    anime({
      targets: `.${wrapperClassName}`,
      backgroundColor: color,
      duration: 100,
      easing: "easeInOutQuad",
    });

    anime({
      targets: `.${className}`,
      scale: 0,
      delay: 100,
      easing: "spring(1, 80, 10, 0)",
    });
  } catch (e) {
    console.log("hide error:", e);
  }
};

const Elshow = (className, wrapperClassName, color) => {
  try {
    console.log(`${className} show`);
    anime({
      targets: `.${wrapperClassName}`,
      backgroundColor: '#fff',
      duration: 100,
      easing: "easeInOutQuad",
    });

    anime({
      targets: `.${className}`,
      scale: 1,
      delay: 100,
      color: color,
      easing: "spring(1, 80, 10, 0)",
    });
  } catch (e) {
    console.log(e);
  }
};

onMounted(() => {
  BackElhide("icon_close", "icon_close_wrap", "#ed4c54");
  BackElhide("icon_mini", "icon_mini_wrap", "#a365c9");
});

const min_window = () => {
  window.pywebview.api.min_win()
}

const close_window = () => {
  window.pywebview.api.close_win()
}
</script>

<style scoped lang="scss">
.Layouts_components_header {
  width: 100%;
  height: 100%;
  display: grid;
  padding: 5px 10px;
  box-sizing: border-box;
  grid-template-columns: 140px 1fr;
  grid-template-rows: 1fr;
  grid-gap: 10px;
  align-content: space-around;
  align-items: center;

  .icons {
    background-color: #333;
    border-radius: 20px;
    height: 100%;
    text-align: left;
    display: flex;
    align-content: space-around;
    align-items: center;
    justify-content: center;
    .n-icon-wrapper {
      margin-right: 10px;
    }
  }
}
</style>
