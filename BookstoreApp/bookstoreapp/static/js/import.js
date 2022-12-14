function add_to_list(id, name, category) {
        fetch('/api/import-cart', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "category": category
        }),
        headers: {
            "Content-Type": "application/json"
         }
         }).then(res => res.json()).then((data) => {
            console.info(data)
            let d = document.getElementsByClassName('import-cart-counter')
            for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity
         })
}

function update_from_list(product_id, obj) {
    number_reasonable(obj, parseInt(document.getElementById("limit").innerText))
    fetch(`/api/import-cart/${product_id}`, {
            method:'put',
            body: JSON.stringify({
                "quantity": obj.value
             }),
            headers:{
                "Content-type": "application/json"
            }}).then(res => res.json()).then((data) => {
                console.info(data)
                let d = document.getElementsByClassName('import-cart-counter')
                for (let i = 0; i < d.length; i++)
                    d[i].innerText = data.total_quantity


            })
}

function delete_from_list(product_id){
    fetch(`/api/import-cart/${product_id}`, {
        method: "delete"
    }).then(res => res.json()).then((data) => {
        console.info(data)
        let c = document.getElementById(`list${product_id}`)
        c.style.display = "none"
        location.reload()
    }).catch(err=>console.error(err))
}

function create(){
    if(confirm("Bạn có chắc chắn muốn tạo phiếu?") == true){
        fetch('/api/import-cart/create',{
        }).then(res => res.json()).then((data) => {
            if(data.status === 200)
                location.reload()
            console.info(data)
        })
    }
}