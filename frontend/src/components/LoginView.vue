<template>
    <div class="container d-flex justify-content-center align-items-center vh-100">
        <div class="card p-4 shadow" style="width: 100%; max-width: 400px;">
            <h3 class="text-center mb-4">Login</h3>
            <form @submit.prevent="login">
                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input v-model="email" type="email" class="form-control" id="email" required />
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input v-model="password" type="password" class="form-control" id="password" required />
                </div>
                <div class="d-grid gap-2">
                    <button type="submit" class="btn btn-primary">Login</button>
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
            email: '',
            password: '',
            errorMessage: null
        };
    },
    methods: {
        async login() {
            this.errorMessage = null;
            const payload = {
                email: this.email,
                password: this.password
            };
            try {
                const response = await fetch("/api/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();
                if(response.ok){
                    alert('Login successful!');
                    localStorage.setItem('token', result.token);
                    if (result.user_role === 'admin') {
                        this.$router.push('/admin-dashboard');
                    } else if (result.user_role === 'user') {
                        this.$router.push('/user-dashboard');
                    }
                    
                } else {
                    this.errorMessage = result.message || 'Login failed. Please check your credentials.';
                }
            } catch (error) {
                this.errorMessage = 'Something went wrong. Please try again later.';
            }
        }
    }
};
</script>

<style scoped>
.card {
    border-radius: 1rem;
}
</style>