<template>
		
		<v-app>
			<!-- <v-system-bar>
				<v-icon icon="mdi-wifi-strength-4"></v-icon>
				<v-icon icon="mdi-signal" class="ms-2"></v-icon>
				<v-icon icon="mdi-battery" class="ms-2"></v-icon>
			
				<span class="ms-2">3:13PM</span>
			</v-system-bar> -->
			
			<side-bar v-model="drawer" v-if="$auth.isLoggedIn"></side-bar>

			<v-app-bar app v-if="$auth.isLoggedIn">
				<v-app-bar-nav-icon @click.stop="drawer = !drawer">
					
				</v-app-bar-nav-icon>
				<template v-slot:append>
					<v-btn icon="mdi-heart"></v-btn>
			
					<v-btn icon="mdi-magnify"></v-btn>
			
					<v-btn icon="mdi-dots-vertical"></v-btn>
				</template>
			</v-app-bar>
			
			
			<v-main >
				<router-view />
			</v-main>
		</v-app>

</template>


<script>
import SideBar from './component/SideBar.vue';
export default {
	data() {
		return {
			drawer: true
		}
	},
	components: { SideBar },
	inject: ['$auth'],
	methods: {
		
	},
	};
</script>
