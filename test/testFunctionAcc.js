function Product(a,b,c,d){
    let x = a+b;
    x -= c;
    if (x == 1) {
        return a;
    }
    return x;
}