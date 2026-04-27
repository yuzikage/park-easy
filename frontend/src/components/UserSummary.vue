<template>
    <nav class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
        <div class="container-fluid d-flex justify-content-between align-items-center">
            <a class="navbar-brand fw-bold" href="">User Dashboard</a>
            <ul class="navbar-nav flex-row gap-3">
                <li class="nav-item">
                    <router-link to="/user-dashboard" class="nav-link px-2">Dashboard</router-link>
                </li>
                <li class="nav-item">
                    <a class="nav-link px-2 text-danger" aria-current="page" @click="logout" style="cursor: pointer;">Logout</a>
                </li>
            </ul>
        </div>
    </nav>

    <div class="container">
        <br><br>
        <h3 class="text-center mb-4">Parking Summary</h3>
        <br><br>

        <div class="row" v-if="statusData">
            <div class="col-md-6" v-if="statusData">
                <h5>Reservation by Status</h5>
                <UserPieChart :chart-data="statusData"/>
            </div>

            <div class="col-md-6" v-if="locationData" style="max-height: 300px;">
                <br><br>
                <h5>Reservations by Location</h5>
                <UserBarChart :chart-data="locationData"/>
            </div>
        </div>
    </div>
</template>


<script>

import UserPieChart from './UserPieChart.vue';
import UserBarChart from './UserBarChart.vue';

export default {
    components: {
        UserPieChart,
        UserBarChart
    },
    data() {
        return {
            statusData: null,
            locationData: null
        }
    },
    methods: {
        async logout() {
            localStorage.removeItem("token");
            this.$router.push('/');
        }
    },
    async mounted() {
        const response = await fetch('/api/user-summary', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        const data = await response.json();

        const status = data.status_summary;
        const location = data.location_summary;

        this.statusData = {
            labels: Object.keys(status),
            datasets: [{
                data: Object.values(status),
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
            }]
        };
        this.locationData = {
            labels: Object.keys(location),
            datasets: [{
                label: 'Reservations by Location',
                data: Object.values(location),
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
            }]
        };
    }
}
</script>