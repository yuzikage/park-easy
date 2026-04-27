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
            <h3 class="text-center mb-4">Create Parking Lot</h3>
            <form @submit.prevent="createLot">
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
                    <label for="totalSpots" class="form-label">Total Spots</label>
                    <input v-model="totalSpots" type="number" class="form-control" id="totalSpots" required />
                </div>
                <div class="d-grid gap-2">
                    <button type="submit" class="btn btn-primary">Create</button>
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
            totalSpots: 0,
            errorMessage: null
        };
    },
    methods: {
        async logout() {
            localStorage.removeItem("token");
            this.$router.push("/");
        },
        async createLot() {
            this.errorMessage = null;
            const payload = {
                prime_location_name: this.primeLocation,
                price: this.price,
                address: this.address,
                pincode: this.pincode,
                number_of_spots: this.totalSpots
            };
            try {
                const response = await fetch("/api/parking-lot", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${localStorage.getItem("token")}`
                    },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();
                if (response.ok) {
                    alert('Parking lot created successfully!');
                    this.$router.push('/admin-dashboard');
                } else {
                    this.errorMessage = result.message || 'Something went wrong.';
                }
            } catch (error) {
                this.errorMessage = 'Something went wrong. Please try again later.';
            }
        },
    },
}
</script>