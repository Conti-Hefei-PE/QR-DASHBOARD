import os

html_path = r"c:\Users\uie51305\OneDrive - Continental AG\Apps\AntiGravity\QR\detail.html"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add missing </div> for detail-grid and missing detail.js script
# Current end:
# 311:          </div>
# 312:       </div>
# 313: <script src="js/i18n.js"></script>

fixed_suffix = """         </div>
      </div>
    </div>
  </div>

  <script src="js/i18n.js"></script>
  <script src="js/detail.js"></script>
</body>
</html>
"""

# I'll just find the last timeline section and replace from there to the end.
timeline_end_marker = 'No history logs available.\n            </div>\n         </div>\n      </div>'
# Wait, let's be more robust.
# I'll replace everything from '<script src="js/i18n.js"></script>' to the end.

pattern = '<script src="js/i18n.js"></script>'
parts = content.split(pattern)
new_content = parts[0] + """    </div>
  </div>

  <script src="js/i18n.js"></script>
  <script src="js/detail.js"></script>
</body>
</html>
"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("detail.html scripts and closing tags restored.")
