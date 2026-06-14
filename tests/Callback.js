
function add(num1,num2){
    return num1+num2;
}


function sub(num1,num2){
    return num1-num2;
}

function mul(num1,num2){
    return num1*num2;
}


function calculator(num1,num2,Callback){
    console.log("I am doing calculation");
    const result= Callback(num1,num2);
    console.log(result);

}


calculator(10,20,mul);
calculator(10,20,add);