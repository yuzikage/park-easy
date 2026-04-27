<template>
    <nav class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
        <div class="container-fluid d-flex justify-content-between align-items-center">
            <a class="navbar-brand fw-bold" href="">Admin Dashboard</a>
            <ul class="navbar-nav flex-row gap-3">
                <li class="nav-item">
                    <router-link to="/admin-summary" class="nav-link px-2">Summary</router-link>
                </li>
                <li class="nav-item">
                    <router-link to="/view-users" class="nav-link px-2">Users</router-link>
                </li>
                <li class="nav-item">
                    <a class="nav-link px-2 text-danger" aria-current="page" @click="logout">Logout</a>
                </li>
            </ul>
        </div>
    </nav>

    <div class="container py-5">
        <h2 class="text-center mb-4">Parking Lots</h2>
        <button class="btn btn-primary" @click="createLot">+ Create New Lot</button>
        <br> <br>

        <div class="mb-3 d-flex" style="gap: 0.5rem;">
            <input type="text" class="form-control" placeholder="Search lots..." v-model="searchText">
        </div>

        <div class="d-flex flex-wrap gap-4 justify-content-start" v-if="filteredLots.length > 0">
            <div v-for="lot in filteredLots" :key="lot.id" class="card border-primary p-3" style="min-width: 300px;">
                <h5 class="card-title">{{ lot.prime_location_name }}</h5>
                <p class="card-text">Total Spots: {{ lot.number_of_spots }}</p>
                <small>Occupied: {{ occupiedCount(lot.spots) }}/{{ lot.spots.length }}</small>
                <div class="my-2 d-flex flex-wrap" style="gap: 5px;">
                    <div
                    v-for="(spot,index) in lot.spots"
                    :key="spot.id"
                    :class="['rounded', 'text-center', 'spot-box', spot.status==='Occupied' ? 'bg-danger' : 'bg-success']"
                    @click="openSpotModal(spot)">
                    {{ index+1 }}
                    </div>
                </div>
                <div>
                    <a class="text-primary me-2" @click.prevent="editLot(lot.id)">Edit</a>
                    <a class="text-danger" @click.prevent="deleteLot(lot.id)">Delete</a>
                </div>
            </div>
        </div>
        <div v-else class="alert alert-info mt-4">No parking lots available.</div>

        <div class="modal fade" tabindex="-1" ref="spotModal">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Spot Details</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body" v-if="selectedSpot">
                        <p><strong>Spot ID:</strong> {{ selectedSpot.id }}</p>
                        <p v-if="selectedSpot.reservation">
                            <strong>User ID:</strong> {{ selectedSpot.reservation.user_id }} <br>
                            <strong>Vehicle number:</strong> {{ selectedSpot.reservation.vehicle_number }}
                        </p>
                        <p v-else>
                            This spot is currently available.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div> 
</template>

<script>
export default {
    data(){
        return {
            parkingLots: [],
            searchText: '',
            selectedSpot: null,
        }
    },
    computed: {
        filteredLots() {
            let parkingLots = this.parkingLots;
            if (this.searchText) {
                parkingLots = parkingLots.filter(lot =>
                    lot.prime_location_name.toLowerCase().includes(this.searchText.toLowerCase())
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
        async fetchParkingLots() {
            try {
                const response = await fetch("/api/parking-lot",{
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${localStorage.getItem("token")}`,
                        "Content-Type": "application/json"
                    }
                });
                if(response.ok){
                    const result = await response.json();
                    this.parkingLots = result.parking_lots;
                } else {
                    console.error("Failed to fetch parking lots.");
                }
            } catch (error) {
                console.error("Error fetching parking lots:", error);
            }
        },
        createLot() {
            this.$router.push("/create-lot");
        },
        occupiedCount(spots) {
            return spots.filter(spot => spot.status === 'Occupied').length;
        },
        openSpotModal(spot){
            this.selectedSpot = spot;
            if (!this.modalInstance) {
                this.modalInstance = new bootstrap.Modal(this.$refs.spotModal);
            }
            this.modalInstance.show();
        },
        editLot(lotId) {
            this.$router.push(`/edit-lot/${lotId}`);
        },
        async deleteLot(lotId) {
            if (confirm("Are you sure you want to delete this parking lot?")) {
                try {
                    const response = await fetch(`/api/parking-lot/${lotId}`, {
                        method: "DELETE",
                        headers: {
                            "Authorization": `Bearer ${localStorage.getItem("token")}`,
                            "Content-Type": "application/json"
                        }
                    });
                    const result = await response.json();
                    if (response.ok) {
                        alert(result.message);
                        this.fetchParkingLots();
                    } else {
                        alert("Can not delete parking lot with occupied spots.");
                    }
                } catch (error) {
                    alert("Error deleting parking lot:", error);
                }
            }
        },
    },
    mounted() {
        this.fetchParkingLots();
    },
}
</script>

<style scoped>
.spot-box {
    width: 50px;
    height: 50px;
    color: white;
    cursor: pointer;
    line-height: 35px;
    font-weight: bold;
}
a {
    cursor: pointer;
    text-decoration: none;
}
</style>