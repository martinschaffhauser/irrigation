document.addEventListener('DOMContentLoaded', () => {
    const API_URL = window.API_URL;

    loadJobs();
    setupCronTypeToggle();
    populateScriptDropdown();
    populateCronSelectors();
    setupPumpButton();
});

async function populateScriptDropdown() {
    const API_URL = window.API_URL;
    try {
        const response = await fetch(`${API_URL}/mqttscripts`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        const scripts = data.scripts;
        const scriptDropdown = document.getElementById('scriptPath');
        scriptDropdown.innerHTML = '';
        scripts.forEach(script => {
            const option = document.createElement('option');
            option.value = script;
            option.textContent = script.split('/').pop();
            scriptDropdown.appendChild(option);
        });
    } catch (error) {
        console.error('Failed to populate script dropdown:', error);
    }
}

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

function populateCronSelectors() {
    populateSelector('minutes', 0, 59, true);
    populateSelector('hours', 0, 23, true);
    populateSelector('dayOfMonth', 1, 31, true);
    populateSelector('month', 1, 12, true);
    populateSelector('dayOfWeek', 0, 6, true);
}

function populateSelector(id, start, end, includeWildcard) {
    const selector = document.getElementById(id);
    selector.innerHTML = '';

    if (includeWildcard) {
        const wildcardOption = document.createElement('option');
        wildcardOption.value = '*';
        wildcardOption.textContent = '*';
        selector.appendChild(wildcardOption);
    }

    for (let i = start; i <= end; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i;
        selector.appendChild(option);
    }
}

document.getElementById('jobForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const API_URL = window.API_URL;
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

    const totalTime = document.getElementById('totalTime').value;
    const cycleDuration = document.getElementById('cycleDuration').value;
    const pauseDuration = document.getElementById('pauseDuration').value;

    const job = {
        id: jobId,
        job_description: jobDescription,
        script_path: scriptPath,
        cron: cron,
        mqtt_args: {
            total_time: totalTime,
            cycle_duration: cycleDuration,
            pause_duration: pauseDuration
        }
    };

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
    const API_URL = window.API_URL;
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
            <td>${job[4]}</td>
            <td><button class="delete-btn" data-job-id="${job[0]}">Delete</button></td>
        `;
        tbody.appendChild(row);
    });
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', () => deleteJob(button.getAttribute('data-job-id')));
    });
}

async function deleteJob(jobId) {
    const API_URL = window.API_URL;
    const response = await fetch(`${API_URL}/jobs/delete/${jobId}`, { method: 'DELETE' });
    if (response.ok) {
        alert('Job deleted successfully');
        loadJobs();
    } else {
        alert('Error deleting job');
    }
}

function setupPumpButton() {
    const API_URL = window.API_URL;
    const pumpButton = document.getElementById('turnPumpOnButton');
    pumpButton.addEventListener('click', async () => {
        const duration = document.getElementById('pumpDuration').value;
        const job = {
            script_path: 'api/operations/mqtt_scripts/pump_on_set_time.py',
            mqtt_args: {
                total_time: parseInt(duration),
            }
        };

        try {
            const response = await fetch(`${API_URL}/jobs/run`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(job)
            });

            if (response.ok) {
                alert('Pump turned on successfully');
            } else {
                alert('Error turning on pump');
            }
        } catch (error) {
            console.error('Failed to turn on pump:', error);
            alert('Error turning on pump');
        }
    });
}
