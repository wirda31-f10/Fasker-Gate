import re

with open('pendaftar.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Menu
content = content.replace(
    '<a href="unggah_tawaran.html" class="submenu-item" style="text-decoration: none; color: #4a5568; font-size: 14px; font-weight: 600;">Unggah Tawaran Beasiswa</a>',
    '<a href="unggah_tawaran.html" class="submenu-item" style="text-decoration: none; color: #4a5568; font-size: 14px; font-weight: 600;">Tawaran Beasiswa</a>'
)

# 2. Filter Status
filter_status_old = '''<select id="status-select" onchange="renderTable()" style="height: 32px; border-radius: 20px; border: 1.5px solid rgba(207, 132, 10, 0.3); padding: 0 16px; outline: none; font-family: inherit; font-size: 12px; min-width: 120px;">
                        <option value="">Semua Status</option>
                        <option value="Verified">Verified (Diterima)</option>
                        <option value="Unverified">Unverified (Ditolak)</option>
                        <option value="Pending">Pending (Proses)</option>
                    </select>'''

filter_status_new = '''<select id="status-select" onchange="renderTable()" style="height: 32px; border-radius: 20px; border: 1.5px solid rgba(207, 132, 10, 0.3); padding: 0 16px; outline: none; font-family: inherit; font-size: 12px; min-width: 120px;">
                        <option value="">Semua Status</option>
                        <option value="Memenuhi Syarat">Memenuhi Syarat</option>
                        <option value="Belum Memenuhi Syarat">Belum Memenuhi Syarat</option>
                    </select>'''
content = content.replace(filter_status_old, filter_status_new)

# 3. Table Header
thead_old = '''                        <tr>
                            <th>No</th>
                            <th>Nama</th>
                            <th>Asal Instansi</th>
                            <th>Pangkat/Gol</th>
                            <th>NIP</th>
                            <th>Tahun</th>
                            <th>Detail</th>
                            <th>Status</th>
                        </tr>'''
thead_new = '''                        <tr>
                            <th>No</th>
                            <th>Nama</th>
                            <th>Asal Instansi</th>
                            <th>Pangkat/Gol</th>
                            <th>NIP</th>
                            <th>Tahun</th>
                            <th>Nama Beasiswa</th>
                            <th>IPK</th>
                            <th>TOEFL</th>
                            <th>Detail</th>
                            <th>Status</th>
                        </tr>'''
content = content.replace(thead_old, thead_new)

# 4. We will replace the entire tbody and script for rendering to avoid messy HTML changes
script_old_start = 'const defaultStaticRows = ['
script_old_end = 'function showStaticDetails(id, event) {'

# Remove existing tbody static rows (lines 170 to 386 approx)
tbody_pattern = re.compile(r'(<tbody id="verifikasi-tbody">).*?(</tbody>)', re.DOTALL)
content = tbody_pattern.sub(r'\1\n                    \2', content)

script_new = '''
        const staticASNs = {
            1: { nama: "Ranu", email: "ranu@gmail.com", instansi: "KemenDagri", gol: "Gol. III", nip: "234567" },
            2: { nama: "Rian", email: "rian@gmail.com", instansi: "Bappenas", gol: "Gol. II", nip: "765432" },
            3: { nama: "Ranu", email: "ranu@gmail.com", instansi: "KemenDagri", gol: "Gol. III", nip: "234567" },
            4: { nama: "Rizky", email: "rizky@gmail.com", instansi: "Kemenkeu", gol: "Gol. IV", nip: "345678" },
            5: { nama: "Ranu", email: "ranu@gmail.com", instansi: "KemenDagri", gol: "Gol. III", nip: "234567" },
            6: { nama: "Rafi", email: "rafi@gmail.com", instansi: "Kemenkumham", gol: "Gol. III", nip: "876543" },
            7: { nama: "Ranu", email: "ranu@gmail.com", instansi: "KemenDagri", gol: "Gol. III", nip: "234567" },
            8: { nama: "Rama", email: "rama@gmail.com", instansi: "Kemendikbud", gol: "Gol. II", nip: "543210" },
            9: { nama: "Ranu", email: "ranu@gmail.com", instansi: "KemenDagri", gol: "Gol. III", nip: "234567" },
            10: { nama: "Rehan", email: "rehan@gmail.com", instansi: "Kementerian ESDM", gol: "Gol. III", nip: "123456" },
            11: { nama: "Ranu", email: "ranu@gmail.com", instansi: "KemenDagri", gol: "Gol. III", nip: "234567" },
            12: { nama: "Roni", email: "roni@gmail.com", instansi: "Kementerian Perhubungan", gol: "Gol. IV", nip: "987654" }
        };

        const defaultStaticRows = [
            { id: 1, tahun: '2025', beasiswa: 'Awards Scholarship Australia', ipk: '3.5', toefl: '550' },
            { id: 2, tahun: '2025', beasiswa: 'Leadership Training In Korea', ipk: '2.8', toefl: '450' },
            { id: 3, tahun: '2024', beasiswa: 'Fullbright Program USA', ipk: '3.8', toefl: '600' },
            { id: 4, tahun: '2024', beasiswa: 'JICA Training Program Japan', ipk: '2.5', toefl: '480' },
            { id: 5, tahun: '2023', beasiswa: 'Awards Scholarship Australia', ipk: '3.2', toefl: '520' },
            { id: 6, tahun: '2023', beasiswa: 'Leadership Training In Korea', ipk: '3.6', toefl: '540' },
            { id: 7, tahun: '2022', beasiswa: 'Fullbright Program USA', ipk: '2.9', toefl: '490' },
            { id: 8, tahun: '2022', beasiswa: 'JICA Training Program Japan', ipk: '3.9', toefl: '610' },
            { id: 9, tahun: '2021', beasiswa: 'Awards Scholarship Australia', ipk: '2.7', toefl: '470' },
            { id: 10, tahun: '2021', beasiswa: 'Leadership Training In Korea', ipk: '3.1', toefl: '490' },
            { id: 11, tahun: '2020', beasiswa: 'Fullbright Program USA', ipk: '2.6', toefl: '510' },
            { id: 12, tahun: '2020', beasiswa: 'JICA Training Program Japan', ipk: '3.4', toefl: '530' }
        ];

        function checkSyarat(ipk, toefl) {
            const ipkVal = parseFloat(ipk) || 0;
            const toeflVal = parseInt(toefl) || 0;
            if (ipkVal >= 3.0 && toeflVal >= 500) {
                return "Memenuhi Syarat";
            }
            return "Belum Memenuhi Syarat";
        }

        function renderTable() {
            const tbody = document.getElementById('verifikasi-tbody');
            const selectedTahun = document.getElementById('tahun-select').value;
            const selectedStatus = document.getElementById('status-select').value;
            
            const deletedStatics = JSON.parse(localStorage.getItem('deleted_static_rows') || '[]');
            
            tbody.innerHTML = '';
            const rowsToRender = [];

            // Add static rows
            defaultStaticRows.forEach(row => {
                if (deletedStatics.includes(row.id)) return;
                
                const asnData = staticASNs[row.id];
                const status = checkSyarat(row.ipk, row.toefl);
                
                const matchesTahun = !selectedTahun || row.tahun === selectedTahun;
                const matchesStatus = !selectedStatus || status === selectedStatus;
                
                if (matchesTahun && matchesStatus) {
                    const statusHtml = status === 'Memenuhi Syarat' 
                        ? `<button class="status-btn verified" style="pointer-events: none; cursor: default; width: 130px; font-size: 11px;">Memenuhi Syarat</button>`
                        : `<button class="status-btn unverified" style="pointer-events: none; cursor: default; width: 140px; font-size: 11px;">Belum Memenuhi</button>`;
                        
                    const tr = document.createElement('tr');
                    tr.setAttribute('data-type', 'static');
                    tr.setAttribute('data-id', row.id);
                    tr.setAttribute('data-tahun', row.tahun);
                    tr.style.cursor = 'pointer';
                    tr.addEventListener('click', (e) => showStaticDetails(row.id, e));
                    
                    tr.innerHTML = `
                        <td></td>
                        <td><input type="text" class="table-input" value="${asnData.nama}" readonly style="pointer-events: none;"></td>
                        <td><input type="text" class="table-input" value="${asnData.instansi}" readonly style="pointer-events: none;"></td>
                        <td><input type="text" class="table-input" value="${asnData.gol}" readonly style="pointer-events: none; width: 60px;"></td>
                        <td><input type="text" class="table-input" value="${asnData.nip}" readonly style="pointer-events: none;"></td>
                        <td><input type="text" class="table-input" value="${row.tahun}" readonly style="pointer-events: none; width: 45px;"></td>
                        <td><input type="text" class="table-input" value="${row.beasiswa}" readonly style="pointer-events: none; width: 140px;"></td>
                        <td><input type="text" class="table-input" value="${row.ipk}" readonly style="pointer-events: none; width: 35px; text-align: center;"></td>
                        <td><input type="text" class="table-input" value="${row.toefl}" readonly style="pointer-events: none; width: 45px; text-align: center;"></td>
                        <td>
                            <button class="btn-icon">
                                <svg viewBox="0 0 24 24" fill="none" stroke="#0d6efd" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:18px;height:18px;">
                                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                                </svg>
                            </button>
                        </td>
                        <td>${statusHtml}</td>
                    `;
                    rowsToRender.push(tr);
                }
            });

            // Add dynamic rows
            const apps = JSON.parse(localStorage.getItem('asn_applications') || '[]');
            apps.forEach((app, idx) => {
                const appTahun = app.tahun || '2026';
                const appBeasiswa = app.judul || 'Awards Scholarship Australia';
                
                // Assign mock ipk and toefl if not exist in app data
                const appIpk = app.ipk || (idx % 2 === 0 ? '3.5' : '2.8');
                const appToefl = app.toefl || (idx % 2 === 0 ? '520' : '480');
                const status = checkSyarat(appIpk, appToefl);
                
                if (selectedTahun && appTahun !== selectedTahun) return;
                if (selectedStatus && status !== selectedStatus) return;
                
                const statusHtml = status === 'Memenuhi Syarat' 
                        ? `<button class="status-btn verified" style="pointer-events: none; cursor: default; width: 130px; font-size: 11px;">Memenuhi Syarat</button>`
                        : `<button class="status-btn unverified" style="pointer-events: none; cursor: default; width: 140px; font-size: 11px;">Belum Memenuhi</button>`;
                        
                const tr = document.createElement('tr');
                tr.setAttribute('data-type', 'dynamic');
                tr.setAttribute('data-index', idx);
                tr.setAttribute('data-tahun', appTahun);
                tr.style.cursor = 'pointer';
                tr.addEventListener('click', (e) => showDynamicDetails(idx, e));
                
                tr.innerHTML = `
                    <td></td>
                    <td><input type="text" class="table-input" value="${app.nama}" readonly style="pointer-events: none;"></td>
                    <td><input type="text" class="table-input" value="${app.instansi}" readonly style="pointer-events: none;"></td>
                    <td><input type="text" class="table-input" value="${app.gol}" readonly style="pointer-events: none; width: 60px;"></td>
                    <td><input type="text" class="table-input" value="${app.nip}" readonly style="pointer-events: none;"></td>
                    <td><input type="text" class="table-input" value="${appTahun}" readonly style="pointer-events: none; width: 45px;"></td>
                    <td><input type="text" class="table-input" value="${appBeasiswa}" readonly style="pointer-events: none; width: 140px;"></td>
                    <td><input type="text" class="table-input" value="${appIpk}" readonly style="pointer-events: none; width: 35px; text-align: center;"></td>
                    <td><input type="text" class="table-input" value="${appToefl}" readonly style="pointer-events: none; width: 45px; text-align: center;"></td>
                    <td>
                        <button class="btn-icon">
                            <svg viewBox="0 0 24 24" fill="none" stroke="#0d6efd" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:18px;height:18px;">
                                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                            </svg>
                        </button>
                    </td>
                    <td>${statusHtml}</td>
                `;
                rowsToRender.push(tr);
            });

            // Sort and append
            rowsToRender.sort((a, b) => {
                const yearA = parseInt(a.getAttribute('data-tahun')) || 0;
                const yearB = parseInt(b.getAttribute('data-tahun')) || 0;
                return yearB - yearA;
            });
            
            let visibleIndex = 1;
            rowsToRender.forEach(row => {
                row.cells[0].textContent = `${visibleIndex++}.`;
                tbody.appendChild(row);
            });
        }
        
        function showStaticDetails(id, event) {
'''

idx_start = content.find(script_old_start)
idx_end = content.find(script_old_end)

if idx_start != -1 and idx_end != -1:
    content = content[:idx_start] + script_new + content[idx_end + len(script_old_end):]

# Remove staticASNs dictionary inside showStaticDetails
content = re.sub(r'const staticASNs = \{[^}]*\};\s*', '', content, flags=re.DOTALL)

with open('pendaftar.html', 'w', encoding='utf-8') as f:
    f.write(content)
