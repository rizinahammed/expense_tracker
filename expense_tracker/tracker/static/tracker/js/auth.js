document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.toggle-password').forEach((toggleButton) => {
        toggleButton.addEventListener('click', () => {
            const targetId = toggleButton.dataset.target;
            const input = document.getElementById(targetId);
            if (!input) return;

            const hidden = input.type === 'password';
            input.type = hidden ? 'text' : 'password';
            toggleButton.textContent = hidden ? '🙈' : '👁';
            toggleButton.setAttribute('aria-label', hidden ? 'Hide password' : 'Show password');
        });
    });
});