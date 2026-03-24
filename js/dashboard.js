const { createApp, ref, onMounted } = Vue;

createApp({
    setup() {
        const updateTime = ref(new Date().toLocaleDateString());
        const kpis = ref({ total: 0, completed: 0, failed: 0, completedRate: '0', failedRate: '0', avgDuration: '0' });
        const recentCases = ref([]);

        onMounted(() => {
            fetch('/api/dashboard')
                .then(response => response.json())
                .then(data => {
                    kpis.value = data.kpis;
                    recentCases.value = data.recentCases;
                    
                    setTimeout(() => {
                        renderCharts(data.areaDistribution, data.scopeDistribution);
                    }, 100);
                })
                .catch(err => console.error('Error fetching dashboard data:', err));
        });

        function renderCharts(areaDist, scopeDist) {
             renderDoughnutChart('chart-area', Object.keys(areaDist), Object.values(areaDist));
             renderBarChart('chart-scope', Object.keys(scopeDist), Object.values(scopeDist), 'QR Counts');
        }

        function renderDoughnutChart(id, labels, dataPoints) {
             const ctx = document.getElementById(id).getContext('2d');
             new Chart(ctx, {
                 type: 'doughnut',
                 data: {
                     labels: labels,
                     datasets: [{
                         data: dataPoints,
                         backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', '#858796']
                     }]
                 },
                 options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } } }
             });
        }

        function renderBarChart(id, labels, dataPoints, labelText) {
             const ctx = document.getElementById(id).getContext('2d');
             new Chart(ctx, {
                 type: 'bar',
                 data: {
                     labels: labels,
                     datasets: [{
                         label: labelText,
                         data: dataPoints,
                         backgroundColor: '#4e73df',
                         borderRadius: 4
                     }]
                 },
                 options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } }
             });
        }

        return {
            updateTime,
            kpis,
            recentCases
        };
    }
}).mount('#app');
