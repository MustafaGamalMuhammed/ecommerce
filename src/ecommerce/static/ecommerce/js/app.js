const app = new Vue({
    el: "#app",
    data: function() {
        return {
            maximumPrice: 0,
            page: {},
        };
    },
    methods: {
        getProducts: function(params) {
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
            this.getProducts(`?${params.toString()}`);
        },
    },
    mounted: function() {
        if(document.location.pathname == "/shop/") {
            this.getProducts(document.location.search);
        }
    },
    watch: {},
});