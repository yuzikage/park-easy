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

    <div class="container d-flex justify-content-center align-items-center vh-100">
        <div class="card p-4 shadow" style="width: 100%; max-width: 400px;">
            <h3 class="text-center mb-4">Release Spot</h3>
            <form>
                <div class="mb-3">
                    <label for="spotId" class="form-label">Spot ID</label>
                    <input v-model="spotId" type="text" class="form-control" id="spotId" readonly />
                </div>
                <div class="mb-3">
                    <label for="vehicleNumber" class="form-label">Vehicle Number</label>
                    <input v-model="vehicleNumber" type="text" class="form-control" id="vehicleNumber" readonly />
                </div>
                <div class="mb-3">
                    <label for="parkingTime" class="form-label">Parking Timestamp</label>
                    <textarea v-model="parkingTime" class="form-control" id="parkingTime" rows="3" readonly></textarea>
                </div>
                <div class="mb-3">
                    <label for="leavingTime" class="form-label">Leaving Timestamp</label>
                    <textarea v-model="leavingTime" class="form-control" id="leavingTime" rows="3" readonly></textarea>
                </div>
                <div class="mb-3">
                    <label for="totalCost" class="form-label">Total Cost</label>
                    <input v-model="totalCost" type="text" class="form-control" id="totalCost" readonly />
                </div>
                <div class="d-grid gap-2">
                    <router-link to="/user-dashboard" class="btn btn-primary">Release</router-link>
                </div>
                <p class="text-danger mt-3 text-center" v-if="errorMessage">{{ errorMessage }}</p>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            spotId: '',
            vehicleNumber: '',
            parkingTime: '',
            leavingTime: '',
            totalCost: '',
            reservationId: this.$route.params.reservationId,
            errorMessage: null
        };
    },
    methods: {
        async logout() {
            localStorage.removeItem("token");
            this.$router.push("/");
        },
        async fetchReservationDetails() {
            try {
                const response = await fetch(`/api/reservation-details/${this.reservationId}`, {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${localStorage.getItem("token")}`,
                        "Content-Type": "application/json"
                    }
                });
                if (response.ok) {
                    const res = await response.json();
                    this.spotId = res.spot_id;
                    this.vehicleNumber = res.vehicle_number;
                    this.parkingTime = new Date(res.parking_timestamp).toLocaleString('en-IN');
                    this.leavingTime = new Date(res.leaving_timestamp).toLocaleString('en-IN');
                    this.totalCost = res.parking_cost;
                } else {
                    alert("Failed to fetch reservation details.");
                }
            } catch (error) {
                console.error("Error fetching reservation details:", error);
            }
        },
    },
    mounted() {
        this.fetchReservationDetails();
    }
};
</script>