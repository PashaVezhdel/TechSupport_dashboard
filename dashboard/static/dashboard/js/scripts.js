let charts = {};
const chartOptions = { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } } } };

function filterTable() {
    let filter = document.getElementById("tableSearch").value.toLowerCase();
    let rows = document.getElementById("ticketsTable").getElementsByTagName("tr");
    for (let row of rows) {
        row.style.display = row.textContent.toLowerCase().includes(filter) ? "" : "none";
    }
}

function initCharts(data) {
    charts.status = new Chart(document.getElementById('statusChart'), { type: 'doughnut', data: { labels: data.status_labels, datasets: [{ data: data.status_data, backgroundColor: ['#28a745', '#ffc107', '#17a2b8', '#6c757d'] }] }, options: { ...chartOptions, cutout: '65%' } });
    charts.priority = new Chart(document.getElementById('priorityChart'), { type: 'bar', data: { labels: data.priority_labels, datasets: [{ label: 'Заявки', data: data.priority_data, backgroundColor: ['#dc3545', '#fd7e14', '#007bff'] }] }, options: { ...chartOptions, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } } } });
    charts.worker = new Chart(document.getElementById('workerChart'), { type: 'bar', data: { labels: data.worker_labels, datasets: [{ label: 'Закрито', data: data.worker_data, backgroundColor: '#6f42c1' }] }, options: { ...chartOptions, indexAxis: 'y', plugins: { legend: { display: false } }, scales: { x: { beginAtZero: true, ticks: { stepSize: 1 } } } } });
    charts.month = new Chart(document.getElementById('monthChart'), { type: 'line', data: { labels: data.month_labels, datasets: [{ label: 'Кількість', data: data.month_data, borderColor: '#007bff', fill: true, tension: 0.4 }] }, options: { ...chartOptions, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } } } });
}

async function updateData() {
    const startDate = document.getElementById('start_date').value;
    const endDate = document.getElementById('end_date').value;
    const response = await fetch(`/api/data/?start_date=${startDate}&end_date=${endDate}`);
    const data = await response.json();
    
    document.getElementById('totalCount').innerText = data.total;
    const tbody = document.getElementById('ticketsTable');
    tbody.innerHTML = data.tickets_list.map(t => `
        <tr>
            <td class="text-muted small">${t.date}</td>
            <td class="fw-bold text-primary">#${t.id}</td>
            <td>${t.name}</td>
            <td class="text-truncate" style="max-width: 400px;">${t.desc}</td>
            <td><span class="badge bg-light text-dark border">${t.priority}</span></td>
            <td><span class="badge bg-secondary" style="font-size: 0.75rem;">${t.status}</span></td>
        </tr>
    `).join('');
    
    filterTable();
    Object.keys(charts).forEach(key => {
        charts[key].data.labels = data[key + '_labels'];
        charts[key].data.datasets[0].data = data[key + '_data'];
        charts[key].update();
    });
}

function setupRefresh() {
    const interval = document.getElementById('refreshInterval').value;
    localStorage.setItem('refreshInterval', interval);
    const badge = document.getElementById('autoRefreshStatus');
    if (window.refreshTimer) clearInterval(window.refreshTimer);
    if (interval > 0) {
        badge.innerText = `Авто: ${interval >= 60 ? (interval/60)+'хв' : interval+'с'}`;
        badge.className = "badge bg-success refresh-badge";
        window.refreshTimer = setInterval(updateData, interval * 1000);
    } else { 
        badge.innerText = "OFF"; 
        badge.className = "badge bg-secondary refresh-badge"; 
    }
}