import Main from '@/views/main.vue'
import Download from '@/views/download.vue'
import { createRouter, createWebHashHistory } from 'vue-router'
const routes = [
    {
        name: 'main',
        path: '/index',
        component: Main,
    },
    {
        name: 'download',
        path: '/download',
        component: Download,
    },
    {
        path: '/',
        redirect: '/download'
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes, // `routes: routes` 的缩写
})

export default router