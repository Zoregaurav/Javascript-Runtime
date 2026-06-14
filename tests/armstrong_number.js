let number = 153;
let original = number;
let sum = 0;

while (number > 0) {
  let digit = number % 10;
  sum += digit ** 3;
  number = Math.floor(number / 10);
}

console.log(sum === original);
