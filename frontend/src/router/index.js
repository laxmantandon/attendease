import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Company from "../views/Company.vue";
import Employee from '../views/Employee.vue'
import Attendance from '../views/Attendance.vue'
import authRoutes from './auth';

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/company",
    name: "Company",
    component: Company,
  },
  {
    path: "/employee",
    name: "employee",
    component: Employee,
  },
  {
    path: "/attendance",
    name: "Attendance",
    component: Attendance,
  },
  
  ...authRoutes,
];

const router = createRouter({
  base: "/frontend/",
  history: createWebHistory(),
  routes,
});

export default router;
