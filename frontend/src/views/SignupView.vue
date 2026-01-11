<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Criar Conta</h1>

                <p class="mb-6 text-gray-500">
                    Lorem ipsum dolor sit, amet consectetur adipisicing elit. Aspernatur ea a deleniti.
                    Lorem ipsum dolor sit, amet consectetur adipisicing elit. Aspernatur ea a deleniti.
                </p>

                <p class="font-bold">
                    Já tem uma conta? <RouterLink :to="{'name': 'login'}" class="underline">Clique aqui</RouterLink> para entrar!
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6" v-on:submit.prevent="submitForm">
                    <div>
                        <label>Nome</label><br>
                        <input type="text" v-model="form.name" placeholder="Seu nome completo" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>E-mail</label><br>
                        <input type="email" v-model="form.email" placeholder="Seu endereço de e-mail" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Senha</label><br>
                        <input type="password" v-model="form.password1" placeholder="Sua senha" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Confirmar senha</label><br>
                        <input type="password" v-model="form.password2" placeholder="Confirme sua senha" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-400 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-blue-600 text-white rounded-lg">Criar conta</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
    import { useToastStore } from '@/stores/toast'
    import axios from 'axios'

    export default {
        setup() {
            const toastStore = useToastStore()

            return {
                toastStore
            }
        },

        data() {
            return {
                form: {
                    email: '',
                    name: '',
                    password1: '',
                    password2: ''
                },
                errors: [],
            }
        },

        methods: {
            submitForm() {
                this.errors = []

                if (this.form.email === '') {
                    this.errors.push("Seu e-mail está faltando")
                }

                if (this.form.name === '') {
                    this.errors.push("Seu nome está faltando")
                }

                if (this.form.password1 === '') {
                    this.errors.push("Sua senha está faltando")
                }

                if (this.form.password1 !== this.form.password2) {
                    this.errors.push("A senha não corresponde")
                }

                if (this.errors.length === 0) {
                    axios
                        .post('/api/signup/', this.form)
                        .then(response => {
                            if (response.data.message === 'success') {
                                this.toastStore.showToast(5000, 'O usuário está registrado. Por favor entre', 'bg-emerald-500')

                                this.form.email = ''
                                this.form.name = ''
                                this.form.password1 = ''
                                this.form.password2 = ''
                            } else {
                                this.toastStore.showToast(5000, 'Algo deu errado. Por favor tente novamente', 'bg-red-300')
                            }
                        })
                        .catch(error => {
                            console.log('error', error)
                        })
                }
            }
        }
    }
</script>