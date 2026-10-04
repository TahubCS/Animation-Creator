param(
    [ValidateSet('All', 'Build', 'Draft', 'Final', 'Verify')]
    [string]$Mode = 'All',
    [string]$Blender = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Blender)) { throw "Blender not found: $Blender" }
Set-Location -LiteralPath $PSScriptRoot
New-Item -ItemType Directory -Force -Path 'logs','renders\draft','renders\review','renders\frames' | Out-Null

function Invoke-BlenderTask {
    param([string]$Script, [string]$Log, [switch]$Scene, [switch]$Draft)
    $taskArgs = @('--background')
    if ($Scene) { $taskArgs += (Join-Path $PSScriptRoot 'scene.blend') }
    else { $taskArgs += '--factory-startup' }
    $taskArgs += @('--python-exit-code', '1', '--python', (Join-Path $PSScriptRoot $Script))
    if ($Draft) { $taskArgs += @('--', '--draft') }
    Write-Host "Running $Script (draft=$Draft)"
    # Windows PowerShell treats native stderr warnings as errors. Capture them
    # while using the actual Blender exit code to decide whether work succeeded.
    $savedPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    & $Blender @taskArgs *> (Join-Path $PSScriptRoot "logs\$Log")
    $code = $LASTEXITCODE
    $ErrorActionPreference = $savedPreference
    if ($code -ne 0) { throw "$Script failed ($code). See logs\$Log" }
}

if ($Mode -in @('All','Build')) {
    Invoke-BlenderTask -Script 'build_scene.py' -Log 'build.log' -Draft
    Invoke-BlenderTask -Script 'verify_scene.py' -Log 'scene_checks.log' -Scene
}
if ($Mode -in @('All','Draft')) {
    Invoke-BlenderTask -Script 'render_saved.py' -Log 'draft_sequence.log' -Scene -Draft
    Invoke-BlenderTask -Script 'encode_preview.py' -Log 'draft_encode.log' -Draft
    Invoke-BlenderTask -Script 'verify_preview.py' -Log 'draft_media_checks.log' -Draft
    python (Join-Path $PSScriptRoot 'make_review.py') --draft
    if ($LASTEXITCODE -ne 0) { throw 'Draft contact-sheet generation failed' }
}
if ($Mode -in @('All','Final')) {
    Invoke-BlenderTask -Script 'render_saved.py' -Log 'final_render.log' -Scene
    Invoke-BlenderTask -Script 'encode_preview.py' -Log 'encode.log'
    Invoke-BlenderTask -Script 'verify_preview.py' -Log 'media_checks.log'
    python (Join-Path $PSScriptRoot 'make_review.py')
    if ($LASTEXITCODE -ne 0) { throw 'Contact-sheet generation failed' }
    python (Join-Path $PSScriptRoot 'review_joints.py') --after
    if ($LASTEXITCODE -ne 0) { throw 'Foot-joint temporal check failed' }
}
if ($Mode -eq 'Verify') {
    Invoke-BlenderTask -Script 'verify_scene.py' -Log 'scene_checks.log' -Scene
    Invoke-BlenderTask -Script 'verify_preview.py' -Log 'media_checks.log'
    python (Join-Path $PSScriptRoot 'make_review.py')
    if ($LASTEXITCODE -ne 0) { throw 'Contact-sheet generation failed' }
    python (Join-Path $PSScriptRoot 'review_joints.py') --after
    if ($LASTEXITCODE -ne 0) { throw 'Foot-joint temporal check failed' }
}
Write-Host 'Requested stage completed. See verification.md for the recorded review.'
