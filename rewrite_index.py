import re

with open('js/index.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Make getAllOffers async and use Supabase
old_get_all = """function getAllOffers() {
    const dynamicOffers = JSON.parse(localStorage.getItem('uploaded_scholarships') || '[]');"""
new_get_all = """async function getAllOffers() {
    const { data: dynamicOffersList, error } = await window.supabase.from('fasker_scholarships').select('*');
    if (error) console.error("Error fetching scholarships:", error);
    const dynamicOffers = dynamicOffersList || [];"""
content = content.replace(old_get_all, new_get_all)

# Make DOMContentLoaded async
content = content.replace('document.addEventListener("DOMContentLoaded", () => {', 'document.addEventListener("DOMContentLoaded", async () => {')

# Await getAllOffers in render
content = content.replace('const allOffers = getAllOffers();', 'const allOffers = await getAllOffers();')

# Await getAllOffers in search
content = content.replace('const runSearch = () => {', 'const runSearch = async () => {')

with open('js/index.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Rewrote index.js")
