import { createApp, reactive } from "vue";
import App from "./App.vue";
import Chart from "vue-frappe-chart"

import router from './router';
import resourceManager from "../../../doppio/libs/resourceManager";
import call from "../../../doppio/libs/controllers/call";
import socket from "../../../doppio/libs/controllers/socket";
import Auth from "../../../doppio/libs/controllers/auth";

import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const attendease = {
	dark: false,
	colors: {
	  background: "#F0F0F4",//"#F9F7F3",
	  surface: '#FFFFFF',
	  primary: '#0060df',
	  'primary-darken-1': '#C50000',
	  secondary: '#4ac4f3',
	  'secondary-darken-1': '#519bb7',
	  error: '#B00020',
	  info: '#2196F3',
	  success: '#4CAF50',
	  warning: '#FB8C00',
	}
  }

const vuetify = createVuetify({
	components,
	directives,
	theme: {
		defaultTheme: 'attendease',
		themes: {
			attendease,
		}
	}
})

const app = createApp(App);
const auth = reactive(new Auth());


// Plugins
app.use(router);
app.use(resourceManager);
app.use(vuetify)
app.use(Chart)

// Global Properties,
// components can inject this
app.provide("$auth", auth);
app.provide("$call", call);
app.provide("$socket", socket);


// Configure route gaurds
router.beforeEach(async (to, from, next) => {
	if (to.matched.some((record) => !record.meta.isLoginPage)) {
		// this route requires auth, check if logged in
		// if not, redirect to login page.
		if (!auth.isLoggedIn) {
			next({ name: 'Login', query: { route: to.path } });
		} else {
			next();
		}
	} else {
		if (auth.isLoggedIn) {
			next({ name: 'Home' });
		} else {
			next();
		}
	}
});

app.mount("#app");
