import os
import re

# 1. Update list.html
html_path = r"c:\Users\uie51305\OneDrive - Continental AG\Apps\AntiGravity\QR\list.html"
if os.path.exists(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    form_pattern = r'(<form @submit.prevent="submitNewCase">[\s\S]*?</form>)'
    new_form = """<form @submit.prevent="submitNewCase">
           <div class="form-group">
              <label class="form-label">Title</label>
              <input type="text" v-model="newCase.title" class="form-input" required placeholder="Description of issue">
           </div>
           
           <div class="form-group">
              <label class="form-label">Failure Code</label>
              <input type="text" v-model="newCase.failure_code" class="form-input" placeholder="e.g. FC01">
           </div>

           <div class="form-group">
              <label class="form-label">Scope</label>
              <select v-model="newCase.scope" class="form-input" required>
                 <option disabled value="">Select Scope</option>
                 <option value="Article">Article</option>
                 <option value="General">General</option>
                 <option value="Compound">Compound</option>
                 <option value="Management">Management</option>
              </select>
           </div>

           <div class="form-group">
              <label class="form-label">Trigger Area</label>
              <input type="text" v-model="newCase.trigger_area" class="form-input" required placeholder="e.g. CPTB, HP">
           </div>

           <div class="form-group">
              <label class="form-label">Trigger Date</label>
              <input type="date" v-model="newCase.trigger_date" class="form-input" required>
           </div>

           <div class="form-group">
              <label class="form-label">Owner</label>
              <input type="text" v-model="newCase.qr_owner" class="form-input" required placeholder="Name">
           </div>

           <div class="form-group">
              <label class="form-label">Present Cannel</label>
              <select v-model="newCase.present_cannel" class="form-input" required>
                 <option disabled value="">Select Channel</option>
                 <option value="BT2">BT2</option>
                 <option value="BT3">BT3</option>
              </select>
           </div>

           <div style="display: flex; gap: 0.5rem; margin-top: 1.5rem;">
              <button type="submit" class="btn btn-primary">Submit</button>
              <button type="button" class="btn" @click="isModalOpen = false">Cancel</button>
           </div>
        </form>"""

    html_content_updated = re.sub(form_pattern, new_form, html_content)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content_updated)
    print("list.html updated.")

# 2. Update app.py
app_path = r"c:\Users\uie51305\OneDrive - Continental AG\Apps\AntiGravity\QR\app.py"
if os.path.exists(app_path):
    with open(app_path, 'r', encoding='utf-8') as f:
        app_content = f.read()

    extracted_part_match = re.search(r'# Auto-generate QR Number[\s\S]*?cursor\.execute\(sql, \([^\)]+qr_owner\)\)', app_content)

    if extracted_part_match:
        original_text = extracted_part_match.group(0)
        full_replacement = """# Auto-generate QR Number
        cursor.execute("SELECT MAX(qr_number) as max_num FROM qr_cases")
        max_num = cursor.fetchone()['max_num'] or 0
        new_qr_number = max_num + 1

        title = data.get('title', 'Untitled')
        trigger_area = data.get('trigger_area', '')
        scope = data.get('scope', '')
        qr_owner = data.get('qr_owner', '')
        trigger_date = data.get('trigger_date') 
        qr_status = data.get('qr_status', 'Ongoing')
        failure_code = data.get('failure_code', '')
        present_cannel = data.get('present_cannel', '')

        sql = \"\"\"
        INSERT INTO qr_cases (qr_number, title, qr_status, trigger_area, scope, trigger_date, qr_owner, failure_code, present_cannel)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        \"\"\"
        cursor.execute(sql, (new_qr_number, title, qr_status, trigger_area, scope, trigger_date, qr_owner, failure_code, present_cannel))"""
        
        app_content_updated = app_content.replace(original_text, full_replacement)
        with open(app_path, 'w', encoding='utf-8') as f:
             f.write(app_content_updated)
        print("app.py updated.")
    else:
        print("Anchor match failed on app.py.")
