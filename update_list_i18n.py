import os
import re

html_path = r"c:\Users\uie51305\OneDrive - Continental AG\Apps\AntiGravity\QR\list.html"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix keys to match i18n.js (camelCase)
replacements = {
    "t('qr_management')": "t('qrManagement')",
    "t('dashboard')": "t('dashboard')",
    "t('qr_list')": "t('qrList')",
    "t('add_case')": "t('addCase')",
    "t('trigger_area')": "t('triggerArea')",
    "t('qr_owner')": "t('owner')",
    "t('all_status')": "t('allStatus')",
    "t('all_areas')": "t('allAreas')",
    "t('all_scopes')": "t('allScopes')",
    "t('all_owners')": "t('allOwners')",
    "t('qr_number')": "t('qrNumber')",
    "t('scope')": "t('scope')",
    "t('title')": "t('title')",
    "t('failure_code')": "t('failureCode')",
    "t('trigger_date')": "t('triggerDate')",
    "t('search')": "t('search')",
}

for old, new in replacements.items():
    content = content.replace(old, new)

# Fix common text that missed t()
content = content.replace('<th>Actions</th>', '<th>{{ t("action") }}</th>')
content = content.replace('<th>Status</th>', '<th>{{ t("qrStatus") }}</th>')
content = content.replace('Summary', '{{ t("summary") }}') # if applicable
content = content.replace('Submit', '{{ t("submit") }}')
content = content.replace('Cancel', '{{ t("cancel") }}')
content = content.replace('Previous', '{{ t("prev") }}')
content = content.replace('Next', '{{ t("next") }}')

# Fix complex strings
content = content.replace('Showing {{ paginationStart }} to {{ paginationEnd }} of {{ filteredData.length }} entries', 
                          '{{ t("showing") }} {{ paginationStart }} {{ t("to") }} {{ paginationEnd }} {{ t("of") }} {{ filteredData.length }} {{ t("entries") }}')

# Fix placeholders
content = content.replace('placeholder="{{ t(\'search\') }}..."', 'placeholder="{{ t(\'searchPlaceholder\') }}"')
content = content.replace('placeholder="Description of issue"', ':placeholder="t(\'title\')"')
content = content.replace('placeholder="e.g. FC01"', ':placeholder="t(\'failureCode\')"')
content = content.replace('placeholder="Name"', ':placeholder="t(\'owner\')"')

# Fix channel labels
content = content.replace('Present Cannel', '{{ t("presentCannel") }}')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("list.html i18n updated.")
