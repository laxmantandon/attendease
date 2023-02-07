<template>
		
		<v-app>
			<!-- <v-system-bar>
				<v-icon icon="mdi-wifi-strength-4"></v-icon>
				<v-icon icon="mdi-signal" class="ms-2"></v-icon>
				<v-icon icon="mdi-battery" class="ms-2"></v-icon>
			
				<span class="ms-2">3:13PM</span>
			</v-system-bar> -->
			<side-bar v-if="$auth.isLoggedIn"></side-bar>
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
		}
	},
	components: { SideBar },
	inject: ['$auth'],
	methods: {
		
	},
	};
</script>
