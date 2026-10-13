# Cloudflare DNS & SSL Configuration Guide

## 1. DNS Setup
- Change nameservers at your domain registrar to the Cloudflare nameservers provided during setup.
- Add an `A` record pointing to your server's public IP address.
- Ensure the proxy status (orange cloud) is turned **ON** for DDoS protection and caching.

## 2. SSL/TLS Configuration
- Navigate to **SSL/TLS -> Overview**.
- Set the encryption mode to **Full (strict)**.
- Generate an Origin Certificate in Cloudflare (SSL/TLS -> Origin Server) and install it on your Nginx server, or use Let's Encrypt on your origin server.
- Enable **Always Use HTTPS** in **SSL/TLS -> Edge Certificates**.

## 3. WAF Rules Recommendations
- Navigate to **Security -> WAF -> Custom Rules**.
- Create rules to challenge or block requests from known bad IPs or anomalous traffic patterns.
- Restrict access to backend administrative endpoints (`/api/admin/*`) based on IP if possible.
- Enable Cloudflare's managed rulesets (if available on your plan).

## 4. DDoS Protection Notes
- Cloudflare automatically provides unmetered DDoS mitigation.
- Under **Security -> Settings**, you can toggle the "Security Level" to **High** or enable **I'm Under Attack Mode** if you experience an active attack.
- Rate limiting (if available) should be configured on sensitive endpoints like login and registration (`/api/auth/*`).

## 5. Page Rules for Caching
- Navigate to **Rules -> Page Rules**.
- Add a rule for your static assets:
  - URL: `*yourdomain.com/assets/*` (or wherever static files are served)
  - Setting: **Cache Level: Cache Everything**
  - Setting: **Edge Cache TTL: a month**

## 6. Development Mode
- If you are making frequent changes and need to bypass the cache, enable **Development Mode** under **Caching -> Configuration**.
- Remember to turn it off when done, as it automatically disables itself after 3 hours.
