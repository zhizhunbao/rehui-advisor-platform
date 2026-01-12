# 后端生产环境 Dockerfile (Python/FastAPI)
FROM python:3.12-slim AS base

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 构建阶段
FROM base AS builder
WORKDIR /app

# 复制依赖文件
COPY backend/pyproject.toml backend/uv.lock ./

# 安装依赖
RUN uv sync --frozen --no-dev

# 复制源代码
COPY backend/src ./src
COPY backend/alembic ./alembic
COPY backend/alembic.ini ./

# 生产运行阶段
FROM base AS runner
WORKDIR /app

# 创建非 root 用户
RUN groupadd --system --gid 1001 appgroup && \
    useradd --system --uid 1001 --gid appgroup appuser

# 复制虚拟环境和源代码
COPY --from=builder --chown=appuser:appgroup /app/.venv ./.venv
COPY --from=builder --chown=appuser:appgroup /app/src ./src
COPY --from=builder --chown=appuser:appgroup /app/alembic ./alembic
COPY --from=builder --chown=appuser:appgroup /app/alembic.ini ./

USER appuser

EXPOSE 8000

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
