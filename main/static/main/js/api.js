/**
 * API Utility Functions for Singing Bowl & Gong House
 * Handles all API communication with Django backend
 * Updated: 2025-12-20 - Using public booking endpoint
 */

// API Base URL
// Use same-origin by default so it works in both dev and production deployments.
const API_BASE_URL = `${window.location.origin}/api`;

/**
 * Get authentication token from localStorage
 */
function getAuthToken() {
    return localStorage.getItem('authToken');
}

/**
 * Save authentication token to localStorage
 */
function saveAuthToken(token) {
    localStorage.setItem('authToken', token);
}

/**
 * Remove authentication token from localStorage
 */
function removeAuthToken() {
    localStorage.removeItem('authToken');
}

/**
 * Check if user is authenticated
 */
function isAuthenticated() {
    return !!getAuthToken();
}

/**
 * Generic API request function
 */
async function apiRequest(endpoint, method = 'GET', data = null, requiresAuth = false) {
    const url = `${API_BASE_URL}${endpoint}`;

    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
    };

    // Add authentication token if required
    if (requiresAuth) {
        const token = getAuthToken();
        if (!token) {
            throw new Error('Authentication required. Please log in.');
        }
        options.headers['Authorization'] = `Token ${token}`;
    }

    // Add request body
    if (data && ['POST', 'PUT', 'PATCH'].includes(method)) {
        options.body = JSON.stringify(data);
    }

    try {
        console.log('Making API request:', { url, method, data, requiresAuth });
        const response = await fetch(url, options);
        
        // Check if response is JSON
        let responseData;
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            responseData = await response.json();
        } else {
            const text = await response.text();
            console.error('Non-JSON response:', text);
            throw new Error(`Server returned non-JSON response: ${response.status} ${response.statusText}`);
        }

        console.log('API Response:', { status: response.status, data: responseData });

        if (!response.ok) {
            const errorMessage =
                responseData.message ||
                responseData.error ||
                (typeof responseData === 'object' ? Object.values(responseData).flat().join(', ') : String(responseData)) ||
                `Server error: ${response.status} ${response.statusText}`;
            console.error('API Error Response:', responseData);
            throw new Error(errorMessage);
        }

        return responseData;
    } catch (error) {
        console.error('API Request Error:', {
            message: error.message,
            url: url,
            method: method,
            error: error
        });
        
        // If it's a network error, provide helpful message
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            throw new Error('Cannot connect to server. Please make sure the Django server is running at ' + API_BASE_URL);
        }
        
        throw error;
    }
}

/**
 * User Registration
 */
async function registerUser(userData) {
    try {
        const response = await apiRequest('/register/', 'POST', userData, false);
        if (response.token) {
            saveAuthToken(response.token);
        }
        return response;
    } catch (error) {
        throw error;
    }
}

/**
 * User Login
 */
async function loginUser(credentials) {
    try {
        const response = await apiRequest('/login/', 'POST', credentials, false);
        if (response.token) {
            saveAuthToken(response.token);
        }
        return response;
    } catch (error) {
        throw error;
    }
}

/**
 * User Logout
 */
function logoutUser() {
    removeAuthToken();
}

/**
 * Verify Email with Token
 */
async function verifyEmail(token) {
    try {
        console.log('Verifying email with token:', token);
        const response = await apiRequest(`/verify-email/${token}/`, 'GET', null, false);
        console.log('Email verification response:', response);
        return response;
    } catch (error) {
        console.error('Email verification error:', error);
        throw error;
    }
}

/**
 * Resend Verification Email
 */
async function resendVerificationEmail() {
    try {
        const response = await apiRequest('/resend-verification/', 'POST', {}, true);
        return response;
    } catch (error) {
        throw error;
    }
}

/**
 * Submit Booking
 */
async function submitBooking(bookingData) {
    try {
        // Map frontend booking data to API format
        // Determine service type based on session type if it's a Sound Healing Session
        let serviceType = mapServiceType(bookingData.serviceType, bookingData.courseSelection);
        
        // If it's a Sound Healing Session, use session type to determine service_type
        if (bookingData.serviceType === 'Sound Healing Session') {
            if (bookingData.sessionType === 'One to One') {
                serviceType = 'personal';
            } else if (bookingData.sessionType === 'Group Session') {
                serviceType = 'group';
            }
        }
        
        const apiData = {
            service_type: serviceType,
            enrollment_date: bookingData.preferredDate,
            full_name: bookingData.fullName,
            email: bookingData.email,
            phone: bookingData.phone,
            age: parseInt(bookingData.age) || null,
            session_type: bookingData.sessionType || null,
            course_selection: bookingData.courseSelection || null,
            medical_condition: bookingData.medicalCondition || null,
        };

        // Use public endpoint (no authentication required)
        // This allows users to book without logging in
        const endpoint = '/bookings/public/';
        const requiresAuth = false;
        
        console.log('Submitting booking to public endpoint:', endpoint);
        console.log('Booking data being sent:', apiData);
        
        try {
            const response = await apiRequest(endpoint, 'POST', apiData, requiresAuth);
            console.log('Booking submission successful:', response);
            return response;
        } catch (error) {
            // If public endpoint fails, log the error
            console.error('Public booking endpoint failed, error:', error);
            console.error('Error details:', {
                message: error.message,
                name: error.name,
                stack: error.stack
            });
            throw error;
        }
    } catch (error) {
        // If error is about authentication, provide helpful message
        if (error.message && error.message.includes('Authentication')) {
            throw new Error('Please login to book a service. Click the Login button in the header.');
        }
        throw error;
    }
}

/**
 * Submit Contact Form/Inquiry
 */
async function submitInquiry(inquiryData) {
    try {
        const apiData = {
            full_name: inquiryData.fullName,
            email: inquiryData.email,
            subject: inquiryData.subject,
            message: inquiryData.message,
        };

        const response = await apiRequest('/contact/', 'POST', apiData, false);
        return response;
    } catch (error) {
        throw error;
    }
}

/**
 * Map frontend service type to API service type
 */
function mapServiceType(serviceType, courseSelection) {
    // Map service types from booking form to API choices
    if (serviceType === 'Courses & Trainings') {
        if (courseSelection) {
            if (courseSelection.includes('Singing Bowl')) {
                return 'singing_bowl';
            } else if (courseSelection.includes('Gong')) {
                return 'gong';
            } else if (courseSelection.includes('Handpan')) {
                return 'handpan';
            }
        }
        return 'singing_bowl'; // Default
    } else if (serviceType === 'Sound Healing Session') {
        // This will be determined by session type
        return 'personal'; // Default, can be changed based on sessionType
    }
    
    // Direct mapping
    const mapping = {
        'Singing Bowl': 'singing_bowl',
        'Gong': 'gong',
        'Handpan': 'handpan',
        'Personal': 'personal',
        'Group': 'group',
        'One to One': 'personal',
        'Group Session': 'group',
    };
    
    return mapping[serviceType] || 'personal';
}

/**
 * Show success message
 */
function showSuccessMessage(message, container = null) {
    const successDiv = document.createElement('div');
    successDiv.className = 'api-success-message';
    successDiv.style.cssText = `
        background: #10b548;
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        margin: 15px 0;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(16, 181, 72, 0.3);
        animation: slideIn 0.3s ease-out;
    `;
    successDiv.textContent = message;
    
    if (container) {
        container.insertBefore(successDiv, container.firstChild);
    } else {
        document.body.appendChild(successDiv);
    }
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        successDiv.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => successDiv.remove(), 300);
    }, 5000);
}

/**
 * Show error message
 */
function showErrorMessage(message, container = null) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'api-error-message';
    errorDiv.style.cssText = `
        background: #e74c3c;
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        margin: 15px 0;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
        animation: slideIn 0.3s ease-out;
    `;
    errorDiv.textContent = message;
    
    if (container) {
        container.insertBefore(errorDiv, container.firstChild);
    } else {
        document.body.appendChild(errorDiv);
    }
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        errorDiv.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => errorDiv.remove(), 300);
    }, 5000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    @keyframes slideOut {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-20px);
        }
    }
`;
document.head.appendChild(style);

// Export functions for use in other scripts
window.apiUtils = {
    registerUser,
    loginUser,
    logoutUser,
    verifyEmail,
    resendVerificationEmail,
    submitBooking,
    submitInquiry,
    isAuthenticated,
    getAuthToken,
    showSuccessMessage,
    showErrorMessage,
};

