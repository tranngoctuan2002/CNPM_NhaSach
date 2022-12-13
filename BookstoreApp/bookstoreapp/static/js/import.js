
function add_to_list() {

        name = document.getElementById("name").value
        tag = document.getElementById("cate").value
        author = document.getElementById("author").value

        fetch('/api/import', {
        method: "post",
        body: JSON.stringify({
            "name": name,
            "tag": tag,
            "author": author,
        }),
        headers: {
            "Content-Type": "application/json"
         }
         }).then(res => res.json()).then((data) => {
            console.info(data)
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