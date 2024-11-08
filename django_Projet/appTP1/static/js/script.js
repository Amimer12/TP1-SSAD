// the mainLoader

let myMainLoadertext = new SplitType('.theMainLoaderSpan',{type:"chars"})
let loaderMainDivs = document.querySelectorAll('.theMianLoader .textContainer div')
let loaderMain = document.querySelector('.theMianLoader')
let willrun = localStorage.getItem("loader")
let listOfBtnSetting = document.querySelectorAll('.settingSide .box div button')
let webSiteMode = 'cry';

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
let team = document.querySelector(".team")
let teambtn = document.querySelector(".team button")
let teampara = document.querySelector(".header .left p")
teampara.onclick = function() {
    team.classList.toggle('active')
}
teambtn.onclick = function() {
    team.classList.toggle('active')
}

//////////////////////////////////////////////////////////////////////

// the background change
// end
// 
let emailfild = document.querySelector('input[name="usernameL"]');  // Update the selector to match the rendered ID
let passwordfild = document.querySelector('input[name="passwordL"]');  // Update the selector to match the rendered ID
let captcha = document.querySelector('input[name="CAPTCHA"]');
let containerloader = document.querySelector('.landing .container .formcontainer .containerloader');
let loginfrom = document.querySelector('.landing .container .login');
let loginPass = document.querySelector('.landing .container .loginPass');
let urlLogin = document.querySelector('.landing .container .login .formcontainer form').action;
let theModeBox = document.querySelector(".settingSide .box-crypt")
let model = document.querySelector('.landing .container .formcontainer form .ModalCaptcha ');
let afficher =document.querySelector('.landing .container .formcontainer form input[type="submit"]');
afficher.addEventListener('click', function() {
//ModalCaptcha
console.log("le message ",emailfild.value)
if( emailfild.value !=""  && passwordfild.value !="" ) {
model.style.display = 'flex';
}
});

let submit = document.querySelector('.landing .container .formcontainer form .ModalCaptcha input[type="submit"]');
submit.addEventListener('click', function(e) {
    e.preventDefault();

    model.style.display = 'none'
    containerloader.classList.add('active');
    let loader = document.querySelector('.login .formcontainer span.loader');
    let pyes = document.querySelector('.landing .container .formcontainer .containerloader p.yes');
    let pno = document.querySelector('.landing .container .formcontainer .containerloader p.no');
    
    pno.classList.remove('active');
    pyes.classList.remove('active');
    loader.classList.add('active');

    // Collect form data
    let formData = new URLSearchParams();  // Using URLSearchParams
    formData.append('username', emailfild.value);  // Appending username
    formData.append('password', passwordfild.value);  // Appending password
    formData.append('captcha_text',captcha.value); //Apending captcha 
    

    fetch(urlLogin, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',  // URL-encoded form data
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value  // CSRF token
        },
        body: formData.toString()  // Convert formData to string for sending
    })
    .then(response => response.json()) // Parse JSON response
    .then(data => {
        loader.classList.remove('active');

        if (data.success_message) {
            pyes.textContent = data.success_message;
            pyes.classList.add('active');
            theModeBox.style.display = "block"
            setTimeout(() => {
                loginfrom.classList.add('gone');
                setTimeout(() => {
                    loginfrom.remove();
                    loginPass.classList.add('active');
                    
                    let divtextareaLeft = document.querySelector('.landing .container .loginPass div.left');
                    let divtextareaRight = document.querySelector('.landing .container .loginPass div.right');
                    
                    gsap.from(divtextareaLeft, {
                        x: -200,
                        duration: 1,
                        opacity: 0,
                        ease: "power3.out"
                    });
                    gsap.from(divtextareaRight, {
                        x: +400,
                        opacity: 0,
                        duration: 1,
                        ease: "power3.out"
                    });
                }, 1000);
            }, 2000);
        } else if (data.errors) {
            console.log(data.errors)
          //  pno.textContent = data.errors.__all__ ? data.errors.__all__[0] : "Invalid email or password";
            pno.textContent = data.errors.__all__[0] ;
            pno.classList.add('active');
            captcha.value="";
        }
    })
    .catch(error => {
        loader.classList.remove('active');
        pno.textContent = "An error occurred. Please try again.";
        pno.classList.add('active');
        captcha.value="";
    });
});



//////////////////////////////////////////////

let email = 'admin'
let password = 'admin'
let login = document.querySelector('.login')
let pchoise = document.querySelector('.landing .container .loginPass .left .menu p')
let pchoiseIcon = document.querySelector('.landing .container .loginPass .left .menu p i')
let ulchoise = document.querySelector('.landing .container .loginPass div.left .bottom ul.crypt')
let ulLiChoise = document.querySelectorAll('.landing .container .loginPass div.left .bottom ul.crypt li')

// #############--------------------------------####################3
let ulchoisestg = document.querySelector('.landing .container .loginPass div.left .bottom ul.stg')
let ulLiChoisestg = document.querySelectorAll('.landing .container .loginPass div.left .bottom ul.stg li')

let numOfMethod


console.log(webSiteMode)

// website mode

let crypageMode = document.querySelector(".settingSide .box-crypt .cry")
let stegranographyMode = document.querySelector(".settingSide .box-crypt .stg")

// les text

let textareaRightCty = document.querySelectorAll(".landing .container .loginPass div.right > div.areacry ")
let textareaRightStg = document.querySelector(".landing .container .loginPass div.right > div.areastg ")


// ??????

let questionIcon = document.querySelector(".landing .container .loginPass div.left .top .question .icon");
let takeaffine = document.querySelector('.landing .container .loginPass div.left .question .box.takeaffine');
let takecesar = document.querySelector('.landing .container .loginPass div.left .question .box.takecesar');
let takestg = document.querySelector('.landing .container .loginPass div.left .question .box.stg');
let takestgColumn = document.querySelector('.landing .container .loginPass div.left .question .box.stgColumn');
let hideBtn = document.querySelector('button[class="hideBtn"]');
let btnModeList = [questionIcon ,takecesar,takeaffine ]
crypageMode.onclick = ()=> {
    webSiteMode = "cry";
    stegranographyMode.classList.remove('active')
    crypageMode.classList.add('active')
    hideBtn.classList.remove('active')
    textareaRightStg.style.display = "none"
    textareaRightCty.forEach((e)=> {
        e.style.display = "block"
    })
    btnModeList.forEach((e)=> {
        e.classList.remove('active')
    })
    moveDesign()
}
stegranographyMode.onclick = ()=> {
    webSiteMode = "stg";
    crypageMode.classList.remove('active')
    stegranographyMode.classList.add('active')
    hideBtn.classList.add('active')
    textareaRightStg.style.display = "block"
    textareaRightCty.forEach((e)=> {
        e.style.display = "none"
    })
    btnModeList.forEach((e)=> {
        e.classList.remove('active')
    })
    moveDesign()
}

function moveDesign() {
    pchoiseIcon.classList.remove('fa-chevron-down')
    pchoiseIcon.classList.add('fa-chevron-up')
    ulchoise.classList.remove('active')
    ulchoisestg.classList.remove('active')
}

pchoise.addEventListener("click",() => {
    if (webSiteMode === 'cry') {
        ulchoise.classList.toggle('active')
        if (ulchoise.classList.contains('active')) {
            pchoiseIcon.classList.remove('fa-chevron-up')
            pchoiseIcon.classList.add('fa-chevron-down')
        } else {
            pchoiseIcon.classList.remove('fa-chevron-down')
            pchoiseIcon.classList.add('fa-chevron-up')
        }
    } else {
        ulchoisestg.classList.toggle('active')
        if (ulchoisestg.classList.contains('active')) {
            pchoiseIcon.classList.remove('fa-chevron-up')
            pchoiseIcon.classList.add('fa-chevron-down')
        } else {
            pchoiseIcon.classList.remove('fa-chevron-down')
            pchoiseIcon.classList.add('fa-chevron-up')
        }
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
ulLiChoisestg.forEach((ele) => {
    ele.onclick = function() {
        ulLiChoisestg.forEach((e) => {
            e.classList.remove('active')
        })
        this.classList.add('active')
        numOfMethod = this.dataset.method
    }
})
let btnSumbitCryp = document.querySelector('.landing .container .loginPass div.left .bottom button')
let textareaLeft = document.querySelector('.landing .container .loginPass div.left form textarea')
let textareaRight = document.querySelector('.landing .container .loginPass div.right form textarea')

let urlCrypt = document.querySelector('.landing .container .loginPass .left form').action;
let urlHide = document.querySelector('form[id="formHide"]').action;
let textFeildToCrypt = document.querySelector('textarea[id="textToCrypt"]');  
let affine_a = document.querySelector('input[id="affine_a"]');  
let affine_b = document.querySelector('input[id="affine_b"]');  
let cesar_key = document.querySelector('input[id="cesar_key"]');  
let textFeildResultCrypt = document.querySelector('textarea[id="textResultCrypt"]');  
let textFeildResultDecrypt = document.querySelector('textarea[id="textResultDecrypt"]');  

let messageStg = document.querySelector('textarea[id="textResultStg"]');

let messageStgTohide = document.querySelector('input[id="stg_message"]');
let messageStgTohideColumn = document.querySelector('input[id="stg_messageclm"]');
let ColumnStg= document.querySelector('input[id="nbr_column"]');
let hideSuccess = document.querySelector('div[id="success_msg"]');

btnSumbitCryp.addEventListener('click', function(e) {
    e.preventDefault();

    // Clear previous messages
    messageStg.textContent = "";  
    messageStg.style.color = "";  

    if (numOfMethod !== undefined) {
        let formDataCrypt = new URLSearchParams();  

        // Check the mode and set form data accordingly
        if (webSiteMode === "cry") {
            formDataCrypt.append('method', numOfMethod);  
            formDataCrypt.append('textToEncrypt', textFeildToCrypt.value);
            formDataCrypt.append('affine_a', affine_a.value);
            formDataCrypt.append('affine_b', affine_b.value);
            formDataCrypt.append('cesar_key', cesar_key.value);
        } else {
            formDataCrypt.append('methodStg', numOfMethod);  
            formDataCrypt.append('textToStg', textFeildToCrypt.value);
        }

        fetch(urlCrypt, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',  
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value  
            },
            body: formDataCrypt.toString()  
        })
        .then(response => response.json()) 
        .then(data => {
            if (data.success) {
                if (webSiteMode === "cry") {
                    textFeildResultCrypt.textContent = data.CryptedText;
                    textFeildResultDecrypt.textContent = data.DecryptedText;
                } else {
                    messageStg.textContent = data.messageStg;  // Display extracted message
                    messageStg.style.color = "green";  // Success message styling
                }
            } else if (data.errors) {
                // Display specific error message
                if (webSiteMode === "cry") {
                    textFeildResultCrypt.textContent = data.errors;
                } else {
                    messageStg.textContent = data.errors;  // Display extraction error
                    messageStg.style.color = "red";  // Error message styling
                }
            }
        })
        .catch(error => {
            // Network or server error handling
            if (webSiteMode === "cry") {
                textFeildResultCrypt.textContent = "An error occurred. Please try again.";
            } else {
                messageStg.textContent = "No hidden message detected!";
                messageStg.style.color = "red";  // Error styling
            }
        });
    } else {
        // Handling when no method is selected
        if (webSiteMode === "cry") {
            textFeildResultCrypt.textContent = "Please choose a method before you execute.";
            textFeildResultCrypt.style.color = "red";
        } else {
            messageStg.textContent = "Please choose a method before you execute.";
            messageStg.style.color = "red";
        }
    }
});

hideBtn.addEventListener('click', function(e) {
    e.preventDefault();

    // Clear previous messages
    hideSuccess.classList.remove('active');
    hideSuccess.style.color = "";
    hideSuccess.textContent = "";  

    if (numOfMethod !== undefined) {
        let formDataCrypt = new URLSearchParams();  
        formDataCrypt.append('methodStgHide', numOfMethod);  
        formDataCrypt.append('textToStgHide', textFeildToCrypt.value);

        if (numOfMethod === "s1" || numOfMethod === "s2") {
            formDataCrypt.append('MsgStgHide', messageStgTohide.value); 
        } else {
            formDataCrypt.append('MsgStgHide', messageStgTohideColumn.value);
            formDataCrypt.append('nbr_column', ColumnStg.value);
        }

        fetch(urlHide, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',  
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value  
            },
            body: formDataCrypt.toString()  
        })
        .then(response => response.json()) 
        .then(data => {
            if (data.success) {
                hideSuccess.style.color = "green";
                hideSuccess.classList.add('active');
                hideSuccess.textContent = "Your message is hidden successfully!";
                textFeildToCrypt.value = data.TextWithHiddenMessage;
            } else if (data.errors) {
                hideSuccess.classList.add('active');
                hideSuccess.style.color = "red";
                hideSuccess.textContent = data.errors;  // Display specific error message from server
            }
        })
        .catch(error => {
            hideSuccess.classList.add('active');
            hideSuccess.style.color = "red";
            hideSuccess.textContent = "An error occurred. Please try again.";
        });

    } else {
        hideSuccess.classList.add('active');
        hideSuccess.style.color = "red";
        hideSuccess.textContent = "Please choose a method before hiding your message.";
    }
});


// function miroir(theText) {
//     let theTextsting = new String(theText)
//     let words = []
//     words = theTextsting.split(" ")
//     let reverse = words.map(function(ele) {
//         let word = []
//         word = ele.split("")
//         let i = Math.floor(word.length / 2)
//         for (j = 0 ; j <= i ; j++ ) {
//             let a = word[j]
//             word[j] = word[ele.length - 1 - j]
//             word[ele.length - 1 - j] = a
//         }
//         ele = word.join("")
//         return ele
//     } )
//     console.log(reverse.join(" "))
// }
// miroir('mohamed zouaoui')

// function decalgeAdroite(theText) {
//     let theTextsting = new String(theText)
//     let words = [];
//     words = theTextsting.split(" ")
//     let reverseAdoite = words.map(function(ele) {
//         let word = []
//         word = ele.split("")
//         let i = word.length
//         let fin = word[i - 1]
//         for (j = i - 1 ;j >= 1; j--) {
//             let a  = word[j]
//             word[j] = word[j - 1]
//         }
//         word[0] = fin
//         return word.join("")
//     })
//     console.log(reverseAdoite.join(" "))
// }
// decalgeAdroite("abc bcfds mohamed")

// function decalgeAgauche(theText) {
//     let theTextsting = new String(theText)
//     let words = [];
//     words = theTextsting.split(" ")
//     let reverseAdoite = words.map(function(ele) {
//         let word = []
//         word = ele.split("")
//         let i = word.length
//         let start = word[0]
//         for (j = 0 ;j < i -1 ; j++) {
//             let a  = word[j]
//             word[j] = word[j + 1]
//         }
//         word[i -1 ] = start
//         return word.join("")
//     })
//     console.log(reverseAdoite.join(" "))
// }
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
// Handle the submission with visual effects and then form submission
document.addEventListener('DOMContentLoaded', function () {
    let form = document.querySelector('.createUser .mastercontainer .left form');
    let div = document.querySelector('.createUser .mastercontainer .containerloader');
    let successMessageElement = div.querySelector('.yes');

    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault(); // Prevent the default form submission (no page reload)

            let formData = new FormData(form); // Create a FormData object to hold form data
            let url = form.action; // Get the form action URL

            // Clear previous errors by hiding all form-error elements
            let errorElements = form.querySelectorAll('.form-error');
            errorElements.forEach(function (errorElement) {
                errorElement.style.display = 'none'; // Hide all error messages initially
            });

            // Send an AJAX POST request using the Fetch API
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest', // Header to indicate AJAX request
                    'X-CSRFToken': form.querySelector('input[name="csrfmiddlewaretoken"]').value // CSRF token
                }
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => { throw data });  // Throw error data
                }
                return response.json();
            })
            .then(data => {
                // Handle the response data (success)
                if (data.success_message) {
                    // Success: show the loader and animate the form away
                    successMessageElement.textContent = data.success_message;

                    let divLoader = div.querySelector('span');
                    let divP = div.querySelector('p');

                    div.classList.add('active');
                    divLoader.style.display = 'block';
                    divP.style.display = 'none';

                    setTimeout(() => {
                        divLoader.style.display = 'none';
                        divP.style.display = 'block';

                        let createUser = document.querySelector('.createUser');
                        gsap.to(createUser, { y: "-100%", duration: 1.6, delay: 1, ease: "power3.in" });
                    }, 1900);
                }
            })
            .catch(data => {
                // Errors: Display form errors dynamically
                if (data.errors) {
                    let errors = JSON.parse(data.errors); // Parse the JSON-formatted errors
                    Object.keys(errors).forEach(function (fieldName) {
                        let errorElement = form.querySelector(`[name="${fieldName}"]`).nextElementSibling;
                        if (errorElement && errorElement.classList.contains('form-error')) {
                            errorElement.textContent = errors[fieldName][0].message; // Show the first error for the field
                            errorElement.style.display = 'block'; // Show the error message
                           
                        }
                    });
                }
            });
        });
    }
});




// Handle showing the user creation form when clicking "Add User" button
let addUserBtn = document.querySelector('.header .right button');
addUserBtn.addEventListener('click', () => {
    let createUser = document.querySelector('.createUser');
    gsap.to(createUser, {
        duration: 1.6,
        ease: "power3.out",
        y: "100%"
    });
});

// Handle hiding the user creation form when clicking the top icon (like a close button)
let userTopNone = document.querySelector('.createUser .mastercontainer .left i');
userTopNone.addEventListener('click', () => {
    let createUser = document.querySelector('.createUser');
    gsap.to(createUser, {
        duration: 1.6,
        delay: 0.1,
        ease: "power3.out",
        y: "-100%"
    });
});

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
//   meeeee
settingSide.addEventListener('click',(e)=> {
    e.stopPropagation()
})
window.addEventListener('click',function(e) {
    if (e.target !== settingSide ) {
        settingSide.classList.remove('active')
        iconSetting.classList.remove('fa-spin')
        gsap.to(settingSide,{
            x:0,
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
// the question marke ???

ulLiChoise.forEach((ele) => {
    ele.onclick = function() {
        // Remove 'active' class from all list items
        ulLiChoise.forEach((e) => {
            e.classList.remove('active');
        });

        // Add 'active' class to the clicked item
        this.classList.add('active');
        numOfMethod = this.dataset.method;

        // Hide both boxes (Affine and Cesar) by default when any new li is selected
        questionIcon.classList.remove("active");
        takeaffine.classList.remove('active');
        takecesar.classList.remove('active');

        // Show the relevant question icon and box based on the selected method
        if (numOfMethod === "2") {
            questionIcon.classList.add("active"); // Show the question icon for Affine
            takeaffine.classList.add("active");   // Immediately show the Affine box
        } else if (numOfMethod === "5" || numOfMethod === "6") {
            questionIcon.classList.add("active"); // Show the question icon for Cesar
            takecesar.classList.add("active");    // Immediately show the Cesar box
        }
    }
});

// Toggle box visibility on question icon click (optional, can be removed if auto-show is preferred)
questionIcon.addEventListener('click', function() {
    if (numOfMethod === "2") {
        takeaffine.classList.toggle('active'); 
    } else if (numOfMethod === "5" || numOfMethod === '6') {
        takecesar.classList.toggle('active');  
    }else if(numOfMethod === "s1" || numOfMethod === 's2'){
        takestg.classList.toggle('active');  
    }else if(numOfMethod === "s3") {
        takestgColumn.classList.toggle('active'); 
    }
});

ulLiChoisestg.forEach((ele) => {
    ele.onclick = function() {
        ulLiChoisestg.forEach((e) => {
            e.classList.remove('active');
        });
        this.classList.add('active');
        numOfMethod = this.dataset.method;
        takestg.classList.remove('active');
        takestgColumn.classList.remove('active');
        questionIcon.classList.add("active"); 

        if (numOfMethod === "s3") {
            takestgColumn.classList.add("active");
        } else {      
            takestg.classList.add("active");
        }
         
    }
});

