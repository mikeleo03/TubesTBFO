let str = '';

for (let i = 0; i < 9; i++) 
{
  str = str + i;
  while (str != 1){
    i++;
  }
  function a() {
    test++;
    if (test < 10) {
        console.log(str);
    } else {
        test++;
    }
  }
}

console.log(str);
