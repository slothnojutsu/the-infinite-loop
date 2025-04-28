// Get DOM elements
document.addEventListener('DOMContentLoaded', function() {
    const parkingForm = document.getElementById('parkingForm');
    const submitBtn = document.getElementById('submitBtn');
    const confirmationModal = document.getElementById('confirmationModal');
    const confirmationDetails = document.getElementById('confirmationDetails');
    const confirmBtn = document.getElementById('confirmBtn');
    const editBtn = document.getElementById('editBtn');

    // Handle Submit button click
    submitBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Get form data
        const lpn = document.getElementById('LPN').value;
        const pln = document.getElementById('PLN').value;
        const timeLong = document.getElementById('timeLong').value;
        const appointmentTime = document.getElementById('appt').value;

        // Input validation
        if (!lpn || !pln || !timeLong || !appointmentTime) {
            alert('Please fill in all fields');
            return;
        }

        // Display information in confirmation modal
        confirmationDetails.innerHTML = `
            <div class="confirmation-item">
                <strong>License Plate Number:</strong> ${lpn}
            </div>
            <div class="confirmation-item">
                <strong>Parking Lot Number:</strong> ${pln}
            </div>
            <div class="confirmation-item">
                <strong>Parking Duration:</strong> ${timeLong}
            </div>
            <div class="confirmation-item">
                <strong>Appointment Time:</strong> ${appointmentTime}
            </div>
        `;

        // Show modal
        confirmationModal.style.display = 'block';
    });

    // Handle Confirm button click
    confirmBtn.addEventListener('click', function() {
        alert('Information confirmed successfully!');
        confirmationModal.style.display = 'none';
        parkingForm.reset(); // Reset form
    });

    // Handle Edit button click
    editBtn.addEventListener('click', function() {
        confirmationModal.style.display = 'none';
    });

    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === confirmationModal) {
            confirmationModal.style.display = 'none';
        }
    });

    // Prevent non-numeric input in number fields
    document.getElementById('LPN').addEventListener('input', function(e) {
        this.value = this.value.replace(/[^0-9]/g, '');
    });

    document.getElementById('PLN').addEventListener('input', function(e) {
        this.value = this.value.replace(/[^0-9]/g, '');
    });
});