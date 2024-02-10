import { createApp } from "vue/dist/vue.esm-bundler";
import './style.css'

import HelloWorldVue from './components/HelloWorld.vue';

const app = createApp({})
app.component('hello-world-vue', HelloWorldVue);

app.mount('#app')
