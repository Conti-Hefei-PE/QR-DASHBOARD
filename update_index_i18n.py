import os
import re

html_path = r"c:\Users\uie51305\OneDrive - Continental AG\Apps\AntiGravity\QR\index.html"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add i18n.js script tag
content = content.replace('<script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>', 
                          '<script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>\n  <script src="js/i18n.js"></script>')

# 2. Add Language Toggle in header
header_pattern = r'<div class="header-actions">'
content = content.replace(header_pattern, 
                          '<div class="header-actions" style="display:flex; align-items:center; gap:1rem;">\n        <button class="btn btn-sm" @click="toggleLang">{{ currentLang === "en" ? "中文" : "English" }}</button>')

# 3. Replace Static Text with t() calls
content = content.replace('<span>QR Management</span>', '<span>{{ t("qrManagement") }}</span>')
content = content.replace('<span>Dashboard</span>', '<span>{{ t("dashboard") }}</span>')
content = content.replace('<span>QR List</span>', '<span>{{ t("qrList") }}</span>')
content = content.replace('<h1 class="content-title">Dashboard</h1>', '<h1 class="content-title">{{ t("dashboard") }}</h1>')

# KPI labels - I'll do this in the kpi-grid
content = content.replace('Total QR Cases', '{{ t("qrNumber") }} (Total)') # Or just 'Total'
content = content.replace('Completed', '{{ t("completed") }}')
content = content.replace('Ongoing', '{{ t("ongoing") }}')
content = content.replace('Failed', '{{ t("failed") }}')
content = content.replace('Avg Duration', 'Avg. Duration') # i18n key could be added later

# Charts
content = content.replace('触发区域分布', '')
content = content.replace('范围分布比例', '')

# Recent Activity
content = content.replace('Recent Triggered QR (Last 10 Cases)', '{{ t("caseTriggered") }} (Last 10)')
content = content.replace('View All →', '{{ t("qrList") }} →')

# Table headers
content = content.replace('<th>Status</th>', '<th>{{ t("qrStatus") }}</th>')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("index.html i18n updated.")
