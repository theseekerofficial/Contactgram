# 🔐 Cloudflare Origin SSL Setup Guide for NGINX

This guide walks you through setting up a secure Cloudflare Origin Certificate with NGINX.

---

## 1. 📁 Generate Origin Certificate from Cloudflare

1. Go to: [dash.cloudflare.com](https://dash.cloudflare.com) > **Your Domain** > **SSL/TLS** > **Origin Server**
2. Create a certificate with:

   * **Private key type**: ECC
   * **Certificate validity**: 15 Years
3. Save the outputs:

   * `-----BEGIN CERTIFICATE----- ...` → save as `cloudflare_origin.pem`
   * `-----BEGIN PRIVATE KEY----- ...` → save as `cloudflare_origin.key`

---

## 2. 💾 Transfer Certs to Server

Move the files to appropriate secure locations:

```bash
sudo mv cloudflare_origin.pem /etc/ssl/certs/
sudo mv cloudflare_origin.key /etc/ssl/private/
```

---

## 3. 🛡️ Set Secure Permissions

```bash
sudo chmod 644 /etc/ssl/certs/cloudflare_origin.pem
sudo chmod 600 /etc/ssl/private/cloudflare_origin.key
```

---

## 4. ⬇️ Download Cloudflare CA Cert

```bash
sudo curl -o /etc/ssl/certs/cloudflare_ca.pem \
  https://developers.cloudflare.com/ssl/static/authenticated_origin_pull_ca.pem
```

---

## 5. ✍️ Add NGINX Configuration

Paste the content from your `contactgram.nginx` config file into your NGINX site config.
Make sure it includes the certificate and key paths.

---

## 6. 📆 Test NGINX Configuration

```bash
sudo nginx -t
```

---

## 7. ↺ Reload NGINX

```bash
sudo systemctl reload nginx
```

---

## 📆 Side Notes

### ✅ Ensure Ports 80 and 443 Are Open

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw reload
```

### ☁️ Cloudflare DNS Settings

* `your-domain.com` should be **proxied** (orange cloud icon).
* TTL: **Auto** (Cloudflare will handle it optimally).

### 🔒 Enable Full (Strict) SSL Mode

* Navigate to: `Cloudflare Dashboard → SSL/TLS → Overview`
* Set SSL mode to: **Full (strict)**

---

> You're now ready to serve HTTPS traffic securely using Cloudflare and NGINX. ✨
