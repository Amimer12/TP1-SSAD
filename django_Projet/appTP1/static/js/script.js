let img = document.querySelectorAll('.landing > img')
let emailfild = document.querySelector('#email')
let passwordfild = document.querySelector('#password')
let containerloader = document.querySelector('.landing .container .formcontainer  .containerloader')
let loginfrom = document.querySelector('.landing .container .login')
setInterval(() => {
    let i = Math.floor(4 * Math.random())
    img[i].classList.toggle('active')
},2000)
let isremove = false
let submit = document.querySelector('.landing .container .formcontainer form input[type="submit"]')
submit.addEventListener('click',function(e) {
    e.preventDefault();
    containerloader.classList.add('active')
    let loader = document.querySelector('span.loader')
    let pyes = document.querySelector('.landing .container .formcontainer  .containerloader p.yes')
    let pno = document.querySelector('.landing .container .formcontainer  .containerloader p.no')
    pno.classList.remove('active')
    pyes.classList.remove('active')
    loader.classList.add('active')

    setTimeout(()=> {
        loader.classList.remove('active')
        if (emailfild.value == "admin" && passwordfild.value == 'admin') {
            pyes.classList.add('active')
            setTimeout(()=> {
                loginfrom.classList.add('gone')
                setTimeout(()=> {
                    loginfrom.remove()
                    isremove = true
                    loginPass.classList.add('active')
                },1000)
            },2000)
        } else {
            pno.classList.add('active')
        }
    },1900)
})  
let team = document.querySelector(".team")
let teambtn = document.querySelector(".team button")
let teampara = document.querySelector(".header .left p")
teampara.onclick = function() {
    team.classList.toggle('active')
}
teambtn.onclick = function() {
    team.classList.toggle('active')
}
let email = 'admin'
let password = 'admin'
let login = document.querySelector('.login')
let loginPass = document.querySelector('.landing .container .loginPass')
let pchoise = document.querySelector('.landing .container .loginPass .left .menu p')
let pchoiseIcon = document.querySelector('.landing .container .loginPass .left .menu p i')
let ulchoise = document.querySelector('.landing .container .loginPass div.left .bottom ul')
let ulLiChoise = document.querySelectorAll('.landing .container .loginPass div.left .bottom ul li')
let numOfMethod
pchoise.addEventListener("click",() => {
    ulchoise.classList.toggle('active')
    if (ulchoise.classList.contains('active')) {
        pchoiseIcon.classList.remove('fa-chevron-up')
        pchoiseIcon.classList.add('fa-chevron-down')
    } else {
        pchoiseIcon.classList.remove('fa-chevron-down')
        pchoiseIcon.classList.add('fa-chevron-up')
    }
})
pchoise.onclick = function(e) {
    e.stopPropagation();
    
}
ulchoise.onclick = function(e) {
    e.stopPropagation();
    
}
window.addEventListener('click' ,function(e) {
    if (ulchoise.classList.contains('active')) {
        if(e.target !== ulchoise) {
            pchoiseIcon.classList.remove('fa-chevron-down')
            pchoiseIcon.classList.add('fa-chevron-up')
            ulchoise.classList.remove('active')
        }
    }
})
ulLiChoise.forEach((ele) => {
    ele.onclick = function() {
        ulLiChoise.forEach((e) => {
            e.classList.remove('active')
        })
        this.classList.add('active')
        numOfMethod = this.dataset.method
    }
})
let btnSumbitCryp = document.querySelector('.landing .container .loginPass div.left .bottom button')
let textareaLeft = document.querySelector('.landing .container .loginPass div.left form textarea')
let textareaRight = document.querySelector('.landing .container .loginPass div.right form textarea')
btnSumbitCryp.addEventListener('click', function() {
    if (numOfMethod !== undefined) {
        miroir(textareaLeft.value)
    }
})

// function miroir(theText) {
//     let theTextsting = new String(theText)
//     let words = []
//     words = theTextsting.split(" ")
//     words.forEach(function(ele) {

//         let i = Math.floor(ele.length / 2)
//         for (j = 0 ; j < i ; j++ ) {
//             let a = ele[j]
//             let b = ele[ele.length - 1 - i]
//             let c ;
//             c = a;
//             a = b;
//             b = c
//         }
//     } )
//     console.log(words)
// }
