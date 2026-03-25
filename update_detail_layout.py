import os
import re

html_path = r"c:\Users\uie51305\OneDrive - Continental AG\Apps\AntiGravity\QR\detail.html"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add i18n.js script tag
content = content.replace('<script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>', 
                          '<script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>\n  <script src="js/i18n.js"></script>')

# 2. Add Language Toggle in header
header_pattern = r'<div style="display: flex; gap: 0.5rem; align-items:center;">'
content = content.replace(header_pattern, header_pattern + '\n          <button class="btn btn-sm" @click="toggleLang" style="margin-right: 1rem;">{{ currentLang === "en" ? "中文" : "English" }}</button>')

# 3. Replace Static Text with t() calls
# Sidebar
content = content.replace('<span>QR Management</span>', '<span>{{ t("qrManagement") }}</span>')
content = content.replace('<span>Dashboard</span>', '<span>{{ t("dashboard") }}</span>')
content = content.replace('<span>QR List</span>', '<span>{{ t("qrList") }}</span>')
content = content.replace('Back to List', '{{ t("backToList") }}')
content = content.replace('QR Detail', '{{ t("qrList") }} #')

# Case Detail #...
content = re.sub(r'{{ isEditMode \? \'Cancel Edit\' : \'Edit\' }}', '{{ isEditMode ? t("cancelEdit") : t("edit") }}', content)
content = content.replace('Save', '{{ t("save") }}')

# Basic Info
content = content.replace('Basic Information 基本信息', '{{ t("basicInfo") }}')
content = content.replace('<span class="detail-label">Title</span>', '<span class="detail-label">{{ t("title") }}</span>')
content = content.replace('<span class="detail-label">QR Number</span>', '<span class="detail-label">{{ t("qrNumber") }}</span>')
content = content.replace('<span class="detail-label">QR Status</span>', '<span class="detail-label">{{ t("qrStatus") }}</span>')
content = content.replace('<span class="detail-label">Failure Code</span>', '<span class="detail-label">{{ t("failureCode") }}</span>')
content = content.replace('<span class="detail-label">Scope</span>', '<span class="detail-label">{{ t("scope") }}</span>')
content = content.replace('<span class="detail-label">Trigger Area</span>', '<span class="detail-label">{{ t("triggerArea") }}</span>')
content = content.replace('<span class="detail-label">Trigger Date</span>', '<span class="detail-label">{{ t("triggerDate") }}</span>')
content = content.replace('<span class="detail-label">QR Owner</span>', '<span class="detail-label">{{ t("owner") }}</span>')
content = content.replace('<span class="detail-label">Problem Severity</span>', '<span class="detail-label">{{ t("problemSeverity") }}</span>')
content = content.replace('<span class="detail-label">Target</span>', '<span class="detail-label">{{ t("target") }}</span>')
content = content.replace('<span class="detail-label">Close Date</span>', '<span class="detail-label">{{ t("closeDate") }}</span>')

# Phenomenon
content = content.replace('Problem Phenomenon 问题现象', '{{ t("phenomenon") }}')
content = content.replace('Click or Drag & Drop image here to upload', '{{ t("uploadHint") }}')
content = content.replace('No picture uploaded.', '{{ t("noPicture") }}')

# Measures
content = content.replace('Measures & Result 措施与结果', '{{ t("measuresResult") }}')
content = content.replace('<span class="detail-label" style="flex: none; margin-bottom: 0.25rem;">Action 措施</span>', 
                          '<span class="detail-label" style="flex: none; margin-bottom: 0.25rem;">{{ t("action") }}</span>')
content = content.replace('<span class="detail-label" style="flex: none; margin-bottom: 0.25rem;">Result 结果</span>', 
                          '<span class="detail-label" style="flex: none; margin-bottom: 0.25rem;">{{ t("result") }}</span>')
content = content.replace('>Good Lead</span>', '>{{ t("goodLead") }}</span>')
content = content.replace('>Evidence</span>', '>{{ t("evidence") }}</span>')
content = content.replace('Conclusion 结论</span>', '{{ t("conclusion") }}</span>')

# Next Step & Timeline (Structural moves)
# Extract Timeline
timeline_pattern = r'(<!-- Timeline -->[\s\S]*?<!-- Dynamic Automated Diffs Logs -->[\s\S]*?</div>\s*</div>)'
timeline_match = re.search(timeline_pattern, content)
if timeline_match:
    timeline_block = timeline_match.group(1)
    # Remove it from current position
    content = content.replace(timeline_block, '')
    
    # Replace labels in timeline block
    timeline_block = timeline_block.replace('Timeline 时间线 (Logs)', '{{ t("timeline") }}')
    timeline_block = timeline_block.replace('Trigger Date:', '{{ t("triggerDate") }}:')
    timeline_block = timeline_block.replace('QR Case Triggered 触发日期', '{{ t("caseTriggered") }}')

# Next Step (Formerly EP)
content = content.replace('Next Step 次步计划', '{{ t("nextStep") }}')

# Move Next Step Description inside sections
next_step_desc_pattern = r'(<div class="detail-row" style="flex-direction:column; gap:0.25rem; margin-bottom: 1.5rem;">\s*<textarea v-if="isEditMode" v-model="item.next_step"[\s\S]*?</div>)'
desc_match = re.search(next_step_desc_pattern, content)
if desc_match:
    desc_block = desc_match.group(1)
    content = content.replace(desc_block, '')
    
    # Add Executor field inside desc_block
    executor_html = """
            <div class="detail-row" style="margin-top: 1rem;">
               <span class="detail-label">{{ t("nextStepExecutor") }}</span>
               <div class="detail-value">
                  <input v-if="isEditMode" type="text" v-model="item.next_step_executor" class="form-input" placeholder="Name">
                  <span v-else>{{ item.next_step_executor || 'N/A' }}</span>
               </div>
            </div>"""
    desc_block += executor_html
    
    # Re-insert desc_block after the matrix tabs container end
    insertion_point = r'</div>\s*</div>\s*</div>\s*</div>\s*<!-- Lightbox Modal -->'
    content = re.sub(r'(</div>\s*</div>\s*</div>\s*</div>)\s*<!-- Lightbox Modal -->', 
                     r'\1\n            ' + desc_block.replace('\\', '\\\\') + r'\n         </div>\s*<!-- Lightbox Modal -->', content)
    # Wait, that regex might be messy. Let's do it simpler.
    
# Actually, the user wants Timeline at BOTTOM RIGHT.
# Let's find the end of the Right Column.
right_column_end = r'<!-- Next Step Matrix \(Formerly EP Directions\) -->[\s\S]*?</div>\s*</div>\s*</div>' # This matches the whole column's second section
# I'll just append timeline_block before the last </div> of the detail-grid.

content = content.replace('Direction {{ n }} Statement', 'Direction {{ n }} Statement') # No change needed but t() could be used
# Next Step Matrix labels
content = content.replace('Reliability', 'Reliability')
content = content.replace('Cost', 'Cost')
content = content.replace('Applicability', 'Applicability')
content = content.replace('RACES', 'RACES')

# Re-insert Timeline at the end of the right column
if timeline_match:
    # Find the closing tag of the second column
    # The grid has two columns. Each is a <div class="column">.
    # I want to append to the end of the second column.
    # The current content has:
    # <div class="column"> (left) ... </div>
    # <div class="column"> (right) ... </div>
    # I'll look for the second column's end.
    
    parts = content.split('<div class="column">')
    if len(parts) >= 3:
        # parts[0] is preamble
        # parts[1] is left column
        # parts[2] is right column
        right_col = parts[2]
        # Find the last </div> that closes the column
        # But wait, there are many internal <div>s.
        # Let's assume the last </div> before <!-- Lightbox Modal --> closes the column if everything is clean.
        
        # Actually, I'll just look for the end of the detail-section in the right column.
        last_section_end = right_col.rfind('</div>') # Last closing div of the column
        # This is risky. Let's use a unique marker.
        
# Re-insertion logic:
# I'll just place the timeline block after the Next Step section.
content = content.replace('<!-- Next Step Matrix (Formerly EP Directions) -->', '<!-- Next Step Matrix -->')
new_right_col_content = """<!-- Next Step Matrix -->
         <div class="detail-section">
            <div class="detail-title">{{ t("nextStep") }}</div>
            
            <div class="tabs-container" style="border: 1px solid #dee2e6; border-radius: 8px; overflow: hidden; margin-bottom: 1rem;">
               <div class="tabs-header" style="background: #f8f9fa; border-bottom: 1px solid #dee2e6;">
                  <button v-for="n in [1,2,3]" :key="'dir-'+n" class="tab-btn" :class="{ active: selectedTab === n }" @click="selectedTab = n" style="padding: 0.75rem 1.25rem; font-weight: 500;">
                     Direction {{ n }}
                  </button>
               </div>
               
               <div v-for="n in [1,2,3]" :key="'content-'+n" class="tab-content" :class="{ active: selectedTab === n }" style="padding: 1rem; background: #fff;">
                  
                  <div style="margin-bottom: 1rem;">
                     <label class="detail-label" style="display:block; margin-bottom: 0.25rem;">Direction {{ n }} Statement</label>
                     <textarea v-if="isEditMode" v-model="item['ep_direction_' + n]" class="form-input" style="height: 60px;"></textarea>
                     <div v-else class="detail-value" style="background:#f1f3f5; padding:0.5rem; border-radius:4px; min-height:40px;">{{ item['ep_direction_' + n] || 'N/A' }}</div>
                  </div>

                  <!-- Matrix Grid -->
                  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                     <div>
                        <span class="detail-label" style="font-size: 0.75rem;">Reliability</span>
                        <input v-if="isEditMode" type="text" v-model="item['ep'+n+'_reliability']" class="form-input" style="padding:0.4rem; font-size:0.875rem;">
                        <div v-else class="detail-value" style="font-weight:600; font-size: 0.875rem; color: var(--primary-color);">{{ item['ep'+n+'_reliability'] || 'N/A' }}</div>
                     </div>
                     <div>
                        <span class="detail-label" style="font-size: 0.75rem;">Cost</span>
                        <input v-if="isEditMode" type="text" v-model="item['ep'+n+'_cost']" class="form-input" style="padding:0.4rem; font-size:0.875rem;">
                        <div v-else class="detail-value" style="font-weight:600; font-size: 0.875rem; color: var(--primary-color);">{{ item['ep'+n+'_cost'] || 'N/A' }}</div>
                     </div>
                     <div>
                        <span class="detail-label" style="font-size: 0.75rem;">Applicability</span>
                        <input v-if="isEditMode" type="text" v-model="item['ep'+n+'_applicability']" class="form-input" style="padding:0.4rem; font-size:0.875rem;">
                        <div v-else class="detail-value" style="font-weight:600; font-size: 0.875rem; color: var(--primary-color);">{{ item['ep'+n+'_applicability'] || 'N/A' }}</div>
                     </div>
                     <div>
                        <span class="detail-label" style="font-size: 0.75rem;">RACES</span>
                        <input v-if="isEditMode" type="text" v-model="item['ep'+n+'_races']" class="form-input" style="padding:0.4rem; font-size:0.875rem;">
                        <div v-else class="detail-value" style="font-weight:600; font-size: 0.875rem; color: var(--primary-color);">{{ item['ep'+n+'_races'] || 'N/A' }}</div>
                     </div>
                  </div>
               </div>
            </div>

            <!-- Next Step Text Description moved here -->
            <div class="detail-row" style="flex-direction:column; gap:0.25rem;">
               <textarea v-if="isEditMode" v-model="item.next_step" class="form-input" style="height: 80px;" placeholder="Overall Next Step Description..."></textarea>
               <div v-else class="detail-value" style="white-space: pre-line; background: #e9ecef; border-left: 4px solid var(--primary-color); padding: 0.75rem; border-radius: 4px;">{{ item.next_step || 'No overall next step defined.' }}</div>
            </div>

            <!-- Next Step Executor -->
            <div class="detail-row" style="margin-top: 1rem;">
               <span class="detail-label">{{ t("nextStepExecutor") }}</span>
               <div class="detail-value">
                  <input v-if="isEditMode" type="text" v-model="item.next_step_executor" class="form-input" placeholder="Name">
                  <span v-else>{{ item.next_step_executor || 'N/A' }}</span>
               </div>
            </div>
         </div>

         <!-- Timeline moved to bottom of right column -->
"""
if timeline_match:
    new_right_col_content += timeline_block

# Replace the entire right column's sections
right_col_pattern = r'<!-- Timeline -->[\s\S]*?<!-- Next Step Matrix \(Formerly EP Directions\) -->[\s\S]*?</div>\s*</div>\s*</div>'
# This is tricky because of the previously partially replaced stuff.
# I'll just replace the whole section from where Timeline started.
content = re.sub(r'<!-- Timeline -->[\s\S]*?<!-- Next Step Matrix \(Formerly EP Directions\) -->[\s\S]*?</div>\s*</div>', 
                 new_right_col_content, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("detail.html layout and i18n updated.")
