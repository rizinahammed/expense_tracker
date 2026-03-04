document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    const toggleButton = document.querySelector('.sidebar-toggle');

    const toggleSidebar = () => {
        if (!sidebar || !overlay) return;
        sidebar.classList.toggle('show');
        overlay.classList.toggle('show');
    };

    if (toggleButton) {
        toggleButton.addEventListener('click', toggleSidebar);
    }

    if (overlay) {
        overlay.addEventListener('click', toggleSidebar);
    }

    document.querySelectorAll('.sidebar a').forEach((link) => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768 && sidebar?.classList.contains('show')) {
                toggleSidebar();
            }
        });
    });
});