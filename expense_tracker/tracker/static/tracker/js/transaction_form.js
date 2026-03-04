document.addEventListener('DOMContentLoaded', () => {
    const description = document.querySelector('textarea[name="description"], textarea[id^="id_description"]');
    if (!description) {
        return;
    }

    const autoResize = () => {
        description.style.height = 'auto';
        description.style.height = `${description.scrollHeight}px`;
    };

    description.addEventListener('input', autoResize);
    autoResize();
});