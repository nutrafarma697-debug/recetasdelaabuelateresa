$filePath = "c:\Users\Win 10\reicetas dolar\index.html"
$content = Get-Content -Path $filePath -Raw -Encoding UTF8

# Minify CSS: Remove multi-line comments
$content = [regex]::Replace($content, '/\*.*?\*/', '', [System.Text.RegularExpressions.RegexOptions]::Singleline)

# Remove extra whitespace (multiple spaces/newlines) inside CSS ONLY? 
# To avoid breaking HTML pre/code or JS strings, we should ideally restrict this. 
# It's safer to just remove large blocks of whitespace globally outside of specific contexts, 
# but simply removing comments already helps a lot. 
# Let's remove lines that are completely empty or just spaces to compress the file
$content = [regex]::Replace($content, '(?m)^\s*$', '')

# Minify JS: Remove some // comments, but careful not to match URLs like https://
# JS single line comments: \s*//[^"''\n]+
# But let's avoid touching JS deeply to prevent breaking logic.

Set-Content -Path $filePath -Value $content -Encoding UTF8

Write-Host "Minification done."
