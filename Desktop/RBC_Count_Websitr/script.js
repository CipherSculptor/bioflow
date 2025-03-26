document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        // Here you would typically validate credentials with your backend
        console.log('Login attempt:', { email, password });
        
        // For demo purposes, redirect to dashboard
        window.location.href = 'dashboard.html';
    });

    // Handle social login buttons
    const googleBtn = document.querySelector('.google-btn');
    const facebookBtn = document.querySelector('.facebook-btn');

    if (googleBtn) {
        googleBtn.addEventListener('click', () => {
            // Implement Google OAuth login
            console.log('Google login clicked');
            window.location.href = 'dashboard.html';
        });
    }

    if (facebookBtn) {
        facebookBtn.addEventListener('click', () => {
            // Implement Facebook OAuth login
            console.log('Facebook login clicked');
            window.location.href = 'dashboard.html';
        });
    }
}); 