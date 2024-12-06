# MemOS AI Production Deployment Guide

## Overview

This guide provides detailed examples of deploying MemOS AI in production environments, including infrastructure setup, monitoring, and maintenance.

## Infrastructure Setup

### 1. Kubernetes Deployment

```yaml
# memos-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: memos-api
  namespace: memos-production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: memos-api
  template:
    metadata:
      labels:
        app: memos-api
    spec:
      containers:
      - name: memos-api
        image: memos/api:latest
        ports:
        - containerPort: 8000
        env:
        - name: MEMOS_ENV
          value: "production"
        - name: MEMOS_LOG_LEVEL
          value: "info"
        - name: MEMOS_DB_URL
          valueFrom:
            secretKeyRef:
              name: memos-secrets
              key: db-url
        resources:
          limits:
            cpu: "2"
            memory: "4Gi"
          requests:
            cpu: "500m"
            memory: "1Gi"
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 20

---
# memos-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: memos-api
  namespace: memos-production
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: memos-api

---
# memos-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: memos-api
  namespace: memos-production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: memos-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 2. Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    image: memos/api:latest
    ports:
      - "8000:8000"
    environment:
      - MEMOS_ENV=production
      - MEMOS_LOG_LEVEL=info
    depends_on:
      - postgres
      - redis
      - elasticsearch
    networks:
      - memos-network
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 1G

  worker:
    build: .
    image: memos/worker:latest
    command: celery -A memos.tasks worker
    environment:
      - MEMOS_ENV=production
    depends_on:
      - redis
    networks:
      - memos-network
    deploy:
      replicas: 2

  postgres:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=memos
      - POSTGRES_USER=memos
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    networks:
      - memos-network
    secrets:
      - db_password

  redis:
    image: redis:6-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - memos-network

  elasticsearch:
    image: elasticsearch:7.14.0
    environment:
      - discovery.type=single-node
      - ES_JAVA_OPTS=-Xms512m -Xmx512m
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    networks:
      - memos-network

networks:
  memos-network:
    driver: overlay

volumes:
  postgres_data:
  redis_data:
  elasticsearch_data:

secrets:
  db_password:
    external: true
```

## Monitoring Setup

### 1. Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'memos-api'
    static_configs:
      - targets: ['memos-api:8000']
    metrics_path: '/metrics'
    scheme: 'http'

  - job_name: 'memos-worker'
    static_configs:
      - targets: ['memos-worker:8000']
    metrics_path: '/metrics'
    scheme: 'http'

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
```

### 2. Grafana Dashboard

```json
{
  "dashboard": {
    "id": null,
    "title": "MemOS AI Production Metrics",
    "tags": ["memos", "production"],
    "timezone": "browser",
    "panels": [
      {
        "title": "API Request Rate",
        "type": "graph",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{path}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])",
            "legendFormat": "{{method}} {{path}}"
          }
        ]
      }
    ]
  }
}
```

## CI/CD Pipeline

### 1. GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest tests/

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build Docker image
      run: docker build -t memos/api:${{ github.sha }} .
    - name: Push to registry
      run: |
        docker login -u ${{ secrets.DOCKER_USER }} -p ${{ secrets.DOCKER_PASSWORD }}
        docker push memos/api:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Kubernetes
      uses: steebchen/kubectl@v2
      with:
        config: ${{ secrets.KUBE_CONFIG_DATA }}
        command: set image deployment/memos-api memos-api=memos/api:${{ github.sha }} -n memos-production
```

## Backup and Recovery

### 1. Database Backup Script

```python
# scripts/backup.py
import subprocess
from datetime import datetime
import boto3
import os

class DatabaseBackup:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = os.environ['BACKUP_BUCKET']
        self.db_url = os.environ['DATABASE_URL']

    def create_backup(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"backup_{timestamp}.sql"
        
        # Create backup
        subprocess.run([
            'pg_dump',
            self.db_url,
            '-F', 'c',
            '-f', filename
        ])
        
        # Upload to S3
        self.s3.upload_file(
            filename,
            self.bucket,
            f"backups/{filename}"
        )
        
        # Cleanup
        os.remove(filename)

    def restore_backup(self, backup_file):
        # Download from S3
        self.s3.download_file(
            self.bucket,
            f"backups/{backup_file}",
            backup_file
        )
        
        # Restore backup
        subprocess.run([
            'pg_restore',
            '-d', self.db_url,
            '-c',
            backup_file
        ])
        
        # Cleanup
        os.remove(backup_file)
```

## Performance Tuning

### 1. NGINX Configuration

```nginx
# nginx.conf
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 65535;
    multi_accept on;
    use epoll;
}

http {
    include mime.types;
    default_type application/octet-stream;

    # Optimization
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    keepalive_requests 100;

    # Buffers
    client_body_buffer_size 10K;
    client_header_buffer_size 1k;
    client_max_body_size 8m;
    large_client_header_buffers 2 1k;

    # Caching
    open_file_cache max=200000 inactive=20s;
    open_file_cache_valid 30s;
    open_file_cache_min_uses 2;
    open_file_cache_errors on;

    # Gzip
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml application/json application/javascript application/xml+rss application/atom+xml image/svg+xml;

    # SSL
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    upstream memos_api {
        server 127.0.0.1:8000;
        keepalive 32;
    }

    server {
        listen 80;
        server_name api.memos-ai.org;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name api.memos-ai.org;

        ssl_certificate /etc/letsencrypt/live/api.memos-ai.org/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/api.memos-ai.org/privkey.pem;

        location / {
            proxy_pass http://memos_api;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }
    }
}
```

### 2. PostgreSQL Tuning

```ini
# postgresql.conf
max_connections = 200
shared_buffers = 4GB
effective_cache_size = 12GB
maintenance_work_mem = 1GB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 20MB
min_wal_size = 1GB
max_wal_size = 4GB
max_worker_processes = 8
max_parallel_workers_per_gather = 4
max_parallel_workers = 8
max_parallel_maintenance_workers = 4

# Logging
log_min_duration_statement = 1000
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on
log_temp_files = 0
log_autovacuum_min_duration = 0
```

## Security Configuration

### 1. Security Headers Middleware

```python
from fastapi import FastAPI, Request
from fastapi.middleware.base import BaseHTTPMiddleware
from typing import Callable

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable
    ):
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response

app = FastAPI()
app.add_middleware(SecurityHeadersMiddleware)
```

### 2. Rate Limiting Configuration

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
from typing import Dict, Tuple

class RateLimiter:
    def __init__(self, rate_limit: int, time_window: int):
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.requests: Dict[str, list] = {}

    async def is_rate_limited(self, key: str) -> Tuple[bool, int]:
        now = time.time()
        
        # Clean old requests
        self.requests[key] = [
            req_time for req_time in self.requests.get(key, [])
            if now - req_time < self.time_window
        ]
        
        # Check rate limit
        if len(self.requests[key]) >= self.rate_limit:
            return True, self.time_window - (now - self.requests[key][0])
        
        # Add new request
        self.requests[key] = self.requests.get(key, []) + [now]
        return False, 0

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        rate_limit: int = 100,
        time_window: int = 60
    ):
        super().__init__(app)
        self.limiter = RateLimiter(rate_limit, time_window)

    async def dispatch(
        self, request: Request, call_next: Callable
    ):
        key = request.client.host
        is_limited, retry_after = await self.limiter.is_rate_limited(key)
        
        if is_limited:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "retry_after": retry_after
                }
            )
        
        return await call_next(request)

app.add_middleware(RateLimitMiddleware)
```

## Maintenance Procedures

### 1. Database Maintenance Script

```python
import psycopg2
from datetime import datetime, timedelta
import logging

class DatabaseMaintenance:
    def __init__(self, db_url: str):
        self.conn = psycopg2.connect(db_url)
        self.logger = logging.getLogger(__name__)

    async def perform_maintenance(self):
        try:
            # Vacuum analyze
            await self._vacuum_analyze()
            
            # Clean old data
            await self._clean_old_data()
            
            # Reindex
            await self._reindex()
            
            # Update statistics
            await self._update_statistics()
            
        except Exception as e:
            self.logger.error(f"Maintenance failed: {e}")
            raise
        finally:
            self.conn.close()

    async def _vacuum_analyze(self):
        with self.conn.cursor() as cur:
            cur.execute("VACUUM ANALYZE;")
            self.logger.info("Vacuum analyze completed")

    async def _clean_old_data(self):
        threshold = datetime.now() - timedelta(days=90)
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM interaction_history WHERE created_at < %s",
                (threshold,)
            )
            self.logger.info(f"Cleaned {cur.rowcount} old records")

    async def _reindex(self):
        with self.conn.cursor() as cur:
            cur.execute("REINDEX DATABASE memos;")
            self.logger.info("Database reindexed")

    async def _update_statistics(self):
        with self.conn.cursor() as cur:
            cur.execute("ANALYZE VERBOSE;")
            self.logger.info("Statistics updated")
```

## Disaster Recovery Plan

### 1. Recovery Procedures

```python
from typing import Optional
import boto3
import subprocess
import logging

class DisasterRecovery:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.logger = logging.getLogger(__name__)
        self.backup_bucket = "memos-backups"
        self.region = "us-west-2"

    async def initiate_recovery(
        self,
        incident_type: str,
        backup_id: Optional[str] = None
    ):
        try:
            # Stop services
            await self._stop_services()
            
            # Restore data
            await self._restore_data(backup_id)
            
            # Verify recovery
            await self._verify_recovery()
            
            # Restart services
            await self._start_services()
            
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            await self._notify_team(f"Recovery failed: {e}")
            raise

    async def _stop_services(self):
        subprocess.run(["kubectl", "scale", "deployment", "memos-api", "--replicas=0"])
        self.logger.info("Services stopped")

    async def _restore_data(self, backup_id: Optional[str]):
        if not backup_id:
            backup_id = await self._get_latest_backup()
        
        # Download backup
        self.s3.download_file(
            self.backup_bucket,
            f"backups/{backup_id}",
            "backup.sql"
        )
        
        # Restore database
        subprocess.run([
            "pg_restore",
            "-d", "memos",
            "-c",
            "backup.sql"
        ])
        
        self.logger.info(f"Data restored from backup {backup_id}")

    async def _verify_recovery(self):
        # Verify database
        # Verify file storage
        # Verify cache
        pass

    async def _start_services(self):
        subprocess.run(["kubectl", "scale", "deployment", "memos-api", "--replicas=3"])
        self.logger.info("Services started")

    async def _notify_team(self, message: str):
        # Send notification to team
        pass

    async def _get_latest_backup(self) -> str:
        response = self.s3.list_objects_v2(
            Bucket=self.backup_bucket,
            Prefix="backups/"
        )
        
        backups = sorted(
            response['Contents'],
            key=lambda x: x['LastModified'],
            reverse=True
        )
        
        return backups[0]['Key'].split('/')[-1]
```

## Next Steps

1. **Infrastructure Improvements**
   - Implement multi-region deployment
   - Set up blue-green deployments
   - Enhance auto-scaling policies

2. **Monitoring Enhancements**
   - Add business metrics
   - Implement anomaly detection
   - Create custom alerting rules

3. **Security Updates**
   - Implement WAF rules
   - Add DDoS protection
   - Enhance authentication system

4. **Performance Optimization**
   - Optimize database queries
   - Implement caching strategies
   - Enhance load balancing 