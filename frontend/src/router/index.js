import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Department from "../views/Department.vue";
import Location from "../views/Location.vue";
import Shift from "../views/Shift.vue";
import Analytics from "../views/Analytics.vue";
import Employee from '../views/Employee.vue';
import Attendance from '../views/Attendance.vue';
import Engagement from "../views/Engagement.vue";
import authRoutes from './auth';
import Company from '../views/Company.vue';

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/location",
    name: "Location",
    component: Location,
  },
  {
    path: "/company",
    name: "Company",
    component: Company,
  },
  {
    path: "/department",
    name: "Department",
    component: Department,
  },
  {
    path: "/shift",
    name: "shift",
    component: Shift,
  },
  {
    path: "/analytics",
    name: "Analytics",
    component: Analytics,
  },
  {
    path: "/employee",
    name: "Employee",
    component: Employee,
  },
  {
    path: "/attendance",
    name: "Attendance",
    component: Attendance,
  },
  {
    path: "/engagement",
    name: "Engagement",
    component: Engagement,
  },
  
  ...authRoutes,
];

const router = createRouter({
  base: "/frontend/",
  history: createWebHistory(),
  routes,
});

export default router;
