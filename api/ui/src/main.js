// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App';
import router from './router';

Vue.use(ElementUI);

// TODO - Put this in a settings file
if (window.webpackHotUpdate) {
    // dev server
    Vue.prototype.backendEndpoint = '//localhost:8080/'
} else {
    Vue.prototype.backendEndpoint = '/'
}

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    components: { App },
    template: '<App/>'
})
