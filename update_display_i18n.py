import os
import re

html_path = r"c:\Users\uie51305\OneDrive - Continental AG\Apps\AntiGravity\QR\display.html"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add i18n.js
content = content.replace('<script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>', 
                          '<script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>\n  <script src="js/i18n.js"></script>')

# 2. Add v-if guard and i18n to Header
# Previous:
# <div style="font-weight: bold...
#    <span> _ QR No. {{ item.qr_number }}</span>
# </div>

# Fix: Wrap header content in v-if="item" or just use item?.
# I'll use a wrapper.

navbar_content = """
  <div v-if="item" style="background: #112952; color: #fff; padding: 0.85rem 1.5rem; display: flex; justify-content: space-between; align-items:center; border-bottom: 3px solid #0056b3;">
    <div style="font-weight: bold; font-size: 1.1rem; display:flex; align-items:center; gap:0.4rem; font-family: sans-serif;">
       <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
       <span style="color: #ffd54f;">{{ item.scope || 'N/A' }}</span>
       <span> _ QR No. {{ item.qr_number }}</span>
       <span> _ {{ item.title }}</span>
       <span> _ {{ t('owner') }}_ <span style="color: #81d4fa;">{{ item.qr_owner || 'N/A' }}</span></span>
    </div>
    <div style="display:flex; gap: 1rem; align-items:center;">
        <button class="btn btn-sm" @click="toggleLang">{{ currentLang === "en" ? "中文" : "English" }}</button>
        <a href="list.html" style="color: #fff; text-decoration:none; font-size: 0.875rem; font-weight:600; display:flex; align-items:center; gap:0.25rem;">
           <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
           {{ t('backToList') }}
        </a>
    </div>
  </div>
"""

# Replace the navbar (line 70-82 approx)
navbar_pattern = r'<div style="background: #112952;.*?Back to List.*?</a>.*?</div>'
content = re.sub(navbar_pattern, navbar_content, content, flags=re.DOTALL)

# 3. Localize Card Headers
content = content.replace('Problem Severity', '{{ t("problemSeverity") }}')
content = content.replace('Good Lead', '{{ t("goodLead") }}')
content = content.replace('Action', '{{ t("action") }}')
content = content.replace('Target', '{{ t("target") }}')
content = content.replace('Evidence', '{{ t("evidence") }}')
content = content.replace('Conclusion', '{{ t("conclusion") }}')
content = content.replace('Result', '{{ t("result") }}')
content = content.replace('Piece', '{{ t("phenomenon") }}') # Replace Picture with Phenomenon? 
content = content.replace('Picture', '{{ t("phenomenon") }}')
content = content.replace('QR Result', '{{ t("qrStatus") }}')
content = content.replace('Next Step', '{{ t("nextStep") }}')

# Fix table entries in display
content = content.replace('<td><strong>Trigger Area</strong></td>', '<td><strong>{{ t("triggerArea") }}</strong></td>')
content = content.replace('<td><strong>Scope</strong></td>', '<td><strong>{{ t("scope") }}</strong></td>')
content = content.replace('<td><strong>Owner</strong></td>', '<td><strong>{{ t("owner") }}</strong></td>')

# Fix no picture hint
content = content.replace('No Picture Uploaded', '{{ t("noPicture") }}')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("display.html updated with i18n and v-if.")
