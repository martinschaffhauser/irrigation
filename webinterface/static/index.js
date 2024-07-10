const API_URL = 'https://irrigation.klbg.link';

document.addEventListener('DOMContentLoaded', () => {
    loadJobs();
    setupCronTypeToggle();
});

function setupCronTypeToggle() {
    const autoCron = document.getElementById('autoCron');
    const manualCron = document.getElementById('manualCron');
    const cronInputs = document.getElementById('cronInputs');
    const manualCronInput = document.getElementById('manualCronInput');

    autoCron.addEventListener('change', () => {
        if (autoCron.checked) {
            cronInputs.style.display = 'block';
            manualCronInput.style.display = 'none';
        }
    });

    manualCron.addEventListener('change', () => {
        if (manualCron.checked) {
            cronInputs.style.display = 'none';
            manualCronInput.style.display = 'block';
        }
    });
}

document.getElementById('jobForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const jobId = document.getElementById('jobId').value;
    const jobDescription = document.getElementById('jobDescription').value;
    const scriptPath = document.getElementById('scriptPath').value;
    const cronType = document.querySelector('input[name="cronType"]:checked').value;

    let cron;
    if (cronType === 'auto') {
        const minutes = document.getElementById('minutes').value;
        const hours = document.getElementById('hours').value;
        const dayOfMonth = document.getElementById('dayOfMonth').value;
        const month = document.getElementById('month').value;
        const dayOfWeek = document.getElementById('dayOfWeek').value;
        cron = `${minutes} ${hours} ${dayOfMonth} ${month} ${dayOfWeek}`;
    } else {
        cron = document.getElementById('cron').value;
    }

    const job = { id: jobId, job_description: jobDescription, script_path: scriptPath, cron: cron };

    const response = await fetch(`${API_URL}/jobs/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(job)
    });

    if (response.ok) {
        alert('Job added successfully');
        loadJobs();
        document.getElementById('jobForm').reset();
    } else {
        alert('Error adding job');
    }
});

async function loadJobs() {
    const response = await fetch(`${API_URL}/jobs/get_db`);
    const data = await response.json();
    const tbody = document.getElementById('jobsTable').querySelector('tbody');
    tbody.innerHTML = '';
    data.jobs.forEach(job => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${job[0]}</td>
            <td>${job[1]}</td>
            <td>${job[2]}</td>
            <td>${job[3]}</td>
            <td><button class="delete-btn" data-job-id="${job[0]}">Delete</button></td>
        `;
        tbody.appendChild(row);
    });
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', () => deleteJob(button.getAttribute('data-job-id')));
    });
}

async function deleteJob(jobId) {
    const response = await fetch(`${API_URL}/jobs/delete/${jobId}`, { method: 'DELETE' });
    if (response.ok) {
        alert('Job deleted successfully');
        loadJobs();
    } else {
        alert('Error deleting job');
    }
}
