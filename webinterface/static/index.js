const API_URL = 'https://irrigation.klbg.link';

document.getElementById('jobForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const jobId = document.getElementById('jobId').value;
    const scriptPath = document.getElementById('scriptPath').value;
    const cron = document.getElementById('cron').value;
    const job = { id: jobId, script_path: scriptPath, cron: cron };

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

document.addEventListener('DOMContentLoaded', loadJobs);
