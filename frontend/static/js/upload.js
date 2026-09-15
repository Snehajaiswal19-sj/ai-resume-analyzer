$(document).ready(function() {
    const uploadArea = $('#uploadArea');
    const fileInput = $('#fileInput');
    
    // Drag and drop handlers
    uploadArea.on('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).addClass('dragover');
    });
    
    uploadArea.on('dragleave', function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass('dragover');
    });
    
    uploadArea.on('drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass('dragover');
        
        const files = e.originalEvent.dataTransfer.files;
        if (files.length > 0) {
            fileInput[0].files = files;
            displayFileInfo(files[0]);
        }
    });
    
    // File input change handler
    fileInput.on('change', function() {
        if (this.files.length > 0) {
            displayFileInfo(this.files[0]);
        }
    });
    
    // Form submission
    $('#resumeForm').on('submit', function(e) {
        e.preventDefault();
        
        const file = fileInput[0].files[0];
        if (!file) {
            alert('Please select a resume file first!');
            return;
        }
        
        // Show progress
        $('#progress').removeClass('d-none');
        $('#analyzeBtn').prop('disabled', true);
        $('#analyzeBtn').html('<i class="fas fa-spinner fa-spin"></i> Analyzing...');
        
        const formData = new FormData();
        formData.append('resume', file);
        formData.append('job_role', $('#jobRole').val());
        formData.append('user_email', $('#userEmail').val() || 'anonymous');
        
        $.ajax({
            url: '/analyze',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // Store result in session and redirect
                window.location.href = '/result';
            },
            error: function(xhr, status, error) {
                alert('Error analyzing resume: ' + error);
                resetForm();
            }
        });
    });
    
    function displayFileInfo(file) {
        $('#fileInfo').removeClass('d-none');
        $('#fileName').text(file.name + ' (' + formatFileSize(file.size) + ')');
    }
    
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    function resetForm() {
        $('#progress').addClass('d-none');
        $('#analyzeBtn').prop('disabled', false);
        $('#analyzeBtn').html('<i class="fas fa-magic"></i> Analyze Resume');
    }
});

function clearFile() {
    $('#fileInput').val('');
    $('#fileInfo').addClass('d-none');
}