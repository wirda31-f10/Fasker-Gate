with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

modal_html = '''
    <!-- DETAIL MODAL OVERLAY -->
    <div id="index-modal" class="custom-modal-overlay">
        <div class="custom-modal-box">
            <div class="custom-modal-header">
                <span style="display:flex; align-items:center; gap:8px;">🔍 Detail Beasiswa</span>
                <button class="custom-modal-close" onclick="closeIndexModal()">×</button>
            </div>
            <div class="custom-modal-body" id="index-modal-body">
                <!-- Filled dynamically -->
            </div>
        </div>
    </div>
'''

if 'id="index-modal"' not in html:
    html = html.replace('</body>', modal_html + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Modal appended to index.html")
