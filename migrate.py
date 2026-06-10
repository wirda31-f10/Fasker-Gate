import os
import re

SUPABASE_URL = 'https://ogsstamvptbknfvaddtt.supabase.co'
SUPABASE_KEY = 'sb_publishable_aSaLqvCDEyJownZDN9WgOw_nCn0JAe-'

supabase_tag = f"""
    <!-- Supabase -->
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script>
        const supabaseUrl = '{SUPABASE_URL}';
        const supabaseKey = '{SUPABASE_KEY}';
        const supabase = window.supabase.createClient(supabaseUrl, supabaseKey);
    </script>
"""

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '@supabase/supabase-js' not in content:
        if '</head>' in content:
            content = content.replace('</head>', supabase_tag + '</head>')
        else:
            content = supabase_tag + content
            
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Injected Supabase into HTML files.")
