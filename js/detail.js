const { createApp, ref, onMounted } = Vue;

createApp({
    setup() {
        const item = ref(null);
        const selectedTab = ref(1);
        const isModalActive = ref(false);
        const isEditMode = ref(false); // Edit Toggle

        onMounted(() => {
            loadDetail();
        });

        function loadDetail() {
            const urlParams = new URLSearchParams(window.location.search);
            const qrId = urlParams.get('id');

            if (qrId) {
                fetch(`/api/cases/${qrId}`)
                    .then(r => {
                         if (!r.ok) throw new Error('Not found');
                         return r.json();
                    })
                    .then(data => {
                         // Map EP Directions into an array for cleaner template rendering
                         data.ep_directions = [
                              { reliability: data.ep1_reliability, cost: data.ep1_cost, applicability: data.ep1_applicability, races: data.ep1_races },
                              { reliability: data.ep2_reliability, cost: data.ep2_cost, applicability: data.ep2_applicability, races: data.ep2_races },
                              { reliability: data.ep3_reliability, cost: data.ep3_cost, applicability: data.ep3_applicability, races: data.ep3_races }
                         ];
                         item.value = data;
                    })
                    .catch(err => {
                         console.error('Error fetching detail:', err);
                         item.value = null;
                    });
            }
        }

        function openModal() {
             isModalActive.value = true;
        }

        function saveChanges() {
             if (!item.value) return;
             
             const payload = {
                  title: item.value.title,
                  qr_status: item.value.qr_status,
                  phenomenon: item.value.phenomenon,
                  action: item.value.action,
                  result: item.value.result,
                  conclusion: item.value.conclusion
             };

             fetch(`/api/cases/${item.value.qr_number}`, {
                  method: 'PUT',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify(payload)
             })
             .then(r => r.json())
             .then(data => {
                  if (data.message) {
                       alert('Updated successfully!');
                       isEditMode.value = false;
                       // Reload to get latest status colors or duration updates
                       loadDetail();
                  } else {
                       alert('Error: ' + JSON.stringify(data));
                  }
             })
             .catch(err => alert('Error updating case: ' + err));
        }

        return {
            item,
            selectedTab,
            isModalActive,
            isEditMode,
            openModal,
            saveChanges
        };
    }
}).mount('#app');
