# PowerShell Script to Remove Unnecessary Files from Django Project
# This script removes old duplicate files and unnecessary documentation

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Removing Unnecessary Files" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Files to delete
$filesToDelete = @(
    # Old HTML files (duplicates - Django uses main/templates/main/)
    "home.html",
    "About.html",
    "Contact.html",
    "Courses.html",
    "Services.html",
    "index.html",
    "Gallery.html",
    
    # Old CSS files (duplicates - Django uses main/static/main/css/)
    "home.css",
    "About.css",
    "booking.css",
    "contact.css",
    "style.css",
    "auth.css",
    "Services.css",
    "header.css",
    "footer.css",
    "Courses.css",
    
    # Old JavaScript files (duplicates - Django uses main/static/main/js/)
    "api.js",
    "auth-modal.js",
    "booking-modal.js",
    "script.js",
    
    # Temporary/Redundant documentation files
    "BOOKING_FIX_SUMMARY.md",
    "EMAIL_SETUP_INSTRUCTIONS.md",
    "FIX_401_ERROR.md",
    "QUICK_EMAIL_FIX.md",
    "WHATSAPP_SETUP.md",
    "PROJECT_CLEANUP_REPORT.md",
    "CLEANUP_SUMMARY.md",
    
    # Cleanup scripts (no longer needed)
    "cleanup_duplicates.ps1",
    
    # Production settings (optional - keeping as reference)
    # "SingingBallAndGongHouse\settings_production.py"  # Commented out - you might want to keep this
)

Write-Host "Files to be deleted:" -ForegroundColor Yellow
Write-Host "-------------------" -ForegroundColor Yellow

$totalSize = 0
$foundFiles = @()
$notFoundFiles = @()

foreach ($file in $filesToDelete) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length
        $totalSize += $size
        $foundFiles += $file
        $sizeKB = [math]::Round($size/1KB, 2)
        Write-Host "  [OK] $file ($sizeKB KB)" -ForegroundColor Green
    } else {
        $notFoundFiles += $file
        Write-Host "  [SKIP] $file (not found)" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Files found: $($foundFiles.Count)" -ForegroundColor Green
Write-Host "  Files not found: $($notFoundFiles.Count)" -ForegroundColor Gray
Write-Host "  Total size: $([math]::Round($totalSize/1KB, 2)) KB" -ForegroundColor Yellow
Write-Host ""

# Ask for confirmation
$confirmation = Read-Host "Do you want to delete these files? (yes/no)"
if ($confirmation -ne "yes") {
    Write-Host "Cleanup cancelled." -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "Deleting files..." -ForegroundColor Cyan

$deletedCount = 0
foreach ($file in $foundFiles) {
    try {
        Remove-Item $file -Force -ErrorAction Stop
        Write-Host "  [DELETED] $file" -ForegroundColor Green
        $deletedCount++
    } catch {
        Write-Host "  [ERROR] $file - $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Cleanup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Files deleted: $deletedCount" -ForegroundColor Green
Write-Host "Space freed: $([math]::Round($totalSize/1KB, 2)) KB" -ForegroundColor Green
Write-Host ""
Write-Host "Note: The 'images' folder in root is kept as backup." -ForegroundColor Yellow
Write-Host "Django uses images from: main/static/main/images/" -ForegroundColor Yellow
Write-Host ""

