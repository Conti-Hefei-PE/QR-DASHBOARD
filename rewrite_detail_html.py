import os
import re

html_path = r"c:\Users\uie51305\OneDrive - Continental AG\Apps\AntiGravity\QR\detail.html"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Edit button logic: Only show when item.qr_status === 'Ongoing'
edit_btn_pattern = r'<button v-if="item" class="btn" @click="toggleEdit">[\s\S]*?</button>'
new_edit_btn = """<button v-if="item && item.qr_status === 'Ongoing'" class="btn" @click="toggleEdit">
             {{ isEditMode ? 'Cancel Edit' : 'Edit' }}
          </button>"""
content = re.sub(edit_btn_pattern, new_edit_btn, content)

# 2. Reorder Basic Information
basic_info_pattern = r'<!-- Basic Info -->[\s\S]*?<!-- Phenomenon -->'
new_basic_info = """<!-- Basic Info -->
         <div class="detail-section">
            <div class="detail-title">Basic Information 基本信息</div>
            
            <div class="detail-row">
               <span class="detail-label">Title</span>
               <div class="detail-value">
                  <input v-if="isEditMode" type="text" v-model="item.title" class="form-input">
                  <span v-else>{{ item.title }}</span>
               </div>
            </div>
            
            <div class="detail-row"><span class="detail-label">QR Number</span><span class="detail-value">#{{ item.qr_number }}</span></div>
            
            <div class="detail-row">
               <span class="detail-label">QR Status</span>
               <div class="detail-value">
                  <select v-if="isEditMode" v-model="item.qr_status" class="form-input">
                     <option value="Ongoing">Ongoing</option>
                     <option value="Completed">Completed</option>
                     <option value="Failed">Failed</option>
                  </select>
                  <span v-else class="badge" :class="item.qr_status === 'Completed' ? 'badge-completed' : (item.qr_status === 'Ongoing' ? 'badge-ongoing' : 'badge-failed')">{{ item.qr_status }}</span>
               </div>
            </div>

            <div class="detail-row">
               <span class="detail-label">Failure Code</span>
               <div class="detail-value">
                  <input v-if="isEditMode" type="text" v-model="item.failure_code" class="form-input">
                  <span v-else>{{ item.failure_code || 'N/A' }}</span>
               </div>
            </div>

            <div class="detail-row">
               <span class="detail-label">Scope</span>
               <div class="detail-value">
                  <select v-if="isEditMode" v-model="item.scope" class="form-input">
                     <option value="Article">Article</option>
                     <option value="General">General</option>
                     <option value="Compound">Compound</option>
                     <option value="Management">Management</option>
                  </select>
                  <span v-else>{{ item.scope || 'N/A' }}</span>
               </div>
            </div>
            
            <div class="detail-row">
               <span class="detail-label">Trigger Area</span>
               <div class="detail-value">
                  <select v-if="isEditMode" v-model="item.trigger_area" class="form-input">
                     <option value="Mix">Mix</option>
                     <option value="HP">HP</option>
                     <option value="CPTB">CPTB</option>
                     <option value="CUFF">CUFF</option>
                     <option value="Phase IV">Phase IV</option>
                  </select>
                  <span v-else>{{ item.trigger_area || 'N/A' }}</span>
               </div>
            </div>

            <div class="detail-row">
               <span class="detail-label">Trigger Date</span>
               <div class="detail-value">
                  <input v-if="isEditMode" type="date" v-model="item.trigger_date" class="form-input">
                  <span v-else>{{ item.trigger_date || 'N/A' }}</span>
               </div>
            </div>

            <div class="detail-row">
               <span class="detail-label">QR Owner</span>
               <div class="detail-value">
                  <input v-if="isEditMode" type="text" v-model="item.qr_owner" class="form-input">
                  <span v-else>{{ item.qr_owner || 'N/A' }}</span>
               </div>
            </div>
            
            <div class="detail-row">
               <span class="detail-label">Problem Severity</span>
               <div class="detail-value">
                  <input v-if="isEditMode" type="text" v-model="item.problem_severity" class="form-input">
                  <span v-else>{{ item.problem_severity || 'N/A' }}</span>
               </div>
            </div>

            <div class="detail-row">
               <span class="detail-label">Target</span>
               <div class="detail-value">
                  <input v-if="isEditMode" type="text" v-model="item.target" class="form-input">
                  <span v-else>{{ item.target || 'N/A' }}</span>
               </div>
            </div>

            <div class="detail-row">
               <span class="detail-label">Close Date</span>
               <div class="detail-value">
                  <input v-if="isEditMode" type="date" v-model="item.close_date" class="form-input">
                  <span v-else>{{ item.close_date || 'N/A' }}</span>
               </div>
            </div>
         </div>

         <!-- Phenomenon -->"""
content = re.sub(basic_info_pattern, new_basic_info, content)

# 3. Phenomenon -> No textarea, drag/drop + image link only
phenomenon_pattern = r'<!-- Phenomenon -->[\s\S]*?<!-- Measures -->'
new_phenomenon = """<!-- Phenomenon -->
         <div class="detail-section">
            <div class="detail-title">Problem Phenomenon 问题现象</div>
            
            <div v-if="isEditMode" 
                 @drop.prevent="handleDrop" 
                 @dragover.prevent="handleDragOver"
                 @dragleave.prevent="handleDragLeave"
                 :class="['upload-zone', { 'drag-over': isDragging }]"
                 style="border: 2px dashed #ced4da; border-radius: 8px; padding: 2rem; text-align: center; margin-bottom: 1rem; cursor: pointer; transition: all 0.2s; background: #f8f9fa;">
               
               <input type="file" @change="uploadImage" style="display:none;" accept="image/*" id="phenomInput">
               <label for="phenomInput" style="cursor:pointer; display:block; width:100%; height:100%;">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--primary-color)" stroke-width="2" style="margin-bottom:0.5rem;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                  <p style="margin:0; color:#495057; font-weight:500;">Click or Drag & Drop image here to upload</p>
               </label>
            </div>
            
            <div v-if="item.phenomenon_image" style="margin-bottom: 1rem;">
               <img :src="item.phenomenon_image" class="phenom-image" @click="openModal" alt="Phenomenon Evidence" style="max-width:100%; max-height:400px; border:1px solid #dee2e6; border-radius:4px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); cursor: zoom-in;">
            </div>
            <div v-else-if="!isEditMode && !item.phenomenon_image" style="color: #6c757d; font-style: italic; padding: 1rem; background: #f8f9fa; border-radius: 4px;">
               No picture uploaded.
            </div>
         </div>

         <!-- Measures -->"""
content = re.sub(phenomenon_pattern, new_phenomenon, content)


# 4. Measures (Good Lead & Evidence addition)
measures_pattern = r'<!-- Measures -->[\s\S]*?</div>\s*</div>\s*<!-- Right Column: Timeline & EP Directions -->'
new_measures = """<!-- Measures -->
         <div class="detail-section">
            <div class="detail-title">Measures & Result 措施与结果</div>
            <div class="detail-row" style="flex-direction:column; gap:0.25rem; margin-bottom: 1rem;">
               <span class="detail-label" style="flex: none; margin-bottom: 0.25rem;">Action 措施</span>
               <textarea v-if="isEditMode" v-model="item.action" class="form-input" style="height: 120px;"></textarea>
               <div v-else class="detail-value" style="white-space: pre-line; background: #f8f9fa; padding: 0.75rem; border-radius: 4px;">{{ item.action || 'N/A' }}</div>
            </div>
            <div class="detail-row" style="flex-direction:column; gap:0.25rem; margin-bottom: 1rem;">
               <span class="detail-label" style="flex: none; margin-bottom: 0.25rem;">Result 结果</span>
               <textarea v-if="isEditMode" v-model="item.result" class="form-input" style="height: 120px;"></textarea>
               <div v-else class="detail-value" style="white-space: pre-line; background: #f8f9fa; padding: 0.75rem; border-radius: 4px;">{{ item.result || 'N/A' }}</div>
            </div>

            <!-- Newly requested sections -->
            <div class="detail-row" style="flex-direction:column; gap:0.25rem; margin-bottom: 1rem;">
               <span class="detail-label" style="flex: none; margin-bottom: 0.25rem;">Good Lead</span>
               <textarea v-if="isEditMode" v-model="item.good_lead" class="form-input" style="height: 120px;"></textarea>
               <div v-else class="detail-value" style="white-space: pre-line; background: #f8f9fa; padding: 0.75rem; border-radius: 4px;">{{ item.good_lead || 'N/A' }}</div>
            </div>
            <div class="detail-row" style="flex-direction:column; gap:0.25rem; margin-bottom: 1rem;">
               <span class="detail-label" style="flex: none; margin-bottom: 0.25rem;">Evidence</span>
               <textarea v-if="isEditMode" v-model="item.evidence" class="form-input" style="height: 120px;"></textarea>
               <div v-else class="detail-value" style="white-space: pre-line; background: #f8f9fa; padding: 0.75rem; border-radius: 4px;">{{ item.evidence || 'N/A' }}</div>
            </div>

            <div class="detail-row" style="flex-direction:column; gap:0.25rem;">
               <span class="detail-label" style="flex: none; margin-bottom: 0.25rem;">Conclusion 结论</span>
               <textarea v-if="isEditMode" v-model="item.conclusion" class="form-input" style="height: 120px;"></textarea>
               <div v-else class="detail-value" style="white-space: pre-line; background: #f8f9fa; padding: 0.75rem; border-radius: 4px;">{{ item.conclusion || 'N/A' }}</div>
            </div>
         </div>
      </div>

      <!-- Right Column: Timeline & EP Directions -->"""
content = re.sub(measures_pattern, new_measures, content)

# 5. Right column EP directions mapping -> Next Step Matrix editor
ep_pattern = r'<!-- EP Directions -->[\s\S]*?</div>\s*</div>\s*<!-- Lightbox Modal -->'
new_ep = """<!-- Next Step Matrix (Formerly EP Directions) -->
         <div class="detail-section">
            <div class="detail-title">Next Step 次步计划</div>
            
            <div class="detail-row" style="flex-direction:column; gap:0.25rem; margin-bottom: 1.5rem;">
               <textarea v-if="isEditMode" v-model="item.next_step" class="form-input" style="height: 80px;" placeholder="Overall Next Step Description..."></textarea>
               <div v-else class="detail-value" style="white-space: pre-line; background: #e9ecef; border-left: 4px solid var(--primary-color); padding: 0.75rem; border-radius: 4px;">{{ item.next_step || 'No overall next step defined.' }}</div>
            </div>

            <div class="tabs-container" style="border: 1px solid #dee2e6; border-radius: 8px; overflow: hidden;">
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

                  <!-- Matrix Grid for the 4 dimensions -->
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
         </div>
      </div>
    </div>

    <!-- Lightbox Modal -->"""
content = re.sub(ep_pattern, new_ep, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("detail.html rewritten successfully.")
