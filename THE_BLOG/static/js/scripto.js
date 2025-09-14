const loginButton = document.getElementById('login-btn');
const signupButton = document.getElementById('signup-btn');
const formWrapper = document.querySelector('.form-wrapper');
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');

loginButton.addEventListener('click', () => {
  loginButton.classList.add('active');
  signupButton.classList.remove('active');
  formWrapper.style.transform = 'translateX(0)';
  loginForm.classList.add('active');
  signupForm.classList.remove('active');
});

signupButton.addEventListener('click', () => {
  signupButton.classList.add('active');
  loginButton.classList.remove('active');
  formWrapper.style.transform = 'translateX(-50%)';
  signupForm.classList.add('active');
  loginForm.classList.remove('active');
});
