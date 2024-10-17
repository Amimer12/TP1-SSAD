// the mainLoader

let myMainLoadertext = new SplitType('.theMainLoaderSpan',{type:"chars"})
let loaderMainDivs = document.querySelectorAll('.theMianLoader .textContainer div')
let loaderMain = document.querySelector('.theMianLoader')
let willrun = localStorage.getItem("loader")
let listOfBtnSetting = document.querySelectorAll('.settingSide .box div button')
if (willrun !== null) {
        listOfBtnSetting.forEach((e)=> {
            e.classList.remove('active')
        })
        if(willrun === "run") {
                listOfBtnSetting.forEach((lo)=> {
                    if (lo.dataset.loader === "y") {
                        lo.classList.add('active')
                    }
                })
        } else {
            listOfBtnSetting.forEach((lo)=> {
                if (lo.dataset.loader === "n") {
                    lo.classList.add('active')
                }
            })
        }
    if (willrun === "run") {
        const tl = gsap.timeline()
        loaderMain.style.backgroundColor = "#333"
        tl.to(loaderMainDivs,{y:0,duration:0.1,delay:.2,color:'#f6f6f6',
        stagger: {
            each:0.05,
        }
        })
        tl.to(loaderMain,{delay:1.2,height:0,
        ease:"power3.out",duration:1
        })
    } else {
        loaderMain.style.height = "0px"
    }
} else {
    const tl = gsap.timeline()
    loaderMain.style.backgroundColor = "#333"
    tl.to(loaderMainDivs,{y:0,duration:0.1,delay:.2,color:'#f6f6f6',
    stagger: {
        each:0.05,
    }
    })
    tl.to(loaderMain,{delay:1.2,height:0,
    ease:"power3.out",duration:1
    })
}

// end the Main loader


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
    let loader = document.querySelector('.login .formcontainer span.loader')
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
                    let divtextareaLeft = document.querySelector('.landing .container .loginPass div.left')
                    let divtextareaRight = document.querySelector('.landing .container .loginPass div.right')
                    gsap.from(divtextareaLeft, {
                        x:-200,
                        duration:1,
                        opacity:0,
                        ease:"power3.out"
                    })
                    gsap.from(divtextareaRight, {
                        x:+400,
                        opacity:0,
                        duration:1,
                        ease:"power3.out"
                    })
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
        // miroir(textareaLeft.value)
    }
})

function miroir(theText) {
    let theTextsting = new String(theText)
    let words = []
    words = theTextsting.split(" ")
    let reverse = words.map(function(ele) {
        let word = []
        word = ele.split("")
        let i = Math.floor(word.length / 2)
        for (j = 0 ; j <= i ; j++ ) {
            let a = word[j]
            word[j] = word[ele.length - 1 - j]
            word[ele.length - 1 - j] = a
        }
        ele = word.join("")
        return ele
    } )
    console.log(reverse.join(" "))
}
// miroir('mohamed zouaoui')

function decalgeAdroite(theText) {
    let theTextsting = new String(theText)
    let words = [];
    words = theTextsting.split(" ")
    let reverseAdoite = words.map(function(ele) {
        let word = []
        word = ele.split("")
        let i = word.length
        let fin = word[i - 1]
        for (j = i - 1 ;j >= 1; j--) {
            let a  = word[j]
            word[j] = word[j - 1]
        }
        word[0] = fin
        return word.join("")
    })
    console.log(reverseAdoite.join(" "))
}
// decalgeAdroite("abc bcfds mohamed")

function decalgeAgauche(theText) {
    let theTextsting = new String(theText)
    let words = [];
    words = theTextsting.split(" ")
    let reverseAdoite = words.map(function(ele) {
        let word = []
        word = ele.split("")
        let i = word.length
        let start = word[0]
        for (j = 0 ;j < i -1 ; j++) {
            let a  = word[j]
            word[j] = word[j + 1]
        }
        word[i -1 ] = start
        return word.join("")
    })
    console.log(reverseAdoite.join(" "))
}
// decalgeAgauche('mohmaed zouaoui')
// 

//  the responsive start
// let startHeight = window.innerHeight
// textareaLeft.addEventListener('focus' ,function() {
//     if (startHeight !== window.innerHeight) {
//         let change = startHeight - window.innerHeight;
//         let landing = document.querySelector('.landing');
//         landing.style.height = `calc(100vh + ${change}px)`
//     }
// })
// document.querySelector('.landing .container .formcontainer form input[type="text"]').addEventListener('blur' ,function() {
//     console.log(true)
// })
// //  the responsive end
// sign up
let submitNewUser = document.querySelector('.createUser .mastercontainer .left form input[type="submit"]')
submitNewUser.addEventListener('click',function(e) {
    e.preventDefault()
    let div = document.querySelector('.createUser .mastercontainer .containerloader')
    let divP = document.querySelector('.createUser .mastercontainer .containerloader p ')
    let divLoder = document.querySelector('.createUser .mastercontainer .containerloader span');
    div.classList.add('active')
    divLoder.style.display = 'block'
    divP.style.display = 'none';
    setTimeout(()=> {
        divLoder.style.display = 'none'
        divP.style.display = 'block';
        let createUser = document.querySelector('.createUser');
        gsap.to(createUser,{y:"-100%",duration:1.6,delay:1,ease:"power3.in"})
    },1900)
})

let addUserBtn = document.querySelector('.header .right button')
addUserBtn.addEventListener('click',()=> {
    let createUser = document.querySelector('.createUser');
    gsap.to(createUser,{
        duration:1.6,
        ease:"power3.out",
        y:"100%"
    })
})
let userTopNone = document.querySelector('.createUser .mastercontainer .left i')
userTopNone.addEventListener('click',()=> {
    let createUser = document.querySelector('.createUser');
    gsap.to(createUser,{
        duration:1.6,
        delay:0.1,
        ease:"power3.out",
        y:"-100%"
    })

})
// end sign up
// start maim Loader
// ########

let divIconSetting = document.querySelector('.settingSide .icon')
let iconSetting = document.querySelector('.settingSide .icon i')
let settingSide = document.querySelector('.settingSide')
divIconSetting.addEventListener("click",function(e) {
    e.stopPropagation()
    iconSetting.classList.toggle('fa-spin')
    if (settingSide.classList.contains('active') ) {
        settingSide.classList.remove('active')
        gsap.to(settingSide,{
            x:0,
            duration:1,
            ease:"power3.out",
        })
    } else {
        settingSide.classList.add('active')
        gsap.to(settingSide,{
            x:270,
            duration:1,
            ease:"power3.out",
        })
    }
})
listOfBtnSetting.forEach((ele)=> {
    ele.addEventListener("click",(e)=> {
        listOfBtnSetting.forEach((e) => {
            e.classList.remove('active')
        })
        e.target.classList.add('active')
        if (e.target.dataset.loader === "y") {
            localStorage.setItem("loader","run")
        } else {
            localStorage.setItem("loader","stop")
        }
    })
})







// end maim Loader