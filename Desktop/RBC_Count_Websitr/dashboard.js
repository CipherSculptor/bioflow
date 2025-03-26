document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('evaluationForm');
    const profileButton = document.getElementById('profileButton');
    const profileDropdown = document.getElementById('profileDropdown');
    
    // Toggle profile dropdown
    profileButton.addEventListener('click', (e) => {
        e.stopPropagation();
        profileDropdown.classList.toggle('show');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!profileButton.contains(e.target)) {
            profileDropdown.classList.remove('show');
        }
    });
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        try {
            // Get form elements by ID
            const nameInput = document.getElementById('userName');
            const ageInput = document.getElementById('userAge');
            const genderSelect = document.getElementById('userGender');
            const bloodGroupSelect = document.getElementById('userBloodGroup');
            const permittivityInput = document.getElementById('userPermittivity');
            
            console.log('Form elements:', {
                nameInput: nameInput ? nameInput.value : 'not found',
                ageInput: ageInput ? ageInput.value : 'not found',
                genderSelect: genderSelect ? genderSelect.value : 'not found',
                bloodGroupSelect: bloodGroupSelect ? bloodGroupSelect.value : 'not found',
                permittivityInput: permittivityInput ? permittivityInput.value : 'not found'
            });
            
            // Validate blood group
            if (!bloodGroupSelect || !bloodGroupSelect.value) {
                throw new Error('Blood group is required');
            }
            
            // Create the form data object with selected values
            const formData = {
                name: nameInput ? nameInput.value : '',
                age: ageInput ? ageInput.value : '',
                gender: genderSelect ? genderSelect.value : '',
                bloodGroup: bloodGroupSelect.value,
                permittivity: permittivityInput ? permittivityInput.value : ''
            };
            
            console.log('Form data being sent:', formData);
            
            // Show loading state
            const submitBtn = form.querySelector('.evaluate-btn');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing...';
            
            // Send data to API
            console.log('Sending request to API...');
            try {
                // First try to access the test endpoint to check connectivity
                const testResponse = await fetch('http://localhost:5070/test');
                console.log('Test endpoint response:', testResponse.status);
                
                // Now send the actual prediction request
                const response = await fetch('http://localhost:5070/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                console.log('API response status:', response.status);
                
                const responseData = await response.json();
                console.log('API response data:', responseData);
                
                if (!response.ok) {
                    throw new Error(responseData.error || 'Failed to get prediction');
                }
                
                // Store both form data and results
                localStorage.setItem('userDetails', JSON.stringify({
                    ...formData,
                    results: responseData
                }));
                
                console.log('Redirecting to results page...');
                // Redirect to results page
                window.location.href = 'results.html';
            } catch (networkError) {
                console.error('Network error details:', networkError);
                alert(`Failed to connect to the API server at http://localhost:5070. Please make sure the server is running.\n\nError: ${networkError.message}`);
                
                // Restore button state
                const submitBtn = form.querySelector('.evaluate-btn');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Evaluate';
            }
        } catch (error) {
            console.error('Error details:', error);
            alert(`An error occurred: ${error.message}`);
            
            // Restore button state
            const submitBtn = form.querySelector('.evaluate-btn');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Evaluate';
        }
    });
}); 