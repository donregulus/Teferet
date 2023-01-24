//utilities function 
const isEmailValid = (email) => {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
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


//Input validation forgot password
const ResetPasswordButton    = document.querySelector('#ResetPasswordButton');
ResetPasswordButton.disabled = true;
const ResetPasswordEmail     = document.querySelector('#id_EmailResetPassword');
let checkEmailResetPasswordValid = false;   


const enableButton = () => {

    if(checkEmailResetPasswordValid)
    {
        ResetPasswordButton.disabled = false;
    }
    else
    {
        ResetPasswordButton.disabled = true;
    }

}

const checkEmailResetPassword = () => {
    let valid = false;
    const emailv = ResetPasswordEmail.value.trim();
   if (!isEmailValid(emailv)) {
        setError(ResetPasswordEmail, 'Email is not valid.')
        checkEmailResetPasswordValid = false;   
        enableButton()
    } else {
        setSuccess(ResetPasswordEmail);
        checkEmailResetPasswordValid = true;   
        enableButton()
    }    
}
ResetPasswordEmail.addEventListener('input', checkEmailResetPassword);