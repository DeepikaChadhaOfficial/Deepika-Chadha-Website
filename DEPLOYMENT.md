# Deployment Guide

## Local Development

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 4. Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  eps-proxy:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

## Production Deployment (Ubuntu/Debian)

### 1. Install System Dependencies

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx
```

### 2. Setup Application

```bash
# Create app directory
sudo mkdir -p /opt/eps-proxy
sudo chown $USER:$USER /opt/eps-proxy
cd /opt/eps-proxy

# Clone/copy your code
# ...

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with your credentials
```

### 3. Create Systemd Service

Create `/etc/systemd/system/eps-proxy.service`:

```ini
[Unit]
Description=EPS Proxy Service
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/eps-proxy
Environment="PATH=/opt/eps-proxy/venv/bin"
ExecStart=/opt/eps-proxy/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --workers 4

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable eps-proxy
sudo systemctl start eps-proxy
sudo systemctl status eps-proxy
```

### 4. Configure Nginx

Create `/etc/nginx/sites-available/eps-proxy`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/eps-proxy /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Cloud Platforms

### Railway

1. Connect your GitHub repo
2. Add environment variables in the dashboard
3. Railway auto-detects FastAPI and deploys

### Render

1. Create new Web Service
2. Connect repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables

### Heroku

Create `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

Deploy:
```bash
heroku create your-app-name
heroku config:set TOKEN=your_token USER_ID=your_id PASSWORD=your_password
git push heroku main
```

## Monitoring

View logs:
```bash
# Systemd
sudo journalctl -u eps-proxy -f

# Docker
docker-compose logs -f

# Direct
tail -f /var/log/eps-proxy.log
```

## Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "EPS Proxy",
  "env_configured": true
}
```
