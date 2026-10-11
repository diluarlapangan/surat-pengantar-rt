# 🚀 Panduan Deploy Surat Pengantar RT

## VPS yang Dipilih
- **Provider:** Helipod
- **Plan:** VPS S - EU
- **Region:** Germany
- **OS:** Ubuntu 24.04
- **Harga:** Rp 27.900/bulan
- **Spec:** 1 vCPU, 1 GB RAM, 15 GB SSD

## ⚠️ Catatan Penting
- RAM 1 GB cukup untuk Streamlit app ringan
- Storage 15 GB cukup jika tidak menyimpan PDF lama
- Region Germany → latency ~170ms ke Indonesia

## Langkah Deploy

### 1. Setup GitHub Repository
Push semua file ini ke GitHub:
```bash
git init
git add .
git commit -m "Initial deploy"
git branch -M main
git remote add origin https://github.com/USERNAME/surat-pengantar-rt.git
git push -u origin main
```

### 2. Setup VPS
Setelah VPS aktif, SSH ke server:
```bash
ssh root@YOUR_SERVER_IP
```

Copy paste command ini satu per satu:
```bash
# Update
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh
systemctl enable docker
systemctl start docker

# Install Git & curl
apt install -y git curl

# Clone repo
cd /opt
git clone https://github.com/USERNAME/surat-pengantar-rt.git
cd surat-pengantar-rt

# Build & run
docker compose up -d --build
```

### 3. Setup Domain
Di Sumopod DNS zone, tambahkan:
- **Type:** A Record
- **Name:** @
- **Value:** IP VPS Anda
- **TTL:** 3600

### 4. Setup SSL (HTTPS) - OPSIONAL
```bash
apt install -y certbot python3-certbot-nginx
# Setup nginx dulu sebagai reverse proxy, lalu:
# certbot --nginx -d diluarlapangan.my.id
```

Atau lebih sederhana: pakai **Caddy** untuk auto SSL.

### 5. Maintenance
```bash
# Restart app
cd /opt/surat-pengantar-rt
docker compose restart

# Update app
cd /opt/surat-pengantar-rt
git pull
docker compose down
docker compose up -d --build

# Lihat logs
docker compose logs -f
```

## Troubleshooting

### App tidak bisa diakses
```bash
ufw allow 80/tcp
ufw allow 443/tcp
```

### Docker tidak jalan
```bash
systemctl status docker
systemctl start docker
```

### RAM penuh
```bash
free -h
docker system prune -a
```
