<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 place-items-center rounded-lg">
                <img src="https://i.pravatar.cc/150?img=12" class="mb-6 rounded-full">

                <p><strong>{{ user.name }}</strong></p>

                <div class="mt-6 flex space-x-8 text-center justify-around">
                    <p class="text-xs text-gray-500">175 amigos</p>
                    <p class="text-xs text-gray-500">130 postagens</p>
                </div>
            </div>
        </div>

        <div class="main-center col-span-2 space-y-4">
            <div 
                class="bg-white border border-gray-200 rounded-lg"
                v-if="userStore.user.id === user.id"
            >
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="O que você está pensando?"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <a href="#" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Anexar imagem</a>

                        <button class="inline-block py-4 px-6 bg-blue-600 text-white rounded-lg">Postar</button>
                    </div>
                </form>
            </div>

            <div
                class="p-4 bg-white border border-gray-200 rounded-lg"
                v-for="post in posts"
                v-bind:key="post.id"
            >
                <FeedItem v-bind:post="post"/>
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />

            <Trends />
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
    import Trends from '@/components/Trends.vue'
    import FeedItem from '@/components/FeedItem.vue';
    import { useUserStore } from '@/stores/user'


    export default {
        name: 'FeedView',

        setup() {
            const userStore = useUserStore()

            return {
                userStore
            }
        },

        components: {
            PeopleYouMayKnow,
            Trends,
            FeedItem
        },

        data() {
            return {
                posts: [],
                user: {},
                body: '',
            }
        },

        watch: {
            "$route.params.id": {
                handler(id) {
                    this.getFeed(id)
                },
                immediate: true
            }
        },

        methods: {
            getFeed(id) {
                axios
                    .get(`/api/posts/profile/${id}/`)
                    .then(response => {
                        this.posts = response.data.posts
                        this.user = response.data.user
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            },

            submitForm() {
                axios
                    .post('/api/posts/create/', {
                        'body': this.body
                    })
                    .then(response => {
                        this.posts.unshift(response.data)
                        this.body = ''
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
        }
    }
</script>