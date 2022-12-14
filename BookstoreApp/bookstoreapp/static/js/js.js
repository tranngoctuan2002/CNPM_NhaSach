function number_reasonable(n, limit=1){
    if(n.value < limit){
        alert("Số lượng không phù hợp")
        n.value = limit;
    }
}
