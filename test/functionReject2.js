let x = 7;
function Product(a,b,c,d) {
    let x = a+b;
    x -= c;
    if (x == 1) {
        return a;
    }
    while (true) {
        if (x == 2) {
            break;
        } else {
            x++;
        }
    }
    return x;
}
return x;