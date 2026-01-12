# 启动开发环境
param(
    [switch]$Build,
    [switch]$Logs
)

Write-Host "🚀 启动 Rehui Advisor 开发环境..." -ForegroundColor Green

# 检查 Docker 是否运行
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker 未运行，请先启动 Docker Desktop" -ForegroundColor Red
    exit 1
}

# 切换到 docker/development 目录
$originalPath = Get-Location
Set-Location "$PSScriptRoot/../development"

try {
    # 构建镜像（如果需要）
    if ($Build) {
        Write-Host "🔨 构建 Docker 镜像..." -ForegroundColor Yellow
        docker-compose build
    }

    # 启动服务
    Write-Host "⏳ 启动服务..." -ForegroundColor Yellow
    docker-compose up -d

    # 等待服务健康检查
    Write-Host "🔍 等待服务启动..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10

    # 检查服务状态
    Write-Host "`n📊 服务状态:" -ForegroundColor Cyan
    docker-compose ps

    Write-Host "`n✅ 开发环境已启动！" -ForegroundColor Green
    Write-Host "🐘 PostgreSQL: localhost:5432 (数据库: rehui_advisor)" -ForegroundColor Cyan
    Write-Host "🔴 Redis: localhost:6379" -ForegroundColor Cyan
    Write-Host "🔧 pgAdmin: http://localhost:5050 (admin@example.com / admin)" -ForegroundColor Cyan

    # 显示日志（如果需要）
    if ($Logs) {
        Write-Host "`n📋 显示服务日志..." -ForegroundColor Yellow
        docker-compose logs -f
    }

} finally {
    Set-Location $originalPath
}