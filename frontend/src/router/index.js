import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/components/HomeView.vue'
import LoginView from '@/components/LoginView.vue'
import RegisterView from '@/components/RegisterView.vue'

import AdminDashboard from '@/components/AdminDashboard.vue'
import CreateLot from '@/components/CreateLot.vue'
import EditLot from '@/components/EditLot.vue'
import ViewUsers from '@/components/ViewUsers.vue'

import UserDashboard from '@/components/UserDashboard.vue'
import UserReservation from '@/components/UserReservation.vue'
import ReleaseReservation from '@/components/ReleaseReservation.vue'

import UserSummary from '@/components/UserSummary.vue'
import AdminSummary from '@/components/AdminSummary.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/admin-dashboard',
      name: 'admin-dashboard',
      component: AdminDashboard
    },
    {
      path: '/create-lot',
      name: 'create-lot',
      component: CreateLot
    },
    {
      path: '/edit-lot/:id',
      name: 'edit-lot',
      component: EditLot
    },
    {
      path: '/view-users',
      name: 'view-users',
      component: ViewUsers
    },
    {
      path: '/user-dashboard',
      name: 'user-dashboard',
      component: UserDashboard
    },
    {
      path: '/reserve/:lotId',
      name: 'reserve',
      component: UserReservation
    },
    {
      path: '/release/:reservationId',
      name: 'release-reservation',
      component: ReleaseReservation
    },
    {
      path: '/user-summary',
      name: 'user-summary',
      component: UserSummary
    },
    {
      path: '/admin-summary',
      name: 'admin-summary',
      component: AdminSummary
    }
  ],
})

export default router
