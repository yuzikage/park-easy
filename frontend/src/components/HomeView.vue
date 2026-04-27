<template>
    <div class="container mt-5">
        <div class="text-center">
            <h1>Welcome to Park Easy</h1>
            <p>Easily manage your bookings and park without any worries!</p>
        </div>    

        <div class="row mt-5 justify-content-center">
            <div class="col-md-4">
                <div class="card shadow-sm">
                    <div class="card-body text-center">
                        <h5 class="card-title">Login</h5>
                        <p class="card-text">Welcome back, login from here.</p>
                        <router-link to="/login" class="btn btn-primary">Login</router-link>
                    </div>
                </div>
            </div>

            <div class="col-md-4 mt-4 mt-md-0">
                <div class="card shadow-sm">
                    <div class="card-body text-center">
                        <h5 class="card-title">Register</h5>
                        <p class="card-text">New to the app? Signup from here.</p>
                        <router-link to="/register" class="btn btn-success">Register</router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.card {
    border-radius: 1rem;
}
</style>