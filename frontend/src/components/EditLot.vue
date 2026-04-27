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

    <div class="container d-flex justify-content-center align-items-center vh-100">
        <div class="card p-4 shadow" style="width: 100%; max-width: 400px;">
            <h3 class="text-center mb-4">Edit Parking Lot</h3>
            <form @submit.prevent="editLot">
                <div class="mb-3">
                    <label for="primeLocation" class="form-label">Prime Location Name</label>
                    <input v-model="primeLocation" type="text" class="form-control" id="primeLocation" required />
                </div>
                <div class="mb-3">
                    <label for="price" class="form-label">Price</label>
                    <input v-model="price" type="text" class="form-control" id="price" required />
                </div>
                <div class="mb-3">
                    <label for="address" class="form-label">Address</label>
                    <textarea v-model="address" class="form-control" id="address" rows="3" required></textarea>
                </div>
                <div class="mb-3">
                    <label for="pincode" class="form-label">Pincode</label>
                    <input v-model="pincode" type="text" class="form-control" id="pincode" required />
                </div>
                <div class="mb-3">
                    <label for="numberOfSpots" class="form-label">Number of Spots</label>
                    <input v-model="numberOfSpots" type="number" class="form-control" id="numberOfSpots" required />
                </div>
                <div class="d-grid gap-2">
                    <button type="submit" class="btn btn-primary">Edit Lot</button>
                    <router-link to="/admin-dashboard" class="btn btn-secondary">Cancel</router-link>
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
            primeLocation: '',
            price: '',
            address: '',
            pincode: '',
            numberOfSpots: '',
            lotId: this.$route.params.id,
            errorMessage: null
        };
    },
    methods: {
        async logout() {
            localStorage.removeItem("token");
            this.$router.push("/");
        },
        async fetchLot() {
            try {
                const response = await fetch(`/api/a-parking-lot/${this.lotId}`, {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${localStorage.getItem("token")}`,
                        "Content-Type": "application/json"
                    }
                });
                if (response.ok) {
                    const data = await response.json();
                    this.primeLocation = data.parking_lot.prime_location_name;
                    this.price = data.parking_lot.price;
                    this.address = data.parking_lot.address;
                    this.pincode = data.parking_lot.pincode;
                    this.numberOfSpots = data.parking_lot.number_of_spots;
                } else {
                    this.errorMessage = 'Failed to load parking lot details.';
                }
            } catch (error) {
                this.errorMessage = 'Something went wrong. Please try again later.';
            }
        },
        async editLot() {
            this.errorMessage = null;
            const payload = {
                prime_location_name: this.primeLocation,
                price: this.price,
                address: this.address,
                pincode: this.pincode,
                number_of_spots: this.numberOfSpots
            };

            try {
                const response = await fetch(`/api/parking-lot/${this.lotId}`, {
                    method: "PUT",
                    headers: {
                        "Authorization": `Bearer ${localStorage.getItem("token")}`,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    alert('Parking Lot updated successfully!');
                    this.$router.push('/admin-dashboard');
                } else {
                    const result = await response.json();
                    this.errorMessage = result.message || 'Failed to update parking lot.';
                }
            } catch (error) {
                this.errorMessage = 'Something went wrong. Please try again later.';
            }
        }
    },
    mounted() {
        this.fetchLot();
    }
}
</script>