<template>
    <nav class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
        <div class="container-fluid d-flex justify-content-between align-items-center">
            <a class="navbar-brand fw-bold" href="">User Dashboard</a>
            <ul class="navbar-nav flex-row gap-3">
                <li class="nav-item">
                    <router-link to="/user-summary" class="nav-link px-2">Summary</router-link>
                </li>
                <li class="nav-item">
                    <a class="nav-link px-2" aria-current="page" @click="exportdata" style="cursor: pointer;">Export CSV</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link px-2 text-danger" aria-current="page" @click="logout" style="cursor: pointer;">Logout</a>
                </li>
            </ul>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="mb-3 d-flex" style="gap: 0.5rem;">
            <input type="text" class="form-control" placeholder="Search reservations..." v-model="searchText">
        </div>
        <h2 class="mb-3">Reservation Details</h2>
        <div v-if="filteredReservations.length > 0">
            <table class="table table-bordered table-striped">
                <thead class="table-dark">
                    <tr>
                        <th>Lot ID</th>
                        <th>Spot ID</th>
                        <th>Vehicle Number</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="res in filteredReservations" :key="res.id">
                        <td>{{ res.lot_id }}</td>
                        <td>{{ res.spot_id }}</td>
                        <td>{{ res.vehicle_number }}</td>
                        <td>{{ res.status }}</td>
                        <td v-if="res.status=='Parked'">
                            <button class="btn btn-danger btn-sm" @click="releaseVehicle(res.id)">Release</button>
                        </td>
                        <td v-if="res.status=='Booked'">
                            <button class="btn btn-success btn-sm" @click="parkVehicle(res.id)">Park In</button>
                        </td>
                        <td v-if="res.status=='Released'">
                            <span class="text-muted">N/A</span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else class="alert alert-info mt-4">No reservations available.</div>
    </div>
    

    <div class="container mt-4">
        <div class="mb-3 d-flex" style="gap: 0.5rem;">
            <input type="text" class="form-control" placeholder="Search lots..." v-model="searchQuery">
        </div>
        <h2 class="mb-3">Available Parking Lots</h2>
        <div v-if="filteredLots.length > 0">
            <table class="table table-bordered table-striped">
                <thead class="table-dark">
                    <tr>
                        <th>Lot ID</th>
                        <th>Location</th>
                        <th>Address</th>
                        <th>Available Spots</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="lot in filteredLots" :key="lot.id">
                        <td>{{ lot.id }}</td>
                        <td>{{ lot.prime_location_name }}</td>
                        <td>{{ lot.address }}</td>
                        <td>{{ lot.spots.length - occupiedCount(lot.spots) }}</td>
                        <td>
                            <button class="btn btn-primary btn-sm" @click="bookLot(lot.id)">Book</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else class="alert alert-info mt-4">No parking lots available.</div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            parkingLots: [],
            reservations: [],
            searchText: '',
            searchQuery: '',
        };
    },
    computed: {
        filteredReservations() {
            let reservations = this.reservations;
            if (this.searchText){
                reservations = reservations.filter(reservation => 
                    reservation.vehicle_number.toLowerCase().includes(this.searchText.toLowerCase()) ||
                    reservation.status.toLowerCase().includes(this.searchText.toLowerCase())
                );
            }
            return reservations;
        },
        filteredLots() {
            let parkingLots = this.parkingLots;
            if (this.searchQuery) {
                parkingLots = parkingLots.filter(lot =>
                    lot.prime_location_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                    lot.address.toLowerCase().includes(this.searchQuery.toLowerCase())
                );
            }
            return parkingLots;
        },
    },
    methods: {
        async logout() {
            localStorage.removeItem("token");
            this.$router.push("/");
        },
        async fetchLots() {
            try {
                const response = await fetch("/api/view-parking-lots/", {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${localStorage.getItem("token")}`,
                        "Content-Type": "application/json"
                    }
                });
                if (response.ok) {
                    const result = await response.json();
                    this.parkingLots = result.parking_lots;
                } else {
                    console.error("Failed to fetch parking lots.");
                }
            } catch (error) {
                console.error("Error fetching parking lots:", error);
            }
        },
        occupiedCount(spots) {
            return spots.filter(spot => spot.status === 'Occupied').length;
        },
        bookLot(lotId) {
            this.$router.push(`/reserve/${lotId}`);
        },
        async fetchReservations() {
            try {
                const response = await fetch("/api/history", {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${localStorage.getItem("token")}`,
                        "Content-Type": "application/json"
                    }
                });
                if (response.ok) {
                    const result = await response.json();
                    this.reservations = result.reservation_history;
                } else {
                    console.error("Failed to fetch reservations.");
                }
            } catch (error) {
                console.error("Error fetching reservations:", error);
            }
        },
        async parkVehicle(reservationId) {
            try {
                const response = await fetch(`/api/parking-lot/reservation/${reservationId}`, {
                method: "PATCH",
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("token")}`,
                    "Content-Type": "application/json"
                    },
                });
                if (response.ok) {
                    alert("Vehicle parked successfully.");
                    this.fetchReservations();
                } else {
                    alert("Failed to park vehicle.");
                }
            } catch (error) {
                console.error("Error parking vehicle:", error);
            }
        },
        async releaseVehicle(reservationId) {
            try {
                const response = await fetch(`/api/parking-lot/reservation/${reservationId}`, {
                    method: "PUT",
                    headers: {
                        "Authorization": `Bearer ${localStorage.getItem("token")}`,
                        "Content-Type": "application/json"
                    },
                });
                if (response.ok) {
                    this.$router.push(`/release/${reservationId}`);
                } else {
                    alert("Failed to release vehicle.");
                }
            } catch (error) {
                console.error("Error releasing vehicle:", error);
            }
        },
        async exportdata() {
            try {
                const response = await fetch("/api/export", {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${localStorage.getItem("token")}`
                    }
                });
                if (response.ok) {
                    const result = await response.json();
                    alert(result.message);
                } else {
                    alert("Error exporting data.");
                }
            } catch (error) {
                this.errorMessage = "Unable to connect to server.";
            }
        },
    },
    mounted() {
        this.fetchLots();
        this.fetchReservations();
    }
}
</script>