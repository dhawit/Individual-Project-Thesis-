document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const emailError = document.getElementById('emailError');
    const passwordError = document.getElementById('passwordError');
  
    form.addEventListener('submit', (event) => {
      let valid = true;
  
      // Clear previous error messages
      emailError.textContent = '';
      passwordError.textContent = '';
  
      // Email validation
      if (!emailInput.value) {
        emailError.textContent = 'Email is required';
        valid = false;
      } else if (!validateEmail(emailInput.value)) {
        emailError.textContent = 'Please enter a valid email address';
        valid = false;
      }
  
      // Password validation
      if (!passwordInput.value) {
        passwordError.textContent = 'Password is required';
        valid = false;
      }
  
      if (!valid) {
        event.preventDefault();
      }
    });
  
    function validateEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(String(email).toLowerCase());
    }
  });
  