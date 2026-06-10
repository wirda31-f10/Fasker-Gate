import os

files = ['admin.html', 'verifikasi.html', 'unggah_tawaran.html', 'pendaftar.html']
output_path = r'C:\Users\Lenovo\.gemini\antigravity\brain\940636df-d4d1-4f54-9a9f-4b2abc981384\full_scripts.md'

with open(output_path, 'w', encoding='utf-8') as out:
    out.write('# Kode Lengkap Halaman Admin\n\n')
    out.write('Berikut adalah 4 script HTML lengkap yang telah diperbarui:\n\n')
    
    for filename in files:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            out.write(f'## {filename}\n')
            out.write('```html\n')
            out.write(content)
            out.write('\n```\n\n')
