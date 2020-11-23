const app = new Vue({
    el: "#app",
    data: function() {
        return {
            maximumPrice: 0,
            page: {},
        };
    },
    methods: {
        getProducts: function() {
            axios.get(`/products/${document.location.search}`)
            .then(res => {
                console.log(res.data);
                this.page = res.data;
            })
            .catch(err => {
                console.log(err);
            })
        },
    },
    mounted: function() {
        if(document.location.pathname == "/shop/") {
            this.getProducts();
        }
    },
    watch: {},
});