<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Entrar</h1>

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
                <form action="" class="space-y-6">
                    <div>
                        <label>E-mail</label><br>
                        <input type="email" placeholder="Seu endereço de e-mail" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Senha</label><br>
                        <input type="password" placeholder="Sua senha" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <button class="py-4 px-6 bg-blue-600 text-white rounded-lg">Entrar</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>