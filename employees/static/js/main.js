document.addEventListener('DOMContentLoaded', function () {
    // Auto-dismiss Django Messages after 4 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            // Using Bootstrap's alert close trigger or simple fade-out
            alert.classList.add('fade');
            setTimeout(() => {
                alert.style.display = 'none';
            }, 150);
        }, 4000);
    });

    // Handle Delete Confirmation Modal Setup
    const deleteModal = document.getElementById('deleteConfirmModal');
    if (deleteModal) {
        deleteModal.addEventListener('show.bs.modal', function (event) {
            // Button that triggered the modal
            const button = event.relatedTarget;
            
            // Extract info from data-bs-* attributes
            const employeeId = button.getAttribute('data-bs-id');
            const employeeName = button.getAttribute('data-bs-name');
            const deleteUrl = button.getAttribute('data-bs-url');
            
            // Update the modal's content
            const modalBody = deleteModal.querySelector('.modal-body #employeeNameSpan');
            const modalForm = deleteModal.querySelector('#deleteConfirmForm');
            
            if (modalBody) {
                modalBody.textContent = employeeName;
            }
            if (modalForm) {
                modalForm.setAttribute('action', deleteUrl);
            }
        });
    }
});
