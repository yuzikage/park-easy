<template>
    <nav class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
        <div class="container-fluid d-flex justify-content-between align-items-center">
            <a class="navbar-brand fw-bold" href="">Admin Dashboard</a>
            <ul class="navbar-nav flex-row gap-3">
                <li class="nav-item">
                    <router-link to="/admin-dashboard" class="nav-link px-2">Dashboard</router-link>
                </li>
                <li class="nav-item">
                    <a class="nav-link px-2 text-danger" aria-current="page" @click="logout" style="cursor: pointer;">Logout</a>
                </li>
            </ul>
        </div>
    </nav>

    <div class="container">
        <br><br>
        <h3 class="text-center mb-4">Summary</h3>
        <br><br>

        <div class="row">
            <div class="col-md-6" v-if="occupancyData">
                <h5>Reservation by Status</h5>
                <AdminPieChart :chart-data="occupancyData"/>
            </div>

            <div class="col-md-6" v-if="bookingsData" style="max-height: 300px;">
                <h5>Bookings by Location</h5>
                <AdminBarChart :chart-data="bookingsData"/>
            </div>
        </div> 
    </div>
</template>


<script>

import AdminPieChart from './AdminPieChart.vue';
import AdminBarChart from './AdminBarChart.vue';


export default {
    components: {
        AdminPieChart,
        AdminBarChart
    },
    data() {
        return {
            occupancyData: null,
            bookingsData: null,
        }
    },
    methods: {
        async logout() {
            localStorage.removeItem("token");
            this.$router.push('/');
        }
    },
    async mounted() {
        const response = await fetch('/api/admin-summary', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        const data = await response.json();

        const spots = data.occupancy_summary;
        const bookings = data.bookings_summary;

        this.occupancyData = {
            labels: Object.keys(spots),
            datasets: [{
                data: Object.values(spots),
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
            }]
        };

        this.bookingsData = {
            labels: Object.keys(bookings),
            datasets: [{
                label: 'Bookings',
                data: Object.values(bookings),
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
            }]
        };
    }
}
</script>