import re

with open('pendaftar.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the checkSyarat function
old_check = '''        function checkSyarat(ipk, toefl) {
            const ipkVal = parseFloat(ipk) || 0;
            const toeflVal = parseInt(toefl) || 0;
            if (ipkVal >= 3.0 && toeflVal >= 500) {
                return "Memenuhi Syarat";
            }
            return "Belum Memenuhi Syarat";
        }'''

new_check = '''        function getSyaratFromBeasiswa(judulBeasiswa) {
            const staticOffers = [
                { judul: "Awards Scholarship Australia", persyaratan: "IPK > 3.0, TOEFL > 500" },
                { judul: "Leadership Training In Korea", persyaratan: "IPK > 3.0, TOEFL > 500" },
                { judul: "Fullbright Program USA", persyaratan: "IPK > 3.0, TOEFL > 500" },
                { judul: "JICA Training Program Japan", persyaratan: "IPK > 3.0, TOEFL > 500" },
                { judul: "Ranu (Beasiswa Thailand)", persyaratan: "IPK > 3.0" },
                { judul: "Ranu (Beasiswa Vietnam)", persyaratan: "IPK > 3.0" },
                { judul: "Ranu (Beasiswa Singapura)", persyaratan: "IPK > 3.0" },
                { judul: "Ranu (Beasiswa Malaysia)", persyaratan: "IPK > 3.0" },
                { judul: "Ranu (Beasiswa Kamboja)", persyaratan: "IPK > 3.0" },
                { judul: "Ranu (Beasiswa Amerika)", persyaratan: "IPK > 3.0" },
                { judul: "Ranu (Beasiswa Inggris)", persyaratan: "IPK > 3.0" },
                { judul: "Ranu (Beasiswa Australia)", persyaratan: "IPK > 3.0" },
                { judul: "Ranu (Beasiswa Selandia Baru)", persyaratan: "IPK > 3.0" },
                { judul: "Ranu (Beasiswa Korea)", persyaratan: "IPK > 3.0" },
                { judul: "Ranu (Beasiswa Jepang)", persyaratan: "IPK > 3.0" }
            ];
            
            const dynamicOffers = JSON.parse(localStorage.getItem('uploaded_scholarships') || '[]');
            const allOffers = [...staticOffers, ...dynamicOffers];
            
            const offer = allOffers.find(o => o.judul === judulBeasiswa);
            
            let minIpk = 0;
            let minToefl = 0;
            
            if (offer && offer.persyaratan) {
                const ipkMatch = offer.persyaratan.match(/IPK\s*[>=]\s*([\d\.]+)/i);
                if (ipkMatch) minIpk = parseFloat(ipkMatch[1]);
                
                const toeflMatch = offer.persyaratan.match(/TOEFL\s*[>=]\s*(\d+)/i);
                if (toeflMatch) minToefl = parseInt(toeflMatch[1]);
            }
            
            return { minIpk, minToefl };
        }

        function checkSyarat(ipk, toefl, judulBeasiswa) {
            const ipkVal = parseFloat(ipk) || 0;
            const toeflVal = parseInt(toefl) || 0;
            
            const syarat = getSyaratFromBeasiswa(judulBeasiswa);
            
            if (ipkVal >= syarat.minIpk && toeflVal >= syarat.minToefl) {
                return "Memenuhi Syarat";
            }
            return "Belum Memenuhi Syarat";
        }'''

content = content.replace(old_check, new_check)

# Update checkSyarat calls in renderTable
# For static rows
content = content.replace(
    'const status = checkSyarat(row.ipk, row.toefl);',
    'const status = checkSyarat(row.ipk, row.toefl, row.beasiswa);'
)

# For dynamic rows
content = content.replace(
    'const status = checkSyarat(appIpk, appToefl);',
    'const status = checkSyarat(appIpk, appToefl, appBeasiswa);'
)

with open('pendaftar.html', 'w', encoding='utf-8') as f:
    f.write(content)
