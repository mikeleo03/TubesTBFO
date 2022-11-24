let str = '';

for (let i = 0; i < 9; i++) 
{
  str = str + i;
  if (str != 0) {
    continue;
  }
}

console.log(str);
