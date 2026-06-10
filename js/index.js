// Data Statis Beasiswa
const staticOffers = [
    { judul: "Awards Scholarship Australia", instansi: "Pemerintah Australia", kuota: "50", batas: "30-11-2026", persyaratan: "IPK > 3.0, TOEFL > 500", logo: "https://i.ibb.co.com/zWMtT46F/icon1-removebg-preview.png" },
    { judul: "Leadership Training In Korea", instansi: "KOICA", kuota: "30", batas: "15-12-2026", persyaratan: "IPK > 3.0, TOEFL > 500", logo: "https://i.ibb.co.com/wrM3vmJb/icon2-removebg-preview.png" },
    { judul: "Fullbright Program USA", instansi: "AMINEF", kuota: "40", batas: "20-01-2027", persyaratan: "IPK > 3.2, TOEFL > 550", logo: "https://i.ibb.co.com/C3ynQGLf/icon3-removebg-preview.png" },
    { judul: "JICA Training Program Japan", instansi: "JICA", kuota: "25", batas: "10-02-2027", persyaratan: "IPK > 3.0, TOEFL > 500", logo: "https://i.ibb.co.com/QjdrwZGJ/icon4-removebg-preview.png" }
];

async function getAllOffers() {
    const { data: dynamicOffersList, error } = await window.supabase.from('fasker_scholarships').select('*');
    if (error) console.error("Error fetching scholarships:", error);
    const dynamicOffers = dynamicOffersList || [];
    // Add default logo if missing
    dynamicOffers.forEach(o => {
        if (!o.logo) o.logo = "https://i.ibb.co.com/hJsf9vqP/Logo-Fasker.png";
    });
    const all = [...staticOffers, ...dynamicOffers];
    
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    return all.filter(offer => {
        // Jika beasiswa dari admin (memiliki tahun dan periode)
        if (offer.tahun) {
            const startYear = parseInt(offer.tahun) || 2026;
            const duration = parseInt(offer.periode) || 1;
            const endYear = startYear + duration;
            
            // Logika dari admin.html: Jika endYear <= 2026 berarti 'Selesai' (Tutup)
            return true; // Tampilkan yang 'Berjalan'
        }
        
        // Jika beasiswa bawaan (memiliki batas tanggal spesifik)
        if (offer.batas) {
            return true;
        }
        
        return true;
    });
}

function openIndexModal(offer) {
    const modal = document.getElementById('index-modal');
    const body = document.getElementById('index-modal-body');
    
    if (modal && body) {
        body.innerHTML = `
            <div style="text-align:center;">
                <img src="${offer.logo}" class="modal-logo" alt="Logo">
                <h3 class="modal-title">${offer.judul}</h3>
            </div>
            <div style="margin-top: 20px;">
                <div class="modal-detail-row"><strong>Instansi Penyelenggara:</strong> ${offer.instansi || '-'}</div>
                <div class="modal-detail-row"><strong>Tahun:</strong> ${offer.tahun || '2026'}</div>
                <div class="modal-detail-row"><strong>Kuota:</strong> ${offer.kuota || '-'}</div>
                <div class="modal-detail-row"><strong>Batas Pendaftaran:</strong> ${offer.batas || '-'}</div>
                <div class="modal-detail-row"><strong>Persyaratan:</strong> ${offer.persyaratan || '-'}</div>
                <div class="modal-detail-row">
                    <strong>Dokumen Wajib:</strong><br>
                    <ul style="margin-left: 20px; margin-top: 6px;">
                        <li>Surat Permohonan</li>
                        <li>Formulir Lamaran</li>
                        <li>Curriculum Vitae (CV)</li>
                        <li>Sertifikat TOEFL</li>
                    </ul>
                </div>
            </div>
        `;
        modal.classList.add('active');
    }
}

window.closeIndexModal = function() {
    const modal = document.getElementById('index-modal');
    if (modal) modal.classList.remove('active');
};

document.addEventListener("DOMContentLoaded", async () => {
    // 1. Render Cards Horizontally
    const cardsContainer = document.querySelector('.cards-container');
    if (cardsContainer) {
        const allOffers = await getAllOffers();
        cardsContainer.innerHTML = ''; // clear static
        
        allOffers.forEach(offer => {
            const card = document.createElement('div');
            card.className = 'program-card';
            card.innerHTML = `
                <img src="${offer.logo}" class="card-icon" alt="${offer.judul}">
                <h3>${offer.judul}</h3>
                <button class="btn-detail">Detail</button>
            `;
            
            // Allow clicking anywhere on card or detail button
            card.addEventListener('click', () => {
                openIndexModal(offer);
            });
            
            cardsContainer.appendChild(card);
        });
    }

    // 2. Search Logic
    const searchBtn = document.querySelector(".btn-search");
    const searchInput = document.getElementById("searchInput");

    if (searchBtn && searchInput) {
        const runSearch = async () => {
            const query = searchInput.value.trim().toLowerCase();
            if (query) {
                const allOffers = await getAllOffers();
                const matched = allOffers.find(o => o.judul.toLowerCase().includes(query) || (o.instansi && o.instansi.toLowerCase().includes(query)));
                if (matched) {
                    openIndexModal(matched);
                } else {
                    alert("Program tidak ditemukan untuk: " + query);
                }
            }
        };

        searchBtn.addEventListener("click", runSearch);
        searchInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                runSearch();
            }
        });
    }

    // 3. Dynamic Statistics from Supabase
    const offers = await getAllOffers();
    let openOffers = offers.length; // Hitung semua tawaran yang benar-benar masih buka

    let totalApps = 0;
    let totalVerified = 0;
    let totalPending = 0;

    if (window.supabase) {
        const { data: dbApps, error: appsError } = await window.supabase
            .from('fasker_applications')
            .select('status, scholarship_title');
        
        if (!appsError && dbApps) {
            // Kita hitung aplikasi pendaftaran akun (scholarship_title is null atau kosong)
            const regApps = dbApps.filter(a => !a.scholarship_title);
            totalApps = regApps.length;
            totalVerified = regApps.filter(a => a.status === 'Verified').length;
            totalPending = regApps.filter(a => (a.status || 'Pending') === 'Pending').length;
        }
    }

    if (localStorage.getItem('asn_applications_seeded') !== 'true') {
        totalApps += 12;
        totalVerified += 6;
    }

    const totalRekomendasi = totalVerified + totalPending;

    const statProgram = document.getElementById('stat-program');
    const statPelamar = document.getElementById('stat-pelamar');
    const statRekomendasi = document.getElementById('stat-rekomendasi');
    const statPenerima = document.getElementById('stat-penerima');

    if (statProgram) statProgram.innerText = openOffers;
    if (statPelamar) statPelamar.innerText = totalApps;
    if (statRekomendasi) statRekomendasi.innerText = totalRekomendasi;
    if (statPenerima) statPenerima.innerText = totalVerified;
});