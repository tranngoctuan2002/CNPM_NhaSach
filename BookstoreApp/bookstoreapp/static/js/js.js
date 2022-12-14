function number_reasonable(n){
    if(n.value < 1){
        alert("Số lượng không phù hợp")
        n.value = 1;
    }
}