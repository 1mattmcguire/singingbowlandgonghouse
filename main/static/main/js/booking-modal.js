// Luxury Booking Modal JavaScript
// Premium Wellness Booking Form

// Course options for dropdown
const courseOptions = {
  'Singing Bowl Course': {
    duration: '3 Days | 5 Hours/Day',
    description: 'Learn the ancient Himalayan techniques of singing bowl healing'
  },
  'Gong Course': {
    duration: '2 Days | 5 Hours/Day',
    description: 'Discover the powerful transformative vibrations of the gong'
  },
  'Handpan Course': {
    duration: '3 Days | 2 Hours/Day',
    description: 'Beginner-friendly handpan course focused on rhythm and flow'
  }
};

// Create booking modal HTML structure
function createBookingModal() {
  const modalHTML = `
    <div class="booking-modal" id="bookingModal" role="dialog" aria-labelledby="bookingModalTitle" aria-hidden="true">
      <div class="booking-modal-overlay" onclick="closeBookingModal()"></div>
      <div class="booking-modal-container">
        <div class="booking-modal-header">
          <h2 id="bookingModalTitle">
            <i class="fas fa-spa" style="margin-right: 12px; color: #d4af37;"></i>
            Book Your Healing Journey
          </h2>
          <button class="booking-modal-close" onclick="closeBookingModal()" aria-label="Close booking modal">
            &times;
          </button>
        </div>
        <div class="booking-modal-body">
          <form id="bookingForm" onsubmit="event.preventDefault(); return false;" action="javascript:void(0);" method="post" novalidate>
            <!-- Service Type Selection -->
            <div class="booking-form-group">
              <label>Service Type <span class="required">*</span></label>
              <div class="booking-service-type">
                <div class="booking-service-option">
                  <input type="radio" id="service-healing" name="serviceType" value="Sound Healing Session" required>
                  <label for="service-healing" class="booking-service-label">
                    <i class="fas fa-spa service-icon"></i>
                    <span class="service-name">Sound Healing Session</span>
                    <span class="service-duration">Personal & Group</span>
                  </label>
                </div>
                <div class="booking-service-option">
                  <input type="radio" id="service-courses" name="serviceType" value="Courses & Trainings" required>
                  <label for="service-courses" class="booking-service-label">
                    <i class="fas fa-graduation-cap service-icon"></i>
                    <span class="service-name">Courses & Trainings</span>
                    <span class="service-duration">Professional Certification</span>
                  </label>
                </div>
              </div>
            </div>

            <!-- Dynamic Course Dropdown (shown only when Courses & Trainings is selected) -->
            <div class="booking-course-dropdown" id="courseDropdown">
              <div class="booking-form-group">
                <label for="courseSelection">Select Course <span class="required">*</span></label>
                <select id="courseSelection" name="courseSelection" class="booking-course-select">
                  <option value="">-- Choose a Course --</option>
                  <option value="Singing Bowl Course">Singing Bowl Course</option>
                  <option value="Gong Course">Gong Course</option>
                  <option value="Handpan Course">Handpan Course</option>
                </select>
              </div>
            </div>

            <!-- Two-Column Layout: Full Name -->
            <div class="booking-form-row">
              <div class="booking-form-group">
                <label for="fullName">Full Name <span class="required">*</span></label>
                <div class="booking-input-with-icon">
                  <i class="fas fa-user"></i>
                  <input type="text" id="fullName" name="fullName" placeholder="Enter your full name" required>
                </div>
              </div>
              <div class="booking-form-group">
                <label for="age">Age <span class="required">*</span></label>
                <div class="booking-input-with-icon age-input">
                  <i class="fas fa-birthday-cake"></i>
                  <input type="number" id="age" name="age" placeholder="Your age" min="16" max="100" required>
                </div>
              </div>
            </div>

            <!-- Two-Column Layout: Email and Phone -->
            <div class="booking-form-row">
              <div class="booking-form-group">
                <label for="email">Email Address <span class="required">*</span></label>
                <div class="booking-input-with-icon">
                  <i class="fas fa-envelope"></i>
                  <input type="email" id="email" name="email" placeholder="your.email@example.com" required>
                </div>
              </div>
              <div class="booking-form-group">
                <label for="phone">Phone / WhatsApp <span class="required">*</span></label>
                <div class="booking-phone-wrapper">
                  <select id="countryCode" name="countryCode" class="booking-country-select" required>
                    <option value="+977" data-country="NP">🇳🇵 +977 (Nepal)</option>
                    <option value="+1" data-country="US">🇺🇸 +1 (USA/Canada)</option>
                    <option value="+44" data-country="GB">🇬🇧 +44 (UK)</option>
                    <option value="+91" data-country="IN">🇮🇳 +91 (India)</option>
                    <option value="+86" data-country="CN">🇨🇳 +86 (China)</option>
                    <option value="+81" data-country="JP">🇯🇵 +81 (Japan)</option>
                    <option value="+82" data-country="KR">🇰🇷 +82 (South Korea)</option>
                    <option value="+61" data-country="AU">🇦🇺 +61 (Australia)</option>
                    <option value="+49" data-country="DE">🇩🇪 +49 (Germany)</option>
                    <option value="+33" data-country="FR">🇫🇷 +33 (France)</option>
                    <option value="+39" data-country="IT">🇮🇹 +39 (Italy)</option>
                    <option value="+34" data-country="ES">🇪🇸 +34 (Spain)</option>
                    <option value="+31" data-country="NL">🇳🇱 +31 (Netherlands)</option>
                    <option value="+41" data-country="CH">🇨🇭 +41 (Switzerland)</option>
                    <option value="+46" data-country="SE">🇸🇪 +46 (Sweden)</option>
                    <option value="+47" data-country="NO">🇳🇴 +47 (Norway)</option>
                    <option value="+45" data-country="DK">🇩🇰 +45 (Denmark)</option>
                    <option value="+358" data-country="FI">🇫🇮 +358 (Finland)</option>
                    <option value="+32" data-country="BE">🇧🇪 +32 (Belgium)</option>
                    <option value="+43" data-country="AT">🇦🇹 +43 (Austria)</option>
                    <option value="+351" data-country="PT">🇵🇹 +351 (Portugal)</option>
                    <option value="+353" data-country="IE">🇮🇪 +353 (Ireland)</option>
                    <option value="+7" data-country="RU">🇷🇺 +7 (Russia)</option>
                    <option value="+971" data-country="AE">🇦🇪 +971 (UAE)</option>
                    <option value="+966" data-country="SA">🇸🇦 +966 (Saudi Arabia)</option>
                    <option value="+974" data-country="QA">🇶🇦 +974 (Qatar)</option>
                    <option value="+965" data-country="KW">🇰🇼 +965 (Kuwait)</option>
                    <option value="+973" data-country="BH">🇧🇭 +973 (Bahrain)</option>
                    <option value="+968" data-country="OM">🇴🇲 +968 (Oman)</option>
                    <option value="+60" data-country="MY">🇲🇾 +60 (Malaysia)</option>
                    <option value="+65" data-country="SG">🇸🇬 +65 (Singapore)</option>
                    <option value="+66" data-country="TH">🇹🇭 +66 (Thailand)</option>
                    <option value="+62" data-country="ID">🇮🇩 +62 (Indonesia)</option>
                    <option value="+63" data-country="PH">🇵🇭 +63 (Philippines)</option>
                    <option value="+84" data-country="VN">🇻🇳 +84 (Vietnam)</option>
                    <option value="+852" data-country="HK">🇭🇰 +852 (Hong Kong)</option>
                    <option value="+853" data-country="MO">🇲🇴 +853 (Macau)</option>
                    <option value="+886" data-country="TW">🇹🇼 +886 (Taiwan)</option>
                    <option value="+64" data-country="NZ">🇳🇿 +64 (New Zealand)</option>
                    <option value="+27" data-country="ZA">🇿🇦 +27 (South Africa)</option>
                    <option value="+20" data-country="EG">🇪🇬 +20 (Egypt)</option>
                    <option value="+234" data-country="NG">🇳🇬 +234 (Nigeria)</option>
                    <option value="+254" data-country="KE">🇰🇪 +254 (Kenya)</option>
                    <option value="+55" data-country="BR">🇧🇷 +55 (Brazil)</option>
                    <option value="+52" data-country="MX">🇲🇽 +52 (Mexico)</option>
                    <option value="+54" data-country="AR">🇦🇷 +54 (Argentina)</option>
                    <option value="+56" data-country="CL">🇨🇱 +56 (Chile)</option>
                    <option value="+57" data-country="CO">🇨🇴 +57 (Colombia)</option>
                    <option value="+51" data-country="PE">🇵🇪 +51 (Peru)</option>
                    <option value="+90" data-country="TR">🇹🇷 +90 (Turkey)</option>
                    <option value="+972" data-country="IL">🇮🇱 +972 (Israel)</option>
                    <option value="+961" data-country="LB">🇱🇧 +961 (Lebanon)</option>
                    <option value="+962" data-country="JO">🇯🇴 +962 (Jordan)</option>
                    <option value="+20" data-country="EG">🇪🇬 +20 (Egypt)</option>
                  </select>
                  <div class="booking-input-with-icon booking-phone-input">
                    <i class="fab fa-whatsapp" style="color: #25D366;"></i>
                    <input type="tel" id="phone" name="phone" placeholder="1234567890" required>
                  </div>
                </div>
                <small style="display: block; margin-top: 6px; color: #666; font-size: 12px; font-style: italic;">
                  Select your country code and enter your phone number
                </small>
              </div>
            </div>

            <!-- Session Type Selection -->
            <div class="booking-form-group">
              <label>Session Type <span class="required">*</span></label>
              <div class="booking-session-type">
                <div class="booking-session-option">
                  <input type="radio" id="session-one" name="sessionType" value="One to One" required>
                  <label for="session-one" class="booking-session-label">
                    <i class="fas fa-user"></i>
                    <span>One to One</span>
                  </label>
                </div>
                <div class="booking-session-option">
                  <input type="radio" id="session-group" name="sessionType" value="Group Session" required>
                  <label for="session-group" class="booking-session-label">
                    <i class="fas fa-users"></i>
                    <span>Group Session</span>
                  </label>
                </div>
              </div>
            </div>

            <!-- Preferred Date with Calendar Icon -->
            <div class="booking-form-group">
              <label for="preferredDate">Preferred Date <span class="required">*</span></label>
              <div class="booking-date-input-wrapper">
                <input type="date" id="preferredDate" name="preferredDate" required>
                <i class="far fa-calendar-alt"></i>
              </div>
            </div>

            <!-- Medical Condition / Specific Needs Textarea -->
            <div class="booking-form-group">
              <label for="medicalCondition">Medical Condition / Specific Needs <span class="required">*</span></label>
              <textarea 
                id="medicalCondition" 
                name="medicalCondition" 
                placeholder="Please share any medical conditions, allergies, injuries, or specific needs we should be aware of to ensure your safe and comfortable experience..."
                required
              ></textarea>
            </div>

            <!-- Form Note -->
            <div class="booking-form-note">
              <strong>Important Note:</strong> Your information is confidential and will be used solely to personalize your healing experience. We will contact you within 24 hours to confirm your booking and discuss any additional details.
            </div>

            <!-- Submit Button -->
            <button type="submit" class="booking-submit-btn">
              <span class="btn-text">
                <i class="fas fa-check-circle" style="margin-right: 8px;"></i>
                Confirm Booking
              </span>
            </button>
          </form>

          <!-- Loading State -->
          <div class="booking-loading" id="bookingLoading">
            <div class="booking-spinner"></div>
            <p>Processing your booking request...</p>
          </div>

          <!-- Success State -->
          <div class="booking-success" id="bookingSuccess">
            <div class="booking-success-icon">
              <i class="fas fa-check-circle"></i>
            </div>
            <h3>You Have Successfully Booked!</h3>
            <p><strong>Congratulations!</strong> Your booking has been confirmed. Thank you for choosing us for your healing journey.</p>
            <p style="margin-top: 16px; font-size: 14px; color: #666;">We've received your booking request and will contact you within 24 hours to confirm your session and answer any questions you may have.</p>
            <button type="button" class="booking-submit-btn" onclick="closeBookingModal()" style="margin-top: 24px; max-width: 300px;">
              <span class="btn-text">Close</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  `;

  // Add modal to body if it doesn't exist
  if (!document.getElementById('bookingModal')) {
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    setupBookingForm();
  }
}

// Setup form event listeners and functionality
function setupBookingForm() {
  const form = document.getElementById('bookingForm');
  const modal = document.getElementById('bookingModal');
  
  if (form) {
    // Remove existing submit listeners to prevent duplicates
    const newForm = form.cloneNode(true);
    form.parentNode.replaceChild(newForm, form);
    
    // Get the fresh form reference
    const freshForm = document.getElementById('bookingForm');
    
    // Ensure form doesn't submit normally
    freshForm.setAttribute('onsubmit', 'event.preventDefault(); return false;');
    freshForm.setAttribute('action', 'javascript:void(0);');
    freshForm.setAttribute('method', 'post');
    
    // Add submit handler with proper event prevention
    freshForm.addEventListener('submit', function(e) {
      console.log('Form submit event triggered');
      e.preventDefault();
      e.stopPropagation();
      e.stopImmediatePropagation();
      handleBookingSubmit(e);
      return false;
    }, true); // Use capture phase
    
    // Also handle button click as backup
    const submitBtn = freshForm.querySelector('.booking-submit-btn');
    if (submitBtn) {
      submitBtn.addEventListener('click', function(e) {
        // Don't prevent default here, let form submit handler take over
        console.log('Submit button clicked');
      });
    }
    
    // Service type change handler - show/hide course dropdown
    const serviceTypeInputs = freshForm.querySelectorAll('input[name="serviceType"]');
    const courseDropdown = document.getElementById('courseDropdown');
    const courseSelect = document.getElementById('courseSelection');
    
    if (serviceTypeInputs.length > 0 && courseDropdown && courseSelect) {
      serviceTypeInputs.forEach(input => {
        input.addEventListener('change', function() {
          if (this.value === 'Courses & Trainings') {
            courseDropdown.classList.add('show');
            courseSelect.setAttribute('required', 'required');
          } else {
            courseDropdown.classList.remove('show');
            courseSelect.removeAttribute('required');
            courseSelect.value = '';
          }
        });
      });
    }

    // Set minimum date to today
    const dateInput = document.getElementById('preferredDate');
    if (dateInput) {
      const today = new Date();
      const tomorrow = new Date(today);
      tomorrow.setDate(tomorrow.getDate() + 1);
      const minDate = tomorrow.toISOString().split('T')[0];
      dateInput.setAttribute('min', minDate);
    }

    // Phone number formatting with country code selector
    const phoneInput = document.getElementById('phone');
    const countryCodeSelect = document.getElementById('countryCode');
    
    if (phoneInput && countryCodeSelect) {
      // Only allow digits in phone number field
      phoneInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        e.target.value = value;
        
        // Validate phone number length
        if (value.length > 0 && value.length < 7) {
          e.target.setCustomValidity('Please enter a complete phone number (at least 7 digits)');
        } else if (value.length > 15) {
          e.target.setCustomValidity('Phone number is too long (maximum 15 digits)');
        } else {
          e.target.setCustomValidity('');
        }
      });
      
      // Validate on blur
      phoneInput.addEventListener('blur', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length > 0 && value.length < 7) {
          e.target.setCustomValidity('Please enter a complete phone number');
        } else {
          e.target.setCustomValidity('');
        }
      });
      
      // Update placeholder based on selected country (optional enhancement)
      countryCodeSelect.addEventListener('change', function() {
        phoneInput.setCustomValidity('');
        // Focus on phone input after country selection
        phoneInput.focus();
      });
      
      // Set helpful title
      phoneInput.setAttribute('title', 'Enter your phone number without country code (country code is selected above)');
    }

    // Age validation
    const ageInput = document.getElementById('age');
    if (ageInput) {
      ageInput.addEventListener('input', function(e) {
        const age = parseInt(e.target.value);
        if (age < 16) {
          e.target.setCustomValidity('You must be at least 16 years old to book a session.');
        } else if (age > 100) {
          e.target.setCustomValidity('Please enter a valid age.');
        } else {
          e.target.setCustomValidity('');
        }
      });
    }
  }

  // Close modal on Escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && modal && modal.classList.contains('active')) {
      closeBookingModal();
    }
  });
}

// Track if form is currently submitting
let isSubmittingBooking = false;

// Handle form submission
function handleBookingSubmit(e) {
  // Prevent default form submission and page reload
  if (e) {
    e.preventDefault();
    e.stopPropagation();
  }
  
  // Prevent double submission
  if (isSubmittingBooking) {
    console.log('Booking already being submitted, please wait...');
    return false;
  }
  
  const form = document.getElementById('bookingForm');
  if (!form) {
    console.error('Booking form not found!');
    alert('Booking form not found. Please refresh the page.');
    return false;
  }
  
  const loading = document.getElementById('bookingLoading');
  const success = document.getElementById('bookingSuccess');
  const submitBtn = form.querySelector('.booking-submit-btn');
  
  if (!loading || !success || !submitBtn) {
    console.error('Required booking modal elements not found!');
    alert('Booking modal elements not found. Please refresh the page.');
    return false;
  }
  
  // Validate form
  if (!form.checkValidity()) {
    form.reportValidity();
    return false;
  }
  
  // Mark as submitting
  isSubmittingBooking = true;
  
  // Disable submit button
  submitBtn.disabled = true;
  submitBtn.style.opacity = '0.6';
  submitBtn.style.cursor = 'not-allowed';
  
  // Show loading state
  form.style.display = 'none';
  loading.classList.add('active');
  
  // Collect form data
  const formData = new FormData(form);
  const countryCode = formData.get('countryCode') || '+977';
  const phoneNumber = formData.get('phone') || '';
  const fullPhoneNumber = countryCode + phoneNumber;
  
  const bookingData = {
    serviceType: formData.get('serviceType'),
    courseSelection: formData.get('courseSelection') || null,
    fullName: formData.get('fullName'),
    age: formData.get('age'),
    email: formData.get('email'),
    phone: fullPhoneNumber, // Combine country code + phone number
    countryCode: countryCode,
    sessionType: formData.get('sessionType'),
    preferredDate: formData.get('preferredDate'),
    medicalCondition: formData.get('medicalCondition'),
    submittedAt: new Date().toISOString()
  };
  
  console.log('Submitting booking data:', bookingData);
  
  // Submit booking to API
  if (typeof window.apiUtils !== 'undefined' && window.apiUtils.submitBooking) {
    console.log('API utils found, submitting booking...');
    window.apiUtils.submitBooking(bookingData)
      .then(response => {
        console.log('Booking API response:', response);
        
        // Mark that booking was successfully submitted
        bookingJustSubmitted = true;
        isSubmittingBooking = false;
        
        // Hide loading, show success
        loading.classList.remove('active');
        success.classList.add('active');
        form.style.display = 'none';
        
        // Scroll to top of modal
        const modalContainer = document.querySelector('.booking-modal-container');
        if (modalContainer) {
          modalContainer.scrollTop = 0;
        }
        
        // Show success message
        if (window.apiUtils && window.apiUtils.showSuccessMessage) {
          window.apiUtils.showSuccessMessage('You have successfully booked! We will contact you within 24 hours.');
        } else {
          alert('You have successfully booked! We will contact you within 24 hours.');
        }
        
        // Prevent form from being resubmitted
        submitBtn.disabled = true;
        
        console.log('Booking submitted successfully:', response);
        return false;
      })
      .catch(error => {
        // Reset flags on error
        bookingJustSubmitted = false;
        isSubmittingBooking = false;
        
        // Hide loading, show form again
        loading.classList.remove('active');
        form.style.display = 'block';
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';
        submitBtn.style.cursor = 'pointer';
        
        // Show error message
        const errorMessage = error.message || 'An error occurred. Please try again or contact us directly.';
        console.error('Booking submission error:', error);
        console.error('Error details:', {
          message: error.message,
          stack: error.stack,
          name: error.name
        });
        
        if (window.apiUtils && window.apiUtils.showErrorMessage) {
          window.apiUtils.showErrorMessage(errorMessage);
        } else {
          alert('Error: ' + errorMessage);
        }
        return false;
      });
  } else {
    // Reset submitting flag
    isSubmittingBooking = false;
    
    // Fallback if API utils not loaded
    console.error('API utilities not loaded. Please ensure api.js is included before booking-modal.js');
    loading.classList.remove('active');
    form.style.display = 'block';
    submitBtn.disabled = false;
    submitBtn.style.opacity = '1';
    submitBtn.style.cursor = 'pointer';
    alert('API utilities not loaded. Please refresh the page and try again.');
    return false;
  }
  
  return false; // Prevent form submission
}

// Track if booking was just submitted successfully
let bookingJustSubmitted = false;

// Open booking modal
function openBookingModal(serviceType = null) {
  // Note: We allow bookings without authentication (using public endpoint)
  // If you want to require authentication, uncomment the code below:
  /*
  // Check if user is authenticated
  if (typeof window.apiUtils !== 'undefined' && window.apiUtils.isAuthenticated) {
    if (!window.apiUtils.isAuthenticated()) {
      // User not authenticated, show auth modal first
      if (typeof openAuthModal !== 'undefined') {
        openAuthModal('login');
        if (window.apiUtils.showErrorMessage) {
          window.apiUtils.showErrorMessage('Please login to book a service.');
        }
        return;
      }
    }
  }
  */
  
  createBookingModal();
  const modal = document.getElementById('bookingModal');
  const form = document.getElementById('bookingForm');
  const loading = document.getElementById('bookingLoading');
  const success = document.getElementById('bookingSuccess');
  const courseDropdown = document.getElementById('courseDropdown');
  
  if (modal) {
    // If booking was just submitted successfully, don't reset - keep success state
    if (bookingJustSubmitted && success && success.classList.contains('active')) {
      // Just show the modal with success state
      modal.classList.add('active');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      return;
    }
    
    // Reset booking flag
    bookingJustSubmitted = false;
    
    // Reset form if it was previously submitted
    if (form) {
      form.reset();
      form.style.display = 'block';
      
      // Reset course dropdown
      if (courseDropdown) {
        courseDropdown.classList.remove('show');
        const courseSelect = document.getElementById('courseSelection');
        if (courseSelect) {
          courseSelect.removeAttribute('required');
        }
      }
    }
    if (loading) loading.classList.remove('active');
    if (success) success.classList.remove('active');
    
    // Pre-select service type if provided
    if (serviceType) {
      const serviceInput = document.querySelector(`input[value="${serviceType}"]`);
      if (serviceInput) {
        serviceInput.checked = true;
        serviceInput.dispatchEvent(new Event('change'));
      }
    }
    
    // Show modal
    modal.classList.add('active');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    
    // Animate modal entrance with GSAP if available
    if (typeof gsap !== 'undefined') {
      gsap.fromTo('.booking-modal-container', 
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
      
      // Animate form elements
      gsap.fromTo('.booking-form-group',
        {
          opacity: 0,
          y: 20
        },
        {
          opacity: 1,
          y: 0,
          duration: 0.5,
          stagger: 0.1,
          delay: 0.2,
          ease: 'power2.out'
        }
      );
    }
    
    // Focus first input
    const firstInput = modal.querySelector('input[type="radio"], input[type="text"], input[type="email"]');
    if (firstInput) {
      setTimeout(() => {
        if (firstInput.type === 'radio') {
          firstInput.focus();
        } else {
          firstInput.focus();
        }
      }, 400);
    }
  }
}

// Close booking modal
function closeBookingModal() {
  const modal = document.getElementById('bookingModal');
  if (modal) {
    // Reset booking flags when closing
    bookingJustSubmitted = false;
    isSubmittingBooking = false;
    
    // Reset form and states
    const form = document.getElementById('bookingForm');
    const loading = document.getElementById('bookingLoading');
    const success = document.getElementById('bookingSuccess');
    
    if (form) {
      form.reset();
      form.style.display = 'block';
      const submitBtn = form.querySelector('.booking-submit-btn');
      if (submitBtn) submitBtn.disabled = false;
    }
    if (loading) loading.classList.remove('active');
    if (success) success.classList.remove('active');
    
    // Animate modal exit with GSAP if available
    if (typeof gsap !== 'undefined') {
      gsap.to('.booking-modal-container', {
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
window.openBookingModal = openBookingModal;
window.closeBookingModal = closeBookingModal;

// Initialize on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', createBookingModal);
} else {
  createBookingModal();
}
