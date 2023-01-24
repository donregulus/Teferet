//Function used to reveal the password
const toggleConfirmPasswordSignup = document.querySelector('#togglePasswordConfirm');
toggleConfirmPasswordSignup.addEventListener('click', function (e) {
    // toggle the type attribute
    const password = document.querySelector('#id_password2');
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    // toggle the eye slash icon
    this.classList.toggle('fa-eye-slash');
});


const togglePassword = document.querySelector('#togglePassword');
togglePassword.addEventListener('click', function (e) {
    // toggle the type attribute
    const password = document.querySelector('#id_password1');
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    // toggle the eye slash icon
    this.classList.toggle('fa-eye-slash');
});

//Utilities Functions
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


//Input Validations reset password
const ResetPasswordButton = document.getElementById('ResetPasswordButton');
ResetPasswordButton.disabled = true;
let checkPasswordValid        = false;
let checkConfirmPasswordValid = false;

const enableButton = () => {

    if( checkPasswordValid && checkConfirmPasswordValid)
    {
        ResetPasswordButton.disabled = false;
    }
    else
    {
        ResetPasswordButton.disabled = true;
    }

}

const password           = document.querySelector('#id_password1');
const confirmpassword    = document.querySelector('#id_password2');


const checkPassword = () => {    

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
