<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Entrar na sua conta</h1>

                <p class="mb-6 text-gray-500">
                    Lorem ipsum dolor sit, amet consectetur adipisicing elit. Aspernatur ea a deleniti.
                    Lorem ipsum dolor sit, amet consectetur adipisicing elit. Aspernatur ea a deleniti.
                </p>

                <p class="font-bold">
                    Não tem uma conta? <RouterLink :to="{'name': 'signup'}" class="underline">Clique aqui</RouterLink> para criar uma!
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6" v-on:submit.prevent="submitForm">
                    <div>
                        <label>E-mail</label><br>
                        <input type="email" v-model="form.email" placeholder="Seu endereço de e-mail" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Senha</label><br>
                        <input type="password" v-model="form.password" placeholder="Sua senha" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-400 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-blue-600 text-white rounded-lg">Entrar na conta</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
    import { useUserStore } from '@/stores/user'
    import axios from 'axios'

    export default {
        setup() {
            const userStore = useUserStore()

            return {
                userStore
            }
        },

        data() {
            return {
                form: {
                    email: '',
                    password: '',
                },
                errors: []
            }
        },
        methods: {
            async submitForm() {
                this.errors = []

                if (this.form.email === '') {
                    this.errors.push("Seu e-mail está faltando")
                }

                if (this.form.password === '') {
                    this.errors.push("Sua senha está faltando")
                }
                if (this.errors.length === 0) {
                    await axios
                        .post('/api/login/', this.form)
                        .then(response => {
                            this.userStore.setToken(response.data)

                            axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access
                        })
                        .catch(error => {
                            console.log('error', error)
                        })

                    await axios
                        .get('/api/me/')
                        .then(response => {
                            this.userStore.setUserInfo(response.data)

                            this.$router.push('/feed')
                        })
                        .catch(error => {
                            console.log('error', error)
                        })
                }
            }
        }
    }
</script>