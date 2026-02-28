$filePath = "c:\Users\Win 10\reicetas dolar\index.html"
$content = Get-Content -Path $filePath -Raw -Encoding UTF8

# 1. Images to WebP and compress (Unsplash)
$content = [regex]::Replace($content, '(https://images\.unsplash\.com/[^"''\s]+)', {
    param($m)
    $url = $m.Groups[1].Value
    if ($url -notmatch 'fm=webp') {
        $url += '&fm=webp'
    }
    $url = $url -replace 'q=80', 'q=60'
    return $url
})

# 2. Add loading="lazy" and decoding="async" to img tags
$content = [regex]::Replace($content, '<img\b[^>]*>', {
    param($m)
    $tag = $m.Groups[0].Value
    if ($tag -notmatch 'loading=') {
        $tag = $tag -replace '<img', '<img loading="lazy"'
    }
    if ($tag -notmatch 'decoding=') {
        $tag = $tag -replace '<img', '<img decoding="async"'
    }
    return $tag
})

# Undo lazy for the logo or any eager ones if we needed
$content = $content -replace 'class="hero-logo" loading="lazy"', 'class="hero-logo"'

# 3. Optimize CSS: blurs, shadows, animations duration
$content = $content -replace 'filter: blur\(5px\)', 'filter: blur(2px)'
$content = $content -replace 'filter: blur\(8px\)', 'filter: blur(3px)'
$content = $content -replace 'backdrop-filter: blur\([89]px\)', 'backdrop-filter: blur(3px)'
$content = $content -replace 'box-shadow: 0 40px 70px rgba\(0, 0, 0, 0\.35\)', 'box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2)'
$content = $content -replace 'box-shadow: 0 30px 60px rgba\(0, 0, 0, 0\.35\)', 'box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2)'
$content = $content -replace 'box-shadow: 0 25px 45px rgba\(0, 0, 0, 0\.25\)', 'box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15)'

# Change infinite animations
$content = $content -replace 'animation: driftParticles 25s linear infinite;', '/* animation removed */'
$content = $content -replace 'animation: shimmerSlide 5s infinite;', '/* removed */'
$content = $content -replace 'animation: pulsePlayVSL 2s infinite ease-in-out;', 'animation: pulsePlayVSL 4s infinite ease-in-out;'

# Simplify transforms
$content = $content -replace 'transform: translateY\(-8px\) scale\(1\.02\)', 'transform: translateY(-4px)'
$content = $content -replace 'transform: scale\(1\.05\) translate\(-10px, 10px\)', 'transform: scale(1.02)'

# 4. VSL video
$content = $content -replace 'preload="metadata"', 'preload="none"'
$content = $content -replace 'preload="auto"', 'preload="none"'
if ($content -notmatch 'id="vsl-video" playsinline preload="none"') {
    $content = $content -replace 'id="vsl-video" playsinline', 'id="vsl-video" playsinline preload="none"'
}

# Write back
Set-Content -Path $filePath -Value $content -Encoding UTF8

Write-Host "Optimization done."
