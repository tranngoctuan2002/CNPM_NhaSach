function add_to_cash() {
    fetch("/api/cash", {
        method: "post",
        body: JSON.stringify({
            "id": document.getElementById("id").value,
            "quantity": document.getElementById("quantity").value
        }),
        headers: {
            "Content-type": "application/json"
        }
    }).then(res => res.json()).then((data) => {
        console.info(data)
        location.reload()
    })
}

function delete_from_cash(product_id) {
    fetch(`/api/cash/${product_id}`, {
        method: "delete"

    }).then(res => res.json()).then((data) => {
        console.info(data)
        h = document.getElementById(`cash${product_id}`)
        h.style.display = "none"
        location.reload()
    })
}



function update_to_cash(product_id, obj) {
    number_reasonable(obj, 300)

    fetch(`/api/import-cart/${product_id}`, {
            method:'put',
            body: JSON.stringify({
                "quantity": obj.value
             }),
            headers:{
                "Content-type": "application/json"
            }}).then(res => res.json()).then((data) => {
                console.info(data)
                let d = document.getElementsByClassName("cash-quantity")
                for (let i = 0; i < d.length; i++)
                    d[i].innerText = data.total_quantity

                let a = document.getElementsByClassName("cash-value")
                for (let i = 0; i < a.length; i++)
                    a[i].innerText = data.total_value.toLocaleString("en-US")
            })
}

function pay() {
    if(confirm("Bạn có chắc chắn muốn thanh toàn?") == true){
        fetch('/api/pay',{
            method: "post",
            body: JSON.stringify({
                "cName": document.getElementById("name").value,
                "cPhone": document.getElementById("phone").value
            }),
            headers: {
                "Content-type": "application/json"
            }
        }).then(res => res.json()).then((data) => {
            if(data.status === 200)
                location.reload()
            console.info(data)
        })
    }
}


function new_cash() {
    if(confirm("Bạn có muốn xóa giỏ hàng hiện tại?") == true){
    fetch(`/api/cash`).then(res => res.json()).then((data) => {
            console.info(data)
            if(data.status === 200)
                location.reload()
        })
    }
}


