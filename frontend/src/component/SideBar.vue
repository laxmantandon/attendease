<template>
  <v-navigation-drawer
       rail absolute expand-on-hover left :mini-variant.sync="mini"
      >
        <v-list>
          <v-list-item
            prepend-avatar="https://randomuser.me/api/portraits/women/85.jpg"
            title="Sandra Adams"
            subtitle="sandra_a88@gmailcom"
          ></v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list density="compact" nav>
          <v-list-item color="primary" prepend-icon="mdi-view-dashboard" title="Dashboard" value="dashboard" to="/"></v-list-item>
          <v-list-item color="primary" prepend-icon="mdi-domain" title="Company" value="company" to="/company"></v-list-item>
          <v-list-item color="primary" prepend-icon="mdi-account-multiple" title="Employee" value="employee" to="/employee" ></v-list-item>
          <v-list-item color="primary" prepend-icon="mdi-human-handsup" title="Attendance" value="attendance" to="/attendance"></v-list-item>
          <v-list-item color="primary" prepend-icon="mdi-logout" title="Logout" value="logout" @click="$auth.logout()"></v-list-item>
        </v-list>
      </v-navigation-drawer>
</template>

<script>
export default {
  name: "SideNav",
  inject: ["$auth"],
  data() {
    return {
      mini: true
    }
  }
}
</script>