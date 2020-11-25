const app = new Vue({
    el: "#app",
    data: function() {
        return {
            maximumPrice: 0,
            page: {},
            params: null,
            cart: null,
            likes: null,
        };
    },
    methods: {
        getProducts: function(params) {
            if(typeof(params) == "string") {
                this.params = new URLSearchParams(params);
            } else if(typeof(params) == "object") {
                this.params = params;
                params = `?${params.toString()}`;
            }
            
            axios.get(`/products/${params}`)
            .then(res => {
                console.log(res.data);
                this.page = res.data;
            })
            .catch(err => {
                console.log(err);
            })
        },
        submitFilters: function(e) {
            let form = document.getElementById("filters");
            let data = new FormData(form);
            let params = new URLSearchParams(data);
            this.getProducts(params);
        },
        getNextPage: function() {
            this.params.set('page', this.page.page + 1);
            this.getProducts(this.params);
        },
        getPreviousPage: function() {
            this.params.set('page', this.page.page - 1);
            this.getProducts(this.params);
        },
        getCart: function() {
            axios.get('/get_cart/')
            .then(res => {
                this.cart = res.data;
            })
            .catch(err => console.log(err))
        },
        getLikes: function() {
            axios.get('/get_likes/')
            .then(res => {
                this.likes = res.data;
            })
            .catch(err => console.log(err))
        },
        addToLikes: function(product) {
            if(!product.is_liked) {
                axios.post(`/like/${product.id}/`)
                .then(res => {
                    product.is_liked = true;
                    this.likes = res.data;
                })
                .catch(err => console.log(err))
            }
        },
        addToCart: function(product) {
            if(!product.is_in_cart) {
                axios.post(`/add_to_cart/${product.id}/`)
                .then(res => {
                    product.is_in_cart = true;
                    this.cart = res.data;
                })
                .catch(err => console.log(err))
            }
        },
    },
    mounted: function() {
        axios.defaults.headers['X-CSRFToken'] = Cookies.get('csrftoken');
        this.params = document.location.search;

        if(document.location.pathname == "/shop/") {
            this.getProducts(document.location.search);
        }
    
        this.getCart();
        this.getLikes();
    },
    watch: {},
});