// Authentication Modal JavaScript
// Login and Registration UI for Singing Bowl & Gong House

// Create authentication modal HTML structure
function createAuthModal() {
  const modalHTML = `
    <div class="auth-modal" id="authModal" role="dialog" aria-labelledby="authModalTitle" aria-hidden="true">
      <div class="auth-modal-overlay" onclick="closeAuthModal()"></div>
      <div class="auth-modal-container">
        <div class="auth-modal-header">
          <div class="auth-modal-logo-container">
            <img src="images/logo.jpg" alt="Singing Bowl & Gong House Logo" class="auth-modal-logo">
            <h2 id="authModalTitle">
              <span id="authModalTitleText">Welcome</span>
            </h2>
          </div>
          <button class="auth-modal-close" onclick="closeAuthModal()" aria-label="Close auth modal">
            &times;
          </button>
        </div>
        <div class="auth-modal-body">
          <!-- Tab Switcher -->
          <div class="auth-tabs">
            <button class="auth-tab active" id="loginTab" onclick="switchAuthTab('login')">
              <i class="fas fa-sign-in-alt"></i> Login
            </button>
            <button class="auth-tab" id="registerTab" onclick="switchAuthTab('register')">
              <i class="fas fa-user-plus"></i> Register
            </button>
          </div>

          <!-- Login Form -->
          <div class="auth-form-container" id="loginFormContainer">
            <form id="loginForm" class="auth-form">
              <div class="auth-form-group">
                <label for="loginUsername">Username <span class="required">*</span></label>
                <div class="auth-input-with-icon">
                  <i class="fas fa-user"></i>
                  <input type="text" id="loginUsername" name="username" placeholder="Enter your username" required>
                </div>
              </div>

              <div class="auth-form-group">
                <label for="loginPassword">Password <span class="required">*</span></label>
                <div class="auth-input-with-icon">
                  <i class="fas fa-lock"></i>
                  <input type="password" id="loginPassword" name="password" placeholder="Enter your password" required>
                  <button type="button" class="password-toggle" onclick="togglePassword('loginPassword')">
                    <i class="fas fa-eye"></i>
                  </button>
                </div>
              </div>

              <div class="auth-form-options">
                <label class="auth-checkbox">
                  <input type="checkbox" id="rememberMe">
                  <span>Remember me</span>
                </label>
                <a href="#" class="auth-forgot-link">Forgot password?</a>
              </div>

              <button type="submit" class="auth-submit-btn" id="loginSubmitBtn">
                <span class="btn-text">
                  <i class="fas fa-sign-in-alt" style="margin-right: 8px;"></i>
                  Login
                </span>
              </button>
            </form>
          </div>

          <!-- Register Form -->
          <div class="auth-form-container" id="registerFormContainer" style="display: none;">
            <form id="registerForm" class="auth-form">
              <div class="auth-form-row">
                <div class="auth-form-group">
                  <label for="registerUsername">Username <span class="required">*</span></label>
                  <div class="auth-input-with-icon">
                    <i class="fas fa-user"></i>
                    <input type="text" id="registerUsername" name="username" placeholder="Choose a username" required>
                  </div>
                </div>

                <div class="auth-form-group">
                  <label for="registerEmail">Email <span class="required">*</span></label>
                  <div class="auth-input-with-icon">
                    <i class="fas fa-envelope"></i>
                    <input type="email" id="registerEmail" name="email" placeholder="your.email@example.com" required>
                  </div>
                </div>
              </div>

              <div class="auth-form-row">
                <div class="auth-form-group">
                  <label for="registerFirstName">First Name</label>
                  <div class="auth-input-with-icon">
                    <i class="fas fa-id-card"></i>
                    <input type="text" id="registerFirstName" name="first_name" placeholder="First name">
                  </div>
                </div>

                <div class="auth-form-group">
                  <label for="registerLastName">Last Name</label>
                  <div class="auth-input-with-icon">
                    <i class="fas fa-id-card"></i>
                    <input type="text" id="registerLastName" name="last_name" placeholder="Last name">
                  </div>
                </div>
              </div>

              <div class="auth-form-group">
                <label for="registerPassword">Password <span class="required">*</span></label>
                <div class="auth-input-with-icon">
                  <i class="fas fa-lock"></i>
                  <input type="password" id="registerPassword" name="password" placeholder="Create a password" required>
                  <button type="button" class="password-toggle" onclick="togglePassword('registerPassword')">
                    <i class="fas fa-eye"></i>
                  </button>
                </div>
                <small class="auth-help-text">Must be at least 8 characters</small>
              </div>

              <div class="auth-form-group">
                <label for="registerPassword2">Confirm Password <span class="required">*</span></label>
                <div class="auth-input-with-icon">
                  <i class="fas fa-lock"></i>
                  <input type="password" id="registerPassword2" name="password2" placeholder="Confirm your password" required>
                  <button type="button" class="password-toggle" onclick="togglePassword('registerPassword2')">
                    <i class="fas fa-eye"></i>
                  </button>
                </div>
              </div>

              <div class="auth-form-note">
                <label class="auth-checkbox">
                  <input type="checkbox" id="agreeTerms" required>
                  <span>I agree to the <a href="#" target="_blank">Terms & Conditions</a> and <a href="#" target="_blank">Privacy Policy</a></span>
                </label>
              </div>

              <button type="submit" class="auth-submit-btn" id="registerSubmitBtn">
                <span class="btn-text">
                  <i class="fas fa-user-plus" style="margin-right: 8px;"></i>
                  Create Account
                </span>
              </button>
            </form>
          </div>

          <!-- Loading State -->
          <div class="auth-loading" id="authLoading">
            <div class="auth-spinner"></div>
            <p id="authLoadingText">Processing...</p>
          </div>

          <!-- Success State -->
          <div class="auth-success" id="authSuccess">
            <div class="auth-success-icon">
              <i class="fas fa-check-circle"></i>
            </div>
            <h3 id="authSuccessTitle">Success!</h3>
            <p id="authSuccessMessage"></p>
            <button type="button" class="auth-submit-btn" onclick="closeAuthModal()" style="margin-top: 24px; max-width: 300px;">
              <span class="btn-text">Continue</span>
            </button>
          </div>

          <!-- Error Message Container -->
          <div class="auth-error-container" id="authErrorContainer"></div>
        </div>
      </div>
    </div>
  `;
  

  // Add modal to body if it doesn't exist
  if (!document.getElementById('authModal')) {
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    setupAuthForms();
  }
}

// Setup form event listeners
function setupAuthForms() {
  const loginForm = document.getElementById('loginForm');
  const registerForm = document.getElementById('registerForm');
  
  if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
  }
  
  if (registerForm) {
    registerForm.addEventListener('submit', handleRegister);
    
    // Password match validation
    const password2 = document.getElementById('registerPassword2');
    if (password2) {
      password2.addEventListener('input', validatePasswordMatch);
    }
  }

  // Close modal on Escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      const modal = document.getElementById('authModal');
      if (modal && modal.classList.contains('active')) {
        closeAuthModal();
      }
    }
  });
}

// Switch between login and register tabs
function switchAuthTab(tab) {
  const loginTab = document.getElementById('loginTab');
  const registerTab = document.getElementById('registerTab');
  const loginContainer = document.getElementById('loginFormContainer');
  const registerContainer = document.getElementById('registerFormContainer');
  const titleText = document.getElementById('authModalTitleText');
  
  if (tab === 'login') {
    loginTab.classList.add('active');
    registerTab.classList.remove('active');
    loginContainer.style.display = 'block';
    registerContainer.style.display = 'none';
    if (titleText) titleText.textContent = 'Welcome Back';
  } else {
    registerTab.classList.add('active');
    loginTab.classList.remove('active');
    loginContainer.style.display = 'none';
    registerContainer.style.display = 'block';
    if (titleText) titleText.textContent = 'Create Account';
  }
  
  // Clear any error messages
  clearAuthErrors();
}

// Toggle password visibility
function togglePassword(inputId) {
  const input = document.getElementById(inputId);
  const toggle = input.nextElementSibling;
  const icon = toggle.querySelector('i');
  
  if (input.type === 'password') {
    input.type = 'text';
    icon.classList.remove('fa-eye');
    icon.classList.add('fa-eye-slash');
  } else {
    input.type = 'password';
    icon.classList.remove('fa-eye-slash');
    icon.classList.add('fa-eye');
  }
}

// Validate password match
function validatePasswordMatch() {
  const password = document.getElementById('registerPassword');
  const password2 = document.getElementById('registerPassword2');
  
  if (password2.value && password.value !== password2.value) {
    password2.setCustomValidity('Passwords do not match');
    password2.style.borderColor = '#e74c3c';
  } else {
    password2.setCustomValidity('');
    password2.style.borderColor = '';
  }
}

// Handle login form submission
async function handleLogin(e) {
  e.preventDefault();
  
  const form = document.getElementById('loginForm');
  const submitBtn = document.getElementById('loginSubmitBtn');
  const loading = document.getElementById('authLoading');
  const errorContainer = document.getElementById('authErrorContainer');
  
  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }
  
  // Disable submit button
  submitBtn.disabled = true;
  
  // Show loading state
  form.style.display = 'none';
  loading.classList.add('active');
  clearAuthErrors();
  
  // Collect form data
  const formData = new FormData(form);
  const credentials = {
    username: formData.get('username'),
    password: formData.get('password'),
  };
  
  // Submit to API
  if (typeof window.apiUtils !== 'undefined' && window.apiUtils.loginUser) {
    try {
      const response = await window.apiUtils.loginUser(credentials);
      
      // Success
      loading.classList.remove('active');
      
      // Check email verification status
      if (response.email_verified === false) {
        showAuthSuccess(
          'Login Successful!', 
          'Welcome back! Please verify your email to access all features. Check your inbox for the verification link.'
        );
        // Show email verification notice
        showEmailVerificationNotice(response.user.email);
      } else {
        showAuthSuccess('Login Successful!', 'Welcome back! You can now book services.');
      }
      
      // Update UI to show user is logged in
      updateAuthUI(true, response.user);
      
      // Close modal after 3 seconds (longer if email not verified)
      setTimeout(() => {
        closeAuthModal();
      }, response.email_verified === false ? 4000 : 2000);
      
    } catch (error) {
      // Error
      loading.classList.remove('active');
      form.style.display = 'block';
      submitBtn.disabled = false;
      showAuthError(error.message || 'Login failed. Please check your credentials.');
    }
  } else {
    loading.classList.remove('active');
    form.style.display = 'block';
    submitBtn.disabled = false;
    showAuthError('API utilities not loaded. Please refresh the page.');
  }
}

// Handle register form submission
async function handleRegister(e) {
  e.preventDefault();
  
  const form = document.getElementById('registerForm');
  const submitBtn = document.getElementById('registerSubmitBtn');
  const loading = document.getElementById('authLoading');
  
  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }
  
  // Validate password match
  const password = document.getElementById('registerPassword').value;
  const password2 = document.getElementById('registerPassword2').value;
  if (password !== password2) {
    showAuthError('Passwords do not match');
    return;
  }
  
  if (password.length < 8) {
    showAuthError('Password must be at least 8 characters long');
    return;
  }
  
  // Disable submit button
  submitBtn.disabled = true;
  
  // Show loading state
  form.style.display = 'none';
  loading.classList.add('active');
  clearAuthErrors();
  
  // Collect form data
  const formData = new FormData(form);
  const userData = {
    username: formData.get('username'),
    email: formData.get('email'),
    password: formData.get('password'),
    password2: formData.get('password2'),
    first_name: formData.get('first_name') || '',
    last_name: formData.get('last_name') || '',
  };
  
  // Submit to API
  if (typeof window.apiUtils !== 'undefined' && window.apiUtils.registerUser) {
    try {
      const response = await window.apiUtils.registerUser(userData);
      
      // Success
      loading.classList.remove('active');
      
      // Show email verification message
      const emailMessage = response.email_verification_sent 
        ? 'Please check your email to verify your account before logging in.'
        : 'Account created, but verification email could not be sent. Please contact support.';
      
      showAuthSuccess(
        'Registration Successful!', 
        emailMessage
      );
      
      // Show email verification notice
      if (response.user && response.user.email) {
        showEmailVerificationNotice(response.user.email);
      }
      
      // Update UI to show user is logged in (but email not verified)
      updateAuthUI(true, response.user);
      
      // Close modal after 4 seconds to give time to read message
      setTimeout(() => {
        closeAuthModal();
      }, 4000);
      
    } catch (error) {
      // Error
      loading.classList.remove('active');
      form.style.display = 'block';
      submitBtn.disabled = false;
      showAuthError(error.message || 'Registration failed. Please try again.');
    }
  } else {
    loading.classList.remove('active');
    form.style.display = 'block';
    submitBtn.disabled = false;
    showAuthError('API utilities not loaded. Please refresh the page.');
  }
}

// Show success message
function showAuthSuccess(title, message) {
  const success = document.getElementById('authSuccess');
  const successTitle = document.getElementById('authSuccessTitle');
  const successMessage = document.getElementById('authSuccessMessage');
  
  if (success && successTitle && successMessage) {
    successTitle.textContent = title;
    successMessage.textContent = message;
    success.classList.add('active');
  }
}

// Show error message
function showAuthError(message) {
  const errorContainer = document.getElementById('authErrorContainer');
  if (errorContainer) {
    errorContainer.innerHTML = `
      <div class="auth-error-message">
        <i class="fas fa-exclamation-circle"></i>
        <span>${message}</span>
      </div>
    `;
    errorContainer.style.display = 'block';
    
    // Auto remove after 5 seconds
    setTimeout(() => {
      errorContainer.style.display = 'none';
    }, 5000);
  }
}

// Clear error messages
function clearAuthErrors() {
  const errorContainer = document.getElementById('authErrorContainer');
  if (errorContainer) {
    errorContainer.innerHTML = '';
    errorContainer.style.display = 'none';
  }
}

// Show email verification notice
function showEmailVerificationNotice(email) {
  // Remove existing notice if any
  const existingNotice = document.getElementById('emailVerificationNotice');
  if (existingNotice) {
    existingNotice.remove();
  }
  
  // Create notice element
  const notice = document.createElement('div');
  notice.id = 'emailVerificationNotice';
  notice.className = 'email-verification-notice';
  notice.innerHTML = `
    <div class="email-verification-content">
      <i class="fas fa-envelope-circle-check"></i>
      <div class="email-verification-text">
        <strong>Verify Your Email</strong>
        <p>We've sent a verification link to <strong>${email}</strong>. Please check your inbox and click the link to verify your account.</p>
        <button type="button" class="resend-verification-btn" onclick="handleResendVerification()">
          <i class="fas fa-paper-plane"></i> Resend Verification Email
        </button>
      </div>
      <button type="button" class="email-verification-close" onclick="this.parentElement.parentElement.remove()">
        <i class="fas fa-times"></i>
      </button>
    </div>
  `;
  
  // Insert at top of body
  document.body.insertBefore(notice, document.body.firstChild);
  
  // Animate in
  setTimeout(() => {
    notice.classList.add('show');
  }, 100);
}

// Handle resend verification email
async function handleResendVerification() {
  const btn = document.querySelector('.resend-verification-btn');
  if (!btn) return;
  
  const originalText = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
  
  try {
    if (typeof window.apiUtils !== 'undefined' && window.apiUtils.resendVerificationEmail) {
      const response = await window.apiUtils.resendVerificationEmail();
      
      if (response.email_sent) {
        btn.innerHTML = '<i class="fas fa-check"></i> Email Sent!';
        btn.style.background = '#10b548';
        setTimeout(() => {
          btn.innerHTML = originalText;
          btn.style.background = '';
          btn.disabled = false;
        }, 2000);
      } else {
        throw new Error('Failed to send verification email');
      }
    } else {
      throw new Error('API utilities not loaded');
    }
  } catch (error) {
    btn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error';
    btn.style.background = '#e74c3c';
    setTimeout(() => {
      btn.innerHTML = originalText;
      btn.style.background = '';
      btn.disabled = false;
    }, 2000);
    alert('Failed to resend verification email: ' + error.message);
  }
}

// Make functions globally available
window.handleResendVerification = handleResendVerification;

// Update UI based on authentication status
function updateAuthUI(isAuthenticated, user = null) {
  // Update header/login button if it exists
  const loginButtons = document.querySelectorAll('.login-btn, .auth-btn');
  loginButtons.forEach(btn => {
    if (isAuthenticated) {
      btn.innerHTML = `<i class="fas fa-user-check"></i> ${user ? user.username : 'Logged In'}`;
      btn.onclick = handleLogout;
      btn.classList.add('logged-in');
    } else {
      btn.innerHTML = '<i class="fas fa-sign-in-alt"></i> Login';
      btn.onclick = openAuthModal;
      btn.classList.remove('logged-in');
    }
  });
  
  // Check auth status on page load
  if (typeof window.apiUtils !== 'undefined' && window.apiUtils.isAuthenticated()) {
    // User is logged in
    updateAuthUI(true);
  }
}

// Handle logout
function handleLogout() {
  if (typeof window.apiUtils !== 'undefined' && window.apiUtils.logoutUser) {
    window.apiUtils.logoutUser();
    updateAuthUI(false);
    if (window.apiUtils.showSuccessMessage) {
      window.apiUtils.showSuccessMessage('You have been logged out successfully.');
    }
  }
}

// Open authentication modal
function openAuthModal(tab = 'login') {
  createAuthModal();
  const modal = document.getElementById('authModal');
  const loginForm = document.getElementById('loginForm');
  const registerForm = document.getElementById('registerForm');
  const loading = document.getElementById('authLoading');
  const success = document.getElementById('authSuccess');
  
  if (modal) {
    // Reset forms
    if (loginForm) {
      loginForm.reset();
      loginForm.style.display = 'block';
    }
    if (registerForm) {
      registerForm.reset();
    }
    if (loading) loading.classList.remove('active');
    if (success) success.classList.remove('active');
    clearAuthErrors();
    
    // Switch to requested tab
    switchAuthTab(tab);
    
    // Show modal
    modal.classList.add('active');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    
    // Animate modal entrance with GSAP if available
    if (typeof gsap !== 'undefined') {
      gsap.fromTo('.auth-modal-container', 
        { 
          scale: 0.9, 
          y: 30, 
          opacity: 0,
          rotationX: 5
        },
        { 
          scale: 1, 
          y: 0, 
          opacity: 1,
          rotationX: 0,
          duration: 0.6, 
          ease: 'power3.out'
        }
      );
    }
    
    // Focus first input
    setTimeout(() => {
      const firstInput = modal.querySelector('input[type="text"], input[type="email"]');
      if (firstInput) firstInput.focus();
    }, 400);
  }
}

// Close authentication modal
function closeAuthModal() {
  const modal = document.getElementById('authModal');
  if (modal) {
    // Animate modal exit with GSAP if available
    if (typeof gsap !== 'undefined') {
      gsap.to('.auth-modal-container', {
        scale: 0.9,
        y: 30,
        opacity: 0,
        rotationX: 5,
        duration: 0.4,
        ease: 'power2.in',
        onComplete: () => {
          modal.classList.remove('active');
          modal.setAttribute('aria-hidden', 'true');
          document.body.style.overflow = '';
        }
      });
    } else {
      modal.classList.remove('active');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }
  }
}

// Make functions globally available
window.openAuthModal = openAuthModal;
window.closeAuthModal = closeAuthModal;
window.switchAuthTab = switchAuthTab;
window.togglePassword = togglePassword;
window.handleLogout = handleLogout;

// Initialize on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    createAuthModal();
    updateAuthUI(window.apiUtils && window.apiUtils.isAuthenticated());
  });
} else {
  createAuthModal();
  updateAuthUI(window.apiUtils && window.apiUtils.isAuthenticated());
}

