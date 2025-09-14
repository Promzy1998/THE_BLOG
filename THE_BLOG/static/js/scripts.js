 // Creating components or calling out html classes 
 const btn = document.querySelectorAll(".account_btn")
 const first = document.querySelector(".Signup_container")
 const second = document.querySelector(".Login_container")
 const Log=document.querySelector(".Log")
 const Sig = document.querySelector(".Sig")
 const account_btn=document.querySelector(".account_btn")
 const login=document.querySelector(".form-login")
 const sign=document.querySelector(".form_sign")
 const transitionbody = document.querySelector(".transition-body")
 const acct=document.querySelector(".acct")
 // creating a kind of toggling mechanism by overiding initial as true and false 
 let initial=true
 btn.forEach((btn)=>{
     btn.addEventListener('click',()=>{
        account_btn.classList.add("btn")
       // initial turns false and vice-versa
         initial=!initial
         if(initial){
             //this takes place when the initial becomes true
             Sig.classList.remove("dnone")
             Log.classList.remove("dblock")
             sign.classList.add("dnone")
             acct.classList.add("acct")
             login.classList.remove("dnone", "transition")
             transitionbody.classList.add("translateright")
             transitionbody.classList.remove("translateleft")
             first.classList.remove('color','transition','Sig-Config-Mediaquery')
             second.classList.remove( 'Log-Config-Mediaquery')
           
            
         }
    
         else{
             // else this should initially take place
             Sig.classList.add("dnone")
             Log.classList.add("dblock", "transition","btn")
             sign.classList.remove("dnone")
             login.classList.add("dnone", "transition")
             first.classList.add('color', 'transition','Sig-Config-Mediaquery')
             second.classList.add('Log-Config-Mediaquery')
             second.classList.remove('color','transition')
             transitionbody.classList.remove("translateright")
             transitionbody.classList.add("translateleft")
             acct.classList.remove("acct")
            
            
           
         }
     })
 })
// declaration of  input fields and togglers 
 document.addEventListener("DOMContentLoaded", () => {
    const password = document.getElementById("password");
    const cpassword = document.getElementById("confirmpassword");
    const passLog = document.getElementById("passLog");
    const modal_password = document.getElementById("modal_password");
    const login_modal = document.getElementById("login_modal");
    const strengthText = document.getElementById("strength");
    const eyeToggler = document.getElementById('toggler');
    const confirmToggler = document.getElementById('confirmtoggler');
    const loginToggler = document.getElementById('Login_toggle');
    const button = document.getElementById("btn");
    const button_login=document.getElementById("btn_login")

    let opacityState = {}; // Store opacity state for each input

   

  
    [password, cpassword, passLog].forEach(input => {
        // for each input field add eventlistener of input trigger  
        input.addEventListener("input", () => {
              // Automatically trim out space on input for all fields
            trimInput(input);
            if (input === password || cpassword){
                checkStrength();
                checkMatch();
            }
            if (input === passLog) autoTogglerVisibilityAndStrength(passLog.value, loginToggler)
        });
    });

    eyeToggler.addEventListener("click", () => toggleVisibilityOpacity(password, eyeToggler));
    confirmToggler.addEventListener("click", () => toggleVisibilityOpacity(cpassword, confirmToggler));
    loginToggler.addEventListener("click", () => toggleVisibilityOpacity(passLog, loginToggler));

    button.addEventListener("click", checkMatch);
    button_login.addEventListener("click", () => login_validate(passLog));
 // Helper function to trim input fields
    function trimInput(input) {
        if (input) input.value = input.value.trim();
    }

    function checkStrength() {
        const passwordV = password.value;
        // created a variable that increment if true
        let strength = 0;
        // if (!passwordV) return;
        // strengthText.style.display="inline"
         // IF false function that toggle visiblity on or off  detecting
        // if the input field is empty or not
        autoTogglerVisibilityAndStrength(passwordV, eyeToggler);
        // function still checks if the input field triggered display strength result
        autoTogglerVisibilityAndStrength(strengthText, strengthText)
        if (passwordV.length >= 8) strength++;
        if (/[A-Z]/.test(passwordV)) strength++;
        if (/[a-z]/.test(passwordV)) strength++;
        if (/[0-9]/.test(passwordV)) strength++;
        if (/[@$!%*?&]/.test(passwordV)) strength++;
        const strengthLevels = ["Weak ❌", "Moderate ⚠️", "Strong ✅"];
        const [color, level] = strength <= 2 ? ["red", strengthLevels[0]] :
                                strength <= 4 ? ["orange", strengthLevels[1]] : ["green", strengthLevels[2]];
        strengthText.style.color = color;
        strengthText.innerHTML = `Strength: ${level}`;
    }

    function checkMatch() {
        const passwordValue = password.value;
        const cpasswordValue = cpassword.value;
        modal_password.style.display = 'inline';
        //  // function that toggle visiblity on or off  detecting
        // if the input field is empty or not
        autoTogglerVisibilityAndStrength(cpasswordValue, confirmToggler)
        if (!cpasswordValue) {
            modal_password.innerHTML = "⚠️ Please confirm your password!";
            modal_password.style.color = "orange";
        } else {
            modal_password.innerHTML = passwordValue === cpasswordValue ? "✅ Passwords match!" : "❌ Passwords do not match!";
            modal_password.style.color = passwordValue === cpasswordValue ? "green" : "red";
        }
    }
    // toggle's opacity state for the toggles
    function toggleVisibilityOpacity(input, toggler) {
        if (!input) return;
        opacityState[input.id] = !opacityState[input.id]; // Toggle opacity state
        toggler.style.opacity = opacityState[input.id] ? 1 : 0.2;
        input.type = input.type === "password" ? "text" : "password";
    }
    // function toggles visibility for togglers and strength if input field is triggered   
    function autoTogglerVisibilityAndStrength(field_input, toggler) {
        toggler.style.display = field_input ? "inline" : "none";
       
    }
    function login_validate(input){
         return false
        // login_modal.style.display="inline"
        // login_modal.style.fontWeight="light"
        // login_modal.innerHTML = input.value ? "" : "name or password can't be empty!"
        

    }
});
