// Data Statis Beasiswa (fallback jika Supabase kosong)
const staticOffers = [
    { judul: "Awards Scholarship Australia", negara: "Australia", tahun: "2026", kuantitas: "10", persyaratan: "ASN aktif, TOEFL min. 500", logo: "img/Dashboard.png" },
    { judul: "Leadership Training In Korea", negara: "Korea Selatan", tahun: "2026", kuantitas: "5", persyaratan: "ASN aktif, max. 45 tahun", logo: "img/Detail.png" },
    { judul: "Fullbright Program USA", negara: "Amerika Serikat", tahun: "2026", kuantitas: "8", persyaratan: "ASN aktif, TOEFL min. 550", logo: "img/Upload Tawaran.png" },
    { judul: "JICA Training Program Japan", negara: "Jepang", tahun: "2026", kuantitas: "12", persyaratan: "ASN aktif, rekomendasi instansi", logo: "img/Verifikasi (2).png" }
];

async function getAllOffers() {
    if (!window.supabase) return [];
    const { data: dynamicOffersList, error } = await window.supabase.from('fasker_scholarships').select('*');
    if (error) {
        console.error("Error fetching scholarships:", error);
        return [];
    }
    const dynamicOffers = dynamicOffersList || [];
    
    // Add default logo if missing, or map to predefined beautiful icons
    dynamicOffers.forEach(o => {
        if (o.judul === "Awards Scholarship Australia") {
            o.logo = "img/Dashboard.png";
        } else if (o.judul === "Leadership Training In Korea") {
            o.logo = "img/Detail.png";
        } else if (o.judul === "Fullbright Program USA") {
            o.logo = "img/Upload Tawaran.png";
        } else if (o.judul === "JICA Training Program Japan") {
            o.logo = "img/Verifikasi (2).png";
        } else if (!o.logo) {
            o.logo = "img/Logo Fasker .png";
        }
    });
    
    // Jika Supabase tidak mengembalikan data, gunakan data statis
    if (dynamicOffers.length === 0) {
        return staticOffers;
    }

    return dynamicOffers.filter(offer => {
        // Jika beasiswa memiliki tahun dan periode
        if (offer.tahun) {
            const startYear = parseInt(offer.tahun) || 2026;
            const duration = parseInt(offer.periode) || 1;
            const endYear = startYear + duration;
            
            // Tampilkan hanya yang masih aktif (endYear >= tahun sekarang)
            const currentYear = new Date().getFullYear();
            return endYear >= currentYear;
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
                <div class="modal-detail-row"><strong>Instansi Penyelenggara:</strong> ${offer.negara || '-'}</div>
                <div class="modal-detail-row"><strong>Tahun:</strong> ${offer.tahun || '2026'}</div>
                <div class="modal-detail-row"><strong>Kuota:</strong> ${offer.kuantitas || '-'}</div>
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
                const matched = allOffers.find(o => o.judul.toLowerCase().includes(query) || (o.negara && o.negara.toLowerCase().includes(query)));
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