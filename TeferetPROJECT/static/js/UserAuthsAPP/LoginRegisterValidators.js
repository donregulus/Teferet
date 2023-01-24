//Function used to reveal the password
const togglePasswordSignup = document.querySelector('#togglePasswordSignup');
togglePasswordSignup.addEventListener('click', function (e) {
    // toggle the type attribute
    const password = document.querySelector('#id_password1');
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    // toggle the eye slash icon
    this.classList.toggle('fa-eye-slash');
});

const toggleConfirmPasswordSignup = document.querySelector('#togglePasswordConfirm');
toggleConfirmPasswordSignup.addEventListener('click', function (e) {
    // toggle the type attribute
    const password = document.querySelector('#id_password2');
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    // toggle the eye slash icon
    this.classList.toggle('fa-eye-slash');
});


const togglePasswordSignin = document.querySelector('#togglePasswordLogin');
togglePasswordSignin.addEventListener('click', function (e) {
    // toggle the type attribute
    const password = document.querySelector('#id_password');
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    // toggle the eye slash icon
    this.classList.toggle('fa-eye-slash');
});



//overlay display
const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('containerSign');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

//Input Validations register
const SignupButton = document.getElementById('SignupButton');
SignupButton.disabled = true;

const lastName           = document.querySelector('#id_last_name');
const firsName           = document.querySelector('#id_first_name');
const email              = document.querySelector('#id_email');
const username           = document.querySelector('#id_username');
const password           = document.querySelector('#id_password1');
const confirmpassword    = document.querySelector('#id_password2');

//Utilities Functions
const isRequired = value => value === '' ? false : true;
const isBetween = (length, min, max) => length < min || length > max ? false : true;
const isEmailValid = (email) => {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
};
const isPasswordSecure = (password) => {
    const re = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
    return re.test(password);
};

const setError = (element, message) => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = message;
    inputControl.classList.add('error');
    inputControl.classList.remove('success')
}

const setSuccess = element => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');
    
    errorDisplay.innerText = '';
    inputControl.classList.add('success');
    inputControl.classList.remove('error');
};


//Validation Functions
let checkEmailValid           = false;
let checkFirstNameValid       = false;
let checkLastNameValid        = false;
let checkUsertNameValid       = false;
let checkPasswordValid        = false;
let checkConfirmPasswordValid = false;



const enableButton = () => {

    if(checkFirstNameValid && checkLastNameValid && checkUsertNameValid && checkEmailValid && checkPasswordValid && checkConfirmPasswordValid)
    {
        SignupButton.disabled = false;
    }
    else
    {
        SignupButton.disabled = true;
    }

}

const checkFirstName = () => {

    let valid = false;
    const min = 3,
        max = 30;
    const name = firsName.value.trim();

    if (!isBetween(name.length, min, max)) {
        setError(firsName, `FirstName must be between ${min} and ${max} characters.`)
        checkFirstNameValid = false;
        enableButton()
    } else {
        setSuccess(firsName);
        checkFirstNameValid = true;      
        enableButton()  
    }
    
}
firsName.addEventListener('input', checkFirstName);


const checkLastName = () => {

    let valid = false;
    const min = 3,
        max = 150;
    const name = lastName.value.trim();

    if (!isBetween(name.length, min, max)) {
        setError(lastName, `LastName must be between ${min} and ${max} characters.`)
        checkLastNameValid = false;
        enableButton()
    } else {
        setSuccess(lastName);
        checkLastNameValid = true;   
        enableButton()     
    }    
}
lastName.addEventListener('input', checkLastName);


const checkEmail = () => {
    let valid = false;
    const emailv = email.value.trim();
   if (!isEmailValid(emailv)) {
        setError(email, 'Email is not valid.')
        checkEmailValid = false;   
        enableButton()
    } else {
        setSuccess(email);
        checkEmailValid = true;   
        enableButton()
    }    
}
email.addEventListener('input', checkEmail);


const checkUsertName = () => {

    let valid = false;
    const min = 3,
        max = 150;
    const name = username.value.trim();

    if (!isBetween(name.length, min, max)) {
        setError(username, `LastName must be between ${min} and ${max} characters.`)
        checkUsertNameValid = false;
        enableButton()
    } else {
        setSuccess(username);
        checkUsertNameValid = true;
        enableButton()
    }    
}
username.addEventListener('input', checkUsertName);

const checkPassword = () => {

    let valid = false;

    const passwordValue = password.value.trim();

    if (!isPasswordSecure(passwordValue)) {
        setError(password, 'Password format ex: AAaa11@@');
        checkPasswordValid = false
        enableButton()
    } else {
        setSuccess(password);
        checkPasswordValid = true   
        enableButton()     
    }
    checkConfirmPassword();    
};
password.addEventListener('input', checkPassword);


const checkConfirmPassword = () => {
    let valid = false;
    // check confirm password
    const confirmPasswordValue = confirmpassword.value.trim();
    const passwordvalue = password.value.trim();

     if (passwordvalue !== confirmPasswordValue) {
        setError(confirmpassword, 'Confirm password does not match');
        checkConfirmPasswordValid = false;
        enableButton()
    } else {
        setSuccess(confirmpassword);
        checkConfirmPasswordValid = true;
        enableButton()
    }
};
confirmpassword.addEventListener('input', checkConfirmPassword);



//Input Validations signin
const SigninButton = document.getElementById('SigninButton');
SigninButton.disabled = true;
const usernameLogin = document.querySelector('#id_usernameLogin');
const passwordLogin = document.querySelector('#id_password');

let checkusernameLoginValid = false;   
let checkPasswordLoginValid = false;

const enableButtonLogin = () => {

    if(checkusernameLoginValid&&checkPasswordLoginValid)
    {
        SigninButton.disabled = false;
    }
    else
    {
        SigninButton.disabled = true;
    }
}

const checkusernameLogin = () => {
    let valid = false;
    const emailv = usernameLogin.value.trim();
   if (!isRequired(emailv)) {
        setError(usernameLogin, 'Username can not be blank.')
        checkusernameLoginValid = false;   
        enableButtonLogin()
    } else {
        setSuccess(usernameLogin);
        checkusernameLoginValid = true;   
        enableButtonLogin()
    }    
}
usernameLogin.addEventListener('input', checkusernameLogin);

const checkPasswordLogin = () => {
    let valid = false;
    // check confirm password    
    const passwordvalue = passwordLogin.value.trim();

    if (!isRequired(passwordvalue)) {
        setError(passwordLogin, 'Password can not be blank.')
        checkPasswordLoginValid = false;   
        enableButtonLogin()
    } else {
        setSuccess(passwordLogin);
        checkPasswordLoginValid = true;
        enableButtonLogin()
    }
};
passwordLogin.addEventListener('input', checkPasswordLogin);


