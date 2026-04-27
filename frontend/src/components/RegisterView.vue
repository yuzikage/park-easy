<template>
    <div class="container d-flex justify-content-center align-items-center vh-100">
        <div class="card p-4 shadow" style="width: 100%; max-width: 400px;">
            <h3 class="text-center mb-4">Register</h3>
            <form @submit.prevent="register">
                <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input  v-model="username" type="text" class="form-control" id="username"required>
                </div>
                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input v-model="email" type="email" class="form-control" id="email" required />
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input v-model="password" type="password" class="form-control" id="password" required />
                </div>
                <div class="d-grid gap-2">
                    <button type="submit" class="btn btn-primary">Register</button>
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
            username: '',
            email: '',
            password: '',
            errorMessage: null,
        };
    },
    methods: {
        async register() {
            this.errorMessage = null;
            const payload = {
                username: this.username,
                email: this.email,
                password: this.password,
                role: 'user'
            };
            try {
                const response = await fetch("/api/register", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();
                if (response.ok){
                    alert(result.message);
                    this.$router.push("/login");
                } else {
                    this.errorMessage = result.message || "Something went wrong.";
                }
            } catch (error) {
                this.errorMessage = "Unable to connect to server.";
            }
        },
    },
}
</script>

<style scoped>
.card {
  border-radius: 1rem;
}
</style>
