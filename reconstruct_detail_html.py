import os

html_path = r"c:\Users\uie51305\OneDrive - Continental AG\Apps\AntiGravity\QR\detail.html"

# I'll rewrite the core part of the EP/Timeline section to ensure tag integrity.
# Based on the user's request:
# 1. EP Directions (tabs)
# 2. Next Step Executor & Description (below tabs)
# 3. Timeline (bottom of right column)

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I'll search for the right column start
# <div class="column">
#   <!-- Next Step Matrix -->

new_right_col = """
      <!-- Right Column: Timeline & EP Directions -->
      <div class="column">
         <!-- Next Step Matrix -->
         <div class="detail-section">
            <div class="detail-title">{{ t('nextStep') }}</div>
            
            <div class="tabs-container" style="border: 1px solid #dee2e6; border-radius: 8px; overflow: hidden; margin-bottom: 1rem;">
               <div class="tabs-header" style="background: #f8f9fa; border-bottom: 1px solid #dee2e6;">
                  <button v-for="n in [1,2,3]" :key="'dir-'+n" class="tab-btn" :class="{ active: selectedTab === n }" @click="selectedTab = n" style="padding: 0.75rem 1.25rem; font-weight: 500;">
                     Direction {{ n }}
                  </button>
               </div>
               
               <div v-for="n in [1,2,3]" :key="'content-'+n" class="tab-content" :class="{ active: selectedTab === n }" v-show="selectedTab === n" style="padding: 1rem; background: #fff;">
                  
                  <div style="margin-bottom: 1rem;">
                     <label class="detail-label" style="display:block; margin-bottom: 0.25rem;">{{ t('dirLabel') }} {{ n }}</label>
                     <textarea v-if="isEditMode" v-model="item['ep_direction_' + n]" class="form-input" style="height: 60px;"></textarea>
                     <div v-else class="detail-value" style="background:#f1f3f5; padding:0.5rem; border-radius:4px; min-height:40px;">{{ item['ep_direction_' + n] || 'N/A' }}</div>
                  </div>

                  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                     <div>
                        <label class="detail-label">{{ t('reliability') }} ({{ n }})</label>
                        <select v-if="isEditMode" v-model="item['ep' + n + '_reliability']" class="form-input">
                           <option value="High">High</option><option value="Medium">Medium</option><option value="Low">Low</option>
                        </select>
                        <div v-else class="detail-value">{{ item['ep' + n + '_reliability'] || 'N/A' }}</div>
                     </div>
                     <div>
                        <label class="detail-label">{{ t('cost') }} ({{ n }})</label>
                        <select v-if="isEditMode" v-model="item['ep' + n + '_cost']" class="form-input">
                           <option value="High">High</option><option value="Medium">Medium</option><option value="Low">Low</option>
                        </select>
                        <div v-else class="detail-value">{{ item['ep' + n + '_cost'] || 'N/A' }}</div>
                     </div>
                     <div>
                        <label class="detail-label">{{ t('applicability') }} ({{ n }})</label>
                        <select v-if="isEditMode" v-model="item['ep' + n + '_applicability']" class="form-input">
                           <option value="High">High</option><option value="Medium">Medium</option><option value="Low">Low</option>
                        </select>
                        <div v-else class="detail-value">{{ item['ep' + n + '_applicability'] || 'N/A' }}</div>
                     </div>
                     <div>
                        <label class="detail-label">{{ t('races') }} ({{ n }})</label>
                        <select v-if="isEditMode" v-model="item['ep' + n + '_races']" class="form-input">
                           <option value="High">High</option><option value="Medium">Medium</option><option value="Low">Low</option>
                        </select>
                        <div v-else class="detail-value">{{ item['ep' + n + '_races'] || 'N/A' }}</div>
                     </div>
                  </div>
               </div>
            </div>

            <!-- Next Step Executor & Description (Requested to be below tabs) -->
            <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #dee2e6;">
                <div class="detail-row" style="margin-bottom: 1rem;">
                    <span class="detail-label">{{ t('nextStepExecutor') }}</span>
                    <div class="detail-value">
                        <input v-if="isEditMode" type="text" v-model="item.next_step_executor" class="form-input" style="width: 100%;">
                        <span v-else>{{ item.next_step_executor || 'N/A' }}</span>
                    </div>
                </div>
                <div class="detail-row" style="flex-direction:column; gap:0.25rem;">
                    <span class="detail-label" style="flex:none;">{{ t('nextStep') }} Description</span>
                    <textarea v-if="isEditMode" v-model="item.next_step" class="form-input" style="height: 100px; width:100%;"></textarea>
                    <div v-else class="detail-value" style="background:#f8f9fa; padding:0.75rem; border-radius:4px; min-height:80px; white-space:pre-line;">
                        {{ item.next_step || 'N/A' }}
                    </div>
                </div>
            </div>
         </div>

         <!-- Timeline (Logs) -->
         <div class="detail-section">
            <div class="detail-title">{{ t('timeline') }}</div>
            <div class="timeline" v-if="item.history && item.history.length > 0">
               <div v-for="log in item.history" :key="log.id" class="timeline-item">
                  <div class="timeline-dot"></div>
                  <div class="timeline-header">
                     <span class="timeline-user">{{ log.user }}</span>
                     <span class="timeline-date">{{ log.timestamp }}</span>
                  </div>
                  <div class="timeline-desc">{{ log.description }}</div>
               </div>
            </div>
            <div v-else style="color: #6c757d; font-style: italic; text-align:center; padding: 1rem;">
               No history logs available.
            </div>
         </div>
      </div>
"""

# Extract the body part before the right column
start_tag = '<!-- Right Column: Timeline'
split_parts = content.split(start_tag)
if len(split_parts) < 2:
    # Try another search
    start_tag = '<div class="column">'
    # We want the second one
    parts = content.split(start_tag)
    part0 = parts[0] + start_tag + parts[1] # Keep Left Column
    part2 = new_right_col
    # We need to find the scripts at the end
    script_parts = parts[2].split('<script')
    final_content = part0 + part2 + '<script' + script_parts[1]
else:
    # We need to find the scripts at the end
    script_parts = split_parts[1].split('<script')
    final_content = split_parts[0] + new_right_col + '<script' + script_parts[1]

# Fix back_to_list one last time in the head/body
final_content = final_content.replace('t(\'back_to_list\')', 't(\'backToList\')')
final_content = final_content.replace('t(\'qr_detail\')', 't(\'qrList\')')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(final_content)
print("detail.html reconstructed successfully.")
