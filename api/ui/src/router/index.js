import Vue from 'vue'
import Router from 'vue-router'
import Reports from '@/components/Reports'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Reports',
      component: Reports
    },
    {
      path: '/reports',
      name: 'Reports',
      component: Reports
    },
    {
      path: '/reports/:community_id',
      name: 'Reports',
      component: Reports
    }
  ]
})
