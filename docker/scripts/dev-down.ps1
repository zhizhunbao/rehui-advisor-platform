# 停止开发环境
param(
    [switch]$Volumes,
    [switch]$Images
)

Write-Host "🛑 停止 Rehui Advisor 开发环境..." -ForegroundColor Yellow

# 切换到 docker/development 目录
$originalPath = Get-Location
Set-Location "$PSScriptRoot/../development"

try {
    # 停止服务
    if ($Volumes) {
        Write-Host "🗑️ 停止服务并删除数据卷..." -ForegroundColor Red
        docker-compose down -v
    } else {
        docker-compose down
    }

    # 删除镜像（如果需要）
    if ($Images) {
        Write-Host "🗑️ 删除相关镜像..." -ForegroundColor Red
        docker-compose down --rmi all
    }

    Write-Host "✅ 开发环境已停止！" -ForegroundColor Green

} finally {
    Set-Location $originalPath
}