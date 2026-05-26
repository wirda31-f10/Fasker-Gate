// === Script Khusus untuk Fitur Lamar Beasiswa ===
document.addEventListener('DOMContentLoaded', () => {
    // Navigasi dari asn.html -> lamar_beasiswa.html
    const lamarBtns = document.querySelectorAll('.btn-lamar');
    if (lamarBtns.length > 0) {
        lamarBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const card = e.target.closest('.beasiswa-card');
                const titleHTML = card.querySelector('.beasiswa-title').innerHTML;
                const title = titleHTML.replace('<br>', ' ');
                const logoUrl = card.querySelector('.beasiswa-icon').src;
                
                // Teruskan data beasiswa lewat URL Parameter
                const params = new URLSearchParams();
                params.append('title', title);
                params.append('logo', logoUrl);
                window.location.href = 'lamar_beasiswa.html?' + params.toString();
            });
        });
    }

    // Memuat data di lamar_beasiswa.html
    const lamarTitleEl = document.getElementById('lamar-title');
    const lamarLogoEl = document.getElementById('lamar-logo');
    
    if (lamarTitleEl && lamarLogoEl) {
        const urlParams = new URLSearchParams(window.location.search);
        const title = urlParams.get('title');
        const logo = urlParams.get('logo');
        
        if (title) {
            lamarTitleEl.innerText = title;
        }
        if (logo) {
            lamarLogoEl.src = logo;
        }

        // Auto-populate data ASN dari Profil (localStorage)
        const asnNama = localStorage.getItem('asn_nama') || 'ASN';
        const asnNip = localStorage.getItem('asn_nip') || '-';
        const asnInstansi = localStorage.getItem('asn_instansi') || '-';
        const asnEmail = localStorage.getItem('asn_email') || '-';
        
        const lamarAsnTextEl = document.getElementById('lamar-asn-text');
        if (lamarAsnTextEl) {
            lamarAsnTextEl.innerHTML = `<strong>${asnNama}</strong><br>${asnNip}<br>${asnInstansi}<br>${asnEmail}`;
        }

        // Auto-populate nama dokumen unggahan
        const fileCv = localStorage.getItem('asn_cv') || 'cv.pdf';
        const fileSurat = localStorage.getItem('asn_surat') || 'surat_permohonan.pdf';
        const fileFormulir = localStorage.getItem('asn_formulir') || 'formulir_lamaran.pdf';
        const fileToefl = localStorage.getItem('asn_toefl') || 'toefl.pdf';

        const elCv = document.getElementById('lamar-file-cv');
        const elSurat = document.getElementById('lamar-file-surat');
        const elFormulir = document.getElementById('lamar-file-formulir');
        const elToefl = document.getElementById('lamar-file-toefl');

        if (elCv) elCv.innerText = fileCv;
        if (elSurat) elSurat.innerText = fileSurat;
        if (elFormulir) elFormulir.innerText = fileFormulir;
        if (elToefl) elToefl.innerText = fileToefl;
    }
});

function submitLamaran() {
    // Get the profile name or account name
    const profileNameEl = document.querySelector('.profile-name');
    let accountName = "ASN";
    if (profileNameEl) {
        const textNodes = Array.from(profileNameEl.childNodes).filter(node => node.nodeType === Node.TEXT_NODE);
        if (textNodes.length > 0) {
            accountName = textNodes.map(node => node.textContent.trim()).join(' ').trim();
        } else {
            accountName = profileNameEl.textContent.trim();
        }
    }
    if (!accountName) {
        accountName = "ASN";
    }

    // Save application to localStorage for quota tracking
    const currentNip = localStorage.getItem('asn_nip') || '234567';
    const titleEl = document.getElementById('lamar-title');
    const title = titleEl ? titleEl.innerText.trim() : '';
    if (title) {
        const apps = JSON.parse(localStorage.getItem('scholarship_applications') || '[]');
        const alreadyApplied = apps.some(app => app.nip === currentNip && app.judul === title);
        if (!alreadyApplied) {
            apps.push({
                nip: currentNip,
                nama: accountName,
                judul: title,
                tanggal: new Date().toLocaleDateString()
            });
            localStorage.setItem('scholarship_applications', JSON.stringify(apps));
        }
    }

    // Create modal element if it doesn't exist
    let modalOverlay = document.getElementById('custom-modal-popup');
    if (!modalOverlay) {
        modalOverlay = document.createElement('div');
        modalOverlay.id = 'custom-modal-popup';
        modalOverlay.className = 'custom-modal-overlay';
        modalOverlay.innerHTML = `
            <div class="custom-modal-box">
                <div class="custom-modal-header" id="custom-modal-title"></div>
                <div class="custom-modal-body" id="custom-modal-message"></div>
                <div class="custom-modal-footer">
                    <button class="custom-modal-btn" id="custom-modal-ok-btn">OK</button>
                </div>
            </div>
        `;
        document.body.appendChild(modalOverlay);
    }

    // Set text content
    document.getElementById('custom-modal-title').textContent = `Halo, ${accountName}`;
    document.getElementById('custom-modal-message').textContent = 'Lamaran berhasil dikirim';

    // Show modal with a tiny delay to allow CSS transitions to trigger
    setTimeout(() => {
        modalOverlay.classList.add('active');
    }, 10);

    // Handle OK button click
    const okBtn = document.getElementById('custom-modal-ok-btn');
    okBtn.onclick = () => {
        modalOverlay.classList.remove('active');
        setTimeout(() => {
            window.location.href = 'asn.html';
        }, 300);
    };
}

