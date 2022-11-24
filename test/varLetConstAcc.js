let x,y=0,c;
const e = 'a', b='b';
var i;
var a = 10;
        function f(){
            console.log(a);
        }
    f();
    console.log(a);
    function f() {
 
        // It can be accessible any
        // where within this function
        var a = 10;
        console.log(a);
    }
    f();
 
    // A cannot be accessible
    // outside of function
    console.log(a);
    let a = 10;
    function f() 
    {
        if (true) {
            let b = 9;
            if (b==9) 
            {
                // It prints 9
                console.log(b);
            }
        }
 
        // It gives error as it
        // defined in if block
        console.log(b);
    }
    f();
 
    // It prints 10
    console.log(a);
    let a = 10;
 
    // It is not allowed
    let a = 10;
 
    // It is allowed
    a = 10;