console.log('hello world');
var number =5; 
console.log(number)
console.log(number)
let ourname = "come"
const pi = 2 // never change

// case sensitive
number--;
console.log(number)

//remainder
var remainder;
remainder = 11 % 3;
console.log(remainder)
remainder += 12;
console.log(remainder)
remainder -= 6
console.log(remainder)



var subString = 'I am "double" '
console.log(subString)

var sub = subString + "i am"
console.log(sub)

console.log(sub[2])

function wordBlanks(noun, adject, verb, myadvery){
    var result = ""
    result += noun + " " + adject + " " + myadvery + " " + verb
    return result
 }
console.log(wordBlanks("dog", "bark", "something", "soetning"))

var ourArray = ["John", 23]
for (let index = 0; 
    index < ourArray.length; 
    index++) {
    const element = ourArray[index];
    console.log(element)
}

ourArray.shift()
ourArray.unshift("happy")

console.log(ourArray)



var Global = 10;

var testArr = [1,2,3,4,5]
function nextInline(arr, item){
    arr[arr.length] = item
    if (arr.length == 12){
        return "True"
    } else {
        return "False"
    }
}
console.log(nextInline(testArr, 6))

var myMovie = {
    "title": "something", 
    "director": "pta"
};

console.log(myMovie.director)

myMovie.editor = "rinse"
delete myMovie.editor
console.log(myMovie)


console.log(myMovie["title"])
