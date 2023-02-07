<template>
  <v-container class="mt-10">
    <v-row>
      <v-col>
        <v-card class="mx-auto" max-width="368">
          <v-card-item title="Florida">
            <template v-slot:subtitle>
              <v-icon icon="mdi-alert" size="18" color="error" class="me-1 pb-1"></v-icon>
    
              Extreme Weather Alert
            </template>
          </v-card-item>
    
          <v-card-text class="py-0">
            <v-row align="center" no-gutters>
              <v-col class="text-h2" cols="6">
                64&deg;F
              </v-col>
    
              <v-col cols="6" class="text-right">
                <v-icon color="error" icon="mdi-weather-hurricane" size="88"></v-icon>
              </v-col>
            </v-row>
          </v-card-text>
    
          <div class="d-flex py-3 justify-space-between">
            <v-list-item density="compact" prepend-icon="mdi-weather-windy">
              <v-list-item-subtitle>123 km/h</v-list-item-subtitle>
            </v-list-item>
    
            <v-list-item density="compact" prepend-icon="mdi-weather-pouring">
              <v-list-item-subtitle>48%</v-list-item-subtitle>
            </v-list-item>
          </div>
    
          <v-divider></v-divider>
    
          <v-card-actions>
            <v-btn>
              More Info
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col>
        <v-card class="mx-auto" max-width="368">
          <v-card-item title="Florida">
            <template v-slot:subtitle>
              <v-icon icon="mdi-alert" size="18" color="error" class="me-1 pb-1"></v-icon>
    
              Extreme Weather Alert
            </template>
          </v-card-item>
    
          <v-card-text class="py-0">
            <v-row align="center" no-gutters>
              <v-col class="text-h2" cols="6">
                64&deg;F
              </v-col>
    
              <v-col cols="6" class="text-right">
                <v-icon color="error" icon="mdi-weather-hurricane" size="88"></v-icon>
              </v-col>
            </v-row>
          </v-card-text>
    
          <div class="d-flex py-3 justify-space-between">
            <v-list-item density="compact" prepend-icon="mdi-weather-windy">
              <v-list-item-subtitle>123 km/h</v-list-item-subtitle>
            </v-list-item>
    
            <v-list-item density="compact" prepend-icon="mdi-weather-pouring">
              <v-list-item-subtitle>48%</v-list-item-subtitle>
            </v-list-item>
          </div>
    
          <v-divider></v-divider>
    
          <v-card-actions>
            <v-btn>
              More Info
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col>
        <v-card class="mx-auto" max-width="368">
          <v-card-item title="Florida">
            <template v-slot:subtitle>
              <v-icon icon="mdi-alert" size="18" color="error" class="me-1 pb-1"></v-icon>
    
              Extreme Weather Alert
            </template>
          </v-card-item>
    
          <v-card-text class="py-0">
            <v-row align="center" no-gutters>
              <v-col class="text-h2" cols="6">
                64&deg;F
              </v-col>
    
              <v-col cols="6" class="text-right">
                <v-icon color="error" icon="mdi-weather-hurricane" size="88"></v-icon>
              </v-col>
            </v-row>
          </v-card-text>
    
          <div class="d-flex py-3 justify-space-between">
            <v-list-item density="compact" prepend-icon="mdi-weather-windy">
              <v-list-item-subtitle>123 km/h</v-list-item-subtitle>
            </v-list-item>
    
            <v-list-item density="compact" prepend-icon="mdi-weather-pouring">
              <v-list-item-subtitle>48%</v-list-item-subtitle>
            </v-list-item>
          </div>
    
          <v-divider></v-divider>
    
          <v-card-actions>
            <v-btn>
              More Info
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-card>
        <v-frappe-chart
          type="axis-mixed"
          :labels="['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']"
          :data="[{ values: [18, 40, 30, 35, 8, 52, 17, -4] }]" :colors="['red']" />
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-card class="pa-2 ma-2">
          <v-frappe-chart type="bar" :labels="['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']"
            :data="[{ values: [18, 40, 30, 35, 8, 52, 17, -4] }]" :colors="['red']" />
          <!-- <v-btn
    @click="$resources.ping.fetch()"
    color="secondary"
    >Button</v-btn> -->
        </v-card>
      </v-col>
      <v-col>
        <v-card class="pa-2 ma-2">
          <h1>Home Page</h1>
          <v-frappe-chart isNavigable="true" animate="true" type="bar" :labels="['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']"
            :data="[{ values: [18, 40, 30, 35, 8, 52, 17, -4] }]" :colors="['red']" />
          <!-- <v-btn
    @click="$resources.ping.fetch()"
    color="secondary"
    >Button</v-btn> -->
        </v-card>

      </v-col>
    </v-row>
  </v-container>

</template>

<script>

export default {
  resources: {
    ping() {
      return {
        method: "frappe.ping", // Method to call on backend
        onSuccess(d) {
          alert(d);
        },
      };
    },
  },
};
</script>
