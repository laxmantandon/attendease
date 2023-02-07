<template>
 
 <v-row v-if="companies.length > 0" class="ma-2" justify="end" style="background-color: white;">
            <v-col class="text-right">
                <v-btn color="primary" @click="dialog = true">New</v-btn>
            </v-col>
 </v-row>
 
    <v-container fill-height>       
        <v-row justify="center">
            <v-dialog max-width="800" v-model="dialog" :scrim="false" transition="dialog-bottom-transition">
                <template v-slot:activator="{ props }">
                    <v-row class="mt-16" justify="center" align="center" v-if="companies.length == 0">
                        <v-col cols="12" xs="8" sm="8" lg="4" md="6" xl="6" class="text-center">
                            <img src="../assets/no-data.svg">
                            <div>
                                <p>Oops ! No company Found, try adding a new company by clicking on below button</p>
                                <v-btn color="primary" v-bind="props">Add New company</v-btn>
                            </div>
                        </v-col>
                    </v-row>
                </template>
                <v-card>
                    <v-toolbar dark color="primary">
                        <v-btn icon dark @click="dialog = false">
                            <v-icon>mdi-close</v-icon>
                        </v-btn>
                        <v-toolbar-title>New company</v-toolbar-title>
                        <v-spacer></v-spacer>
                        <v-toolbar-items>
                            <v-btn variant="text" @click="newcompany">
                                Save
                            </v-btn>
                        </v-toolbar-items>
                    </v-toolbar>
                    <v-card-text>
                        <v-form ref="form">
                            <v-row>
                                <v-col>
                                    <v-text-field v-model="company_name"  label="Company Name" required></v-text-field>
                                    <v-text-field v-model="address_line_1" label="Address 1" required></v-text-field>
                                    <v-text-field v-model="address_line_2" label="Address 2" required></v-text-field>
                                    <v-text-field v-model="state" label="State" required></v-text-field>
                                    <v-text-field v-model="country" label="Country" required></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col>
                                    <v-text-field v-model="gstin" label="GSTIN" required></v-text-field>
                                </v-col>
                                <v-col>
                                    <v-text-field v-model="pan" label="PAN" required></v-text-field>
                                </v-col>
                                <v-col>
                                    <v-text-field v-model="contact" label="Contact" required></v-text-field>
                                </v-col>

                            </v-row>
                        </v-form>

                    </v-card-text>
                
                
                </v-card>
                
            </v-dialog>
        </v-row>

        <v-row justify="start">
            <v-col cols="12" xs="8" sm="8" lg="6" md="6" xl="6" align-self="start" v-for="b in companies">
                <v-card raised elevation="5" class="pa-2 ma-2">
                    <v-card-title>
                        {{ b.company_name }}
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text>
                        <p>{{b.address_line_1}} {{ b.address_line_2 }}</p>
                    </v-card-text>
                    <v-card-actions color="primary">
                        <v-btn >
                            More Info
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            companies: [],
            dialog: false,
            notifications: false,
            sound: true,
            widgets: false,
            company_name:"",
            address_line_1:"",
            address_line_1:"",
            state:"",
            country:"",
            gstin:"",
            pan:"",
            contact:"",
        }
    },
    mounted() {
        this.getcompanies()
    },

    methods: {
        async getcompanies() {
            await axios.get("api/method/attendease.attendease.api.get_companies")
                .then(r => {
                    if (r.status === 200) {
                        this.companies = r.data.message
                    }
                })
                .catch(e => {
                    console.log(e)
                })

        },
        async newcompany() {
            let req = {
                company_name: this.company_name,
                address_line_1:this.address_line_1,
                address_line_2:this.address_line_2,
                state:this.state,
                country:this.country,
                gstin:this.gstin,
                pan:this.pan,
                contact:this.contact,
            }

            await axios.post("api/method/attendease.attendease.api.new_company", req)
                .then(r => {
                    if (r.status === 200) {
                        this.dialog = false
                        this.getcompanies()
                    }
                })
                .catch(e => {
                    console.log(e)
                })

        }
    }
}
</script>

<style>
.dialog-bottom-transition-enter-active,
.dialog-bottom-transition-leave-active {
    transition: transform .2s ease-in-out;
}
</style>