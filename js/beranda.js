document.addEventListener("DOMContentLoaded", () => {
    const searchBtn = document.querySelector(".btn-search");
    const searchInput = document.getElementById("searchInput");

    if (searchBtn && searchInput) {
        const runSearch = () => {
            const query = searchInput.value.trim();

            if (query) {
                alert("Mencari program: " + query);
            }
        };

        searchBtn.addEventListener("click", runSearch);

        searchInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                runSearch();
            }
        });
    }

    // --- Dynamic Statistics from LocalStorage ---
    
    // 1. Program Aktif (Tawaran beasiswa tahun berjalan / 2026)
    const offers = JSON.parse(localStorage.getItem('uploaded_scholarships') || '[]');
    let openOffers = 4; // 4 penawaran statis (default) untuk tahun 2026
    offers.forEach(o => {
        if ((o.tahun || '2026') === '2026') openOffers++;
    });

    // 2. Data Pelamar & Rekomendasi
    const apps = JSON.parse(localStorage.getItem('asn_applications') || '[]');
    let totalApps = apps.length;
    let totalVerified = apps.filter(a => a.status === 'Verified').length;
    let totalPending = apps.filter(a => (a.status || 'Pending') === 'Pending').length;

    if (localStorage.getItem('asn_applications_seeded') !== 'true') {
        // Jika data dinamis (dari admin.html) belum di-seed, gunakan nilai statis + inputan manual saat ini
        totalApps += 12; // 12 default static rows
        totalVerified += 6; // 6 baris statis default adalah 'Verified'
        // Sisa 6 nya adalah 'Unverified'
    }

    // Rekomendasi diartikan sebagai semua yang sudah lolos (Verified) + yang masih diproses (Pending)
    const totalRekomendasi = totalVerified + totalPending;

    // Update DOM
    const statProgram = document.getElementById('stat-program');
    const statPelamar = document.getElementById('stat-pelamar');
    const statRekomendasi = document.getElementById('stat-rekomendasi');
    const statPenerima = document.getElementById('stat-penerima');

    if (statProgram) statProgram.innerText = openOffers;
    if (statPelamar) statPelamar.innerText = totalApps;
    if (statRekomendasi) statRekomendasi.innerText = totalRekomendasi;
    if (statPenerima) statPenerima.innerText = totalVerified;
});