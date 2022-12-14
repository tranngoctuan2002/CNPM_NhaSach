function add_to_cart(id, name, category, price, img){
      fetch("/api/cart", {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "category": category,
            "price": price,
            "img": img
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => res.json()).then((data) => {
        console.info(data)
        let d = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity
    }) // js promise
}

function update_from_cart(product_id, obj){
      number_reasonable(obj)
      fetch(`/api/cart/${product_id}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => res.json()).then((data) => {
        console.info(data)
        let d = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity

        let a = document.getElementsByClassName('cart-amount')
        for (let i = 0;i < a.length;i++)
            a[i].innerText = data.total_value.toLocaleString("en-US")
    }) // js promise
}

function delete_from_cart(product_id){
      fetch(`/api/cart/${product_id}`, {
        method: "delete"
    }).then((res) => res.json()).then((data) => {
        console.info(data)
        let d = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity

        let a = document.getElementsByClassName('cart-amount')
        for (let i = 0;i < a.length;i++)
            a[i].innerText = data.total_value.toLocaleString("en-US")

        let p = document.getElementById(`cart${product_id}`)
        p.style.display = "none"
    }).catch(err=>console.error(err))
}

function payCart() {
    let addressDelivery = "Tại cửa hàng"
    d = parseInt(document.querySelector("input[type='radio'][name=deliver]:checked").value)
    if(d)
        addressDelivery = document.getElementById("address_delivery").value


    if(confirm("Bạn có chắc chắn muốn thanh toàn?") == true){
        fetch('/api/cart/pay',{
            method: "post",
            body: JSON.stringify({
                "name": document.getElementById("name").value,
                "phone": document.getElementById("phone").value,
                "address": document.getElementById("address").value,
                "email": document.getElementById("email").value,
                "payment": document.querySelector("input[type='radio'][name=payment]:checked").value,
                "address_delivery": addressDelivery
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

function new_cart() {
    if(confirm("Bạn có muốn xóa giỏ hàng hiện tại?") == true){
    fetch(`/api/cart`).then(res => res.json()).then((data) => {
            console.info(data)
            if(data.status === 200)
                location.reload()
        })
    }
}
