document.addEventListener('DOMContentLoaded', () => {
    const minutes = ['*', ...Array.from({ length: 60 }, (_, i) => i)];
    const hours = ['*', ...Array.from({ length: 24 }, (_, i) => i)];
    const days = ['*', ...Array.from({ length: 31 }, (_, i) => i + 1)];
    const months = ['*', ...['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']];
    const daysOfWeek = ['*', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

    function populateSelect(id, options) {
        const select = document.getElementById(id);
        options.forEach(option => {
            const opt = document.createElement('option');
            opt.value = option === '*' ? '*' : options.indexOf(option);
            opt.textContent = option;
            select.appendChild(opt);
        });
    }

    populateSelect('minutes', minutes);
    populateSelect('hours', hours);
    populateSelect('dayOfMonth', days);
    populateSelect('month', months);
    populateSelect('dayOfWeek', daysOfWeek);
});