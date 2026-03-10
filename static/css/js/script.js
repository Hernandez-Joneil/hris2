document.addEventListener('DOMContentLoaded', function() {
   
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.setAttribute('data-bs-toggle', 'tooltip');
        btn.setAttribute('data-bs-placement', 'top');
        btn.title = btn.textContent.trim();
    });

  
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

 
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

  
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
            let valid = true;
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.style.borderColor = 'red';
                    input.style.animation = 'shake 0.5s';
                    valid = false;
                } else {
                    input.style.borderColor = '#28a745';
                }
            });
            if (!valid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

   
    const style = document.createElement('style');
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
    `;
    document.head.appendChild(style);

 
    const elements = document.querySelectorAll('.container, .table, .alert');
    elements.forEach(el => {
        el.style.opacity = '0';
        setTimeout(() => {
            el.style.transition = 'opacity 0.5s ease';
            el.style.opacity = '1';
        }, 100);
    });
});