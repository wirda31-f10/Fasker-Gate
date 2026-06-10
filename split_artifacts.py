import os

files = ['admin.html', 'verifikasi.html', 'unggah_tawaran.html', 'pendaftar.html']
base_dir = r'C:\Users\Lenovo\.gemini\antigravity\brain\940636df-d4d1-4f54-9a9f-4b2abc981384'

for filename in files:
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        art_name = filename.replace('.html', '_script.md')
        out_path = os.path.join(base_dir, art_name)
        
        with open(out_path, 'w', encoding='utf-8') as out:
            out.write(f'# {filename}\n\n')
            out.write('```html\n')
            out.write(content)
            out.write('\n```\n')
