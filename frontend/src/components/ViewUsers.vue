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

    <div class="container mt-4">
        <div class="mb-3 d-flex" style="gap: 0.5rem;">
            <input type="text" class="form-control" placeholder="Search users..." v-model="searchText">
        </div>
        <h2 class="mb-3">Users</h2>
        <table class="table table-striped table-bordered" v-if="filteredUsers.length > 0">
            <thead class="table-dark">
                <tr>
                    <th scope="col">User ID</th>
                    <th scope="col">Username</th>
                    <th scope="col">Email</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in filteredUsers" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.email }}</td>
                </tr>
            </tbody>
        </table>
        <div v-else class="alert alert-info mt-4">No users found.</div>
    </div>

</template>

<script>
export default {
    data(){
        return {
            users: [],
            searchText: ''
        }
    },
    computed: {
        filteredUsers() {
            let users = this.users;
            if (this.searchText){
                users = users.filter(user =>
                    user.username.toLowerCase().includes(this.searchText.toLowerCase()) ||
                    user.email.toLowerCase().includes(this.searchText.toLowerCase())
                );
            }
            return users;
        }
    },
    methods: {
        async logout() {
            localStorage.removeItem("token");
            this.$router.push("/");
        },
        async fetchUsers() {
            try {
                const response = await fetch("/api/users",{
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${localStorage.getItem("token")}`,
                        "Content-Type": "application/json"
                    }
                });
                if(response.ok){
                    const result = await response.json();
                    this.users = result.users;
                } else {
                    console.error("Failed to fetch users.");
                }
            } catch (error) {
                console.error("Error fetching users:", error);
            }
        },
    },
    mounted() {
        this.fetchUsers();
    },
}
</script>