<template>
  <v-navigation-drawer app>
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

          <v-list-group color="primary" prepend-icon="mdi-cog-outline" value="Company Masters">
          <template v-slot:activator="{ props }">
            <v-list-item
              v-bind="props"
              title="Company Masters"
            ></v-list-item>
          </template>

          <v-list-item color="primary" prepend-icon="mdi-city" title="Location" value="location" to="/location" ></v-list-item>
          <v-list-item color="primary" prepend-icon="mdi-account-box-multiple-outline" title="Department" value="department" to="/department" ></v-list-item>
          <v-list-item color="primary" prepend-icon="mdi-clock-time-eight-outline" title="Shift" value="shift" to="/shift" ></v-list-item>
          <v-list-item color="primary" prepend-icon="mdi-account-multiple" title="Employee" value="employee" to="/employee" ></v-list-item>

        </v-list-group>
          <v-list-item color="primary" prepend-icon="mdi-human-handsup" title="Attendance" value="attendance" to="/attendance"></v-list-item>
          <v-list-item color="primary" prepend-icon="mdi-google-analytics" title="Analytics" value="analytics" to="/analytics"></v-list-item>
          <v-list-item color="primary" prepend-icon="mdi-handshake-outline" title="Engagement" value="engagement" to="/engagement"></v-list-item>
          <v-list-item color="primary" prepend-icon="mdi-logout" title="Logout" value="logout" @click="$auth.logout()"></v-list-item>
        </v-list>


        <!-- <v-list density="compact" nav>
          <v-list-item color="primary" prepend-icon="mdi-view-dashboard" title="Dashboard" value="dashboard" to="/"></v-list-item>
          <v-list-item color="primary" prepend-icon="mdi-domain" title="Company Masters" value="company-masters" to="/company-masters"></v-list-item>
          <v-list-item color="primary" prepend-icon="mdi-account-multiple" title="Employee" value="employee" to="/employee" ></v-list-item>
          <v-list-item color="primary" prepend-icon="mdi-human-handsup" title="Attendance" value="attendance" to="/attendance"></v-list-item>
          <v-list-item color="primary" prepend-icon="mdi-human-handsup" title="Analytics" value="analytics" to="/analytics"></v-list-item>
          <v-list-item color="primary" prepend-icon="mdi-human-handsup" title="Engagement" value="engagement" to="/engagement"></v-list-item>
          <v-list-item color="primary" prepend-icon="mdi-logout" title="Logout" value="logout" @click="$auth.logout()"></v-list-item>
        </v-list> -->

      </v-navigation-drawer>
</template>

<script>
export default {
  name: "SideNav",
  inject: ["$auth"],
  data() {
    return {
      mini: true,
      admins: [
        ['Management', 'mdi-account-multiple-outline'],
        ['Settings', 'mdi-cog-outline'],
      ],
      cruds: [
        ['Create', 'mdi-plus-outline'],
        ['Read', 'mdi-file-outline'],
        ['Update', 'mdi-update'],
        ['Delete', 'mdi-delete'],
      ],
    }
  }
}
</script>