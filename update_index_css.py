import re
import os

css_path = r'css\index.css'
if os.path.exists(css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()

    css_cards = '''
.cards-container {
    display: flex;
    align-items: center;
    gap: 40px;
    overflow-x: auto;
    padding: 10px 10px 30px 10px; /* add padding for hover effect */
    scroll-behavior: smooth;
}
.cards-container::-webkit-scrollbar {
    height: 8px;
}
.cards-container::-webkit-scrollbar-thumb {
    background: #E9B242;
    border-radius: 4px;
}
.cards-container::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
}
'''
    css = re.sub(r'\.cards-container\s*\{[\s\S]*?gap:\s*40px;\n\}', css_cards.strip(), css)

    if 'flex-shrink: 0;' not in css.split('.program-card {')[1].split('}')[0]:
        css = css.replace('.program-card {', '.program-card {\n    flex-shrink: 0;')

    # Add modal CSS
    modal_css = '''
/* ================= MODAL BEASISWA ================= */
.custom-modal-overlay {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.6);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s ease, visibility 0.3s ease;
    padding: 20px;
}
.custom-modal-overlay.active {
    opacity: 1;
    visibility: visible;
}
.custom-modal-box {
    background: #fff;
    border-radius: 12px;
    width: 600px;
    max-width: 95%;
    max-height: 90vh;
    overflow-y: auto;
    position: relative;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    font-family: 'Montserrat', sans-serif;
}
.custom-modal-header {
    background: #FDF5E6;
    padding: 20px 24px;
    border-bottom: 2px solid #E9B242;
    color: #1a365d;
    font-size: 18px;
    font-weight: 700;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.custom-modal-close {
    cursor: pointer;
    background: none;
    border: none;
    font-size: 24px;
    color: #e53935;
    font-weight: bold;
    line-height: 1;
}
.custom-modal-body {
    padding: 24px;
}
.modal-logo {
    width: 80px;
    height: 80px;
    object-fit: contain;
    margin-bottom: 16px;
    mix-blend-mode: multiply;
}
.modal-title {
    font-size: 22px;
    font-weight: 700;
    color: #213566;
    margin-bottom: 12px;
}
.modal-detail-row {
    margin-bottom: 12px;
    font-size: 14px;
    line-height: 1.6;
}
.modal-detail-row strong {
    color: #1a365d;
}
'''
    if 'custom-modal-overlay' not in css:
        css += '\n' + modal_css

    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)

print("CSS updated")
