function add_to_list(id, name, category) {
        fetch('/api/import', {
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

function delete_from_list(product_id){
    fetch(`/api/import/${product_id}`, {
        method: "delete",
    }).then(res => res.json()).then((data) => {
        console.info(data)
        let c = document.getElementById(`list${product_id}`)
        c.style.display = "none"
        location.reload()
    }).catch(err => console.error(err))
}