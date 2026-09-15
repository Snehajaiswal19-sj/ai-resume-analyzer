// Global JavaScript functions
$(document).ready(function() {
    // Add smooth scrolling to all links
    $("a").on('click', function(event) {
        if (this.hash !== "") {
            event.preventDefault();
            const hash = this.hash;
            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 800, function(){
                window.location.hash = hash;
            });
        }
    });

    // Enable tooltips
    $('[data-toggle="tooltip"]').tooltip();

    // Add loading state to any form submit
    $('form').on('submit', function() {
        const submitBtn = $(this).find('button[type="submit"]');
        if (submitBtn.length) {
            submitBtn.prop('disabled', true);
            const originalHtml = submitBtn.html();
            submitBtn.html('<i class="fas fa-spinner fa-spin"></i> Processing...');
            // Reset after 30 seconds if still pending
            setTimeout(function() {
                if (submitBtn.prop('disabled')) {
                    submitBtn.prop('disabled', false);
                    submitBtn.html(originalHtml);
                }
            }, 30000);
        }
    });

    // Add active class to current nav item
    const currentPath = window.location.pathname;
    $('.navbar-nav .nav-link').each(function() {
        if ($(this).attr('href') === currentPath) {
            $(this).addClass('active');
        }
    });
});

// Function to show toast notifications
function showToast(message, type = 'success') {
    const toast = `
        <div class="toast align-items-center text-white bg-${type} border-0 position-fixed bottom-0 end-0 m-3" role="alert">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    $('body').append(toast);
    $('.toast').toast({delay: 3000}).toast('show');
    setTimeout(function() {
        $('.toast').remove();
    }, 3500);
}