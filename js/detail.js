const { createApp, ref, onMounted } = Vue;

createApp({
    setup() {
        // Global i18n logic from i18n.js
        const { currentLang, t, toggleLang } = getI18nMixin().setup();

        const item = ref(null);
        const selectedTab = ref(1);
        const isModalActive = ref(false);
        const isEditMode = ref(false); 
        const isDragging = ref(false);

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
                         item.value = data;
                    })
                    .catch(err => {
                         console.error('Error fetching detail:', err);
                         item.value = null;
                    });
            }
        }

        function toggleEdit() {
             if (isEditMode.value) {
                  loadDetail();
             }
             isEditMode.value = !isEditMode.value;
        }

        function openModal() {
             isModalActive.value = true;
        }

        function handleDragOver() { isDragging.value = true; }
        function handleDragLeave() { isDragging.value = false; }
        function handleDrop(event) {
             isDragging.value = false;
             if (event.dataTransfer.files && event.dataTransfer.files.length > 0) {
                  uploadFileRaw(event.dataTransfer.files[0]);
             }
        }

        function uploadImage(event) {
             const file = event.target.files[0];
             if (file) uploadFileRaw(file);
        }

        function uploadFileRaw(file) {
             const formData = new FormData();
             formData.append('file', file);

             fetch('/api/upload', {
                  method: 'POST',
                  body: formData
             })
             .then(r => r.json())
             .then(data => {
                  if (data.url) {
                       item.value.phenomenon_image = data.url; 
                       alert('Image uploaded successfully!');
                  } else {
                       alert('Upload error: ' + JSON.stringify(data));
                  }
             })
             .catch(err => alert('Upload exception: ' + err));
        }

        function saveChanges() {
             if (!item.value) return;
             
             const payload = { ...item.value };
             delete payload.history;

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
            currentLang, t, toggleLang,
            isDragging,
            toggleEdit,
            openModal,
            uploadImage,
            handleDragOver,
            handleDragLeave,
            handleDrop,
            saveChanges
        };
    }
}).mount('#app');
