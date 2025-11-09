# Nginx Reverse Proxy Setup

This guide will help you set up nginx to proxy port 80 to your Flask app running on port 5000.

## Quick Setup

### Option 1: Automated Script (Recommended)

```bash
cd /home/ec2-user/DataCompression/lossy-vae
chmod +x setup_nginx.sh
./setup_nginx.sh
```

This script will:
- Install nginx (if not already installed)
- Create the configuration file
- Test the configuration
- Start and enable nginx

### Option 2: Manual Setup

#### Step 1: Install Nginx

**On Amazon Linux / CentOS:**
```bash
sudo yum update -y
sudo yum install -y nginx
```

**On Ubuntu / Debian:**
```bash
sudo apt-get update
sudo apt-get install -y nginx
```

#### Step 2: Copy Configuration File

```bash
cd /home/ec2-user/DataCompression/lossy-vae
sudo cp nginx_config.conf /etc/nginx/conf.d/lossy-vae.conf
```

#### Step 3: Test Configuration

```bash
sudo nginx -t
```

If you see "syntax is ok" and "test is successful", you're good to go!

#### Step 4: Start Nginx

```bash
sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl status nginx
```

## Verify Setup

1. **Make sure your Flask app is running:**
   ```bash
   python web_demo.py
   ```

2. **Check nginx is running:**
   ```bash
   sudo systemctl status nginx
   ```

3. **Test the connection:**
   ```bash
   curl http://localhost
   ```

4. **Access from browser:**
   Open `http://YOUR_EC2_PUBLIC_IP` in your browser

## AWS Security Group Configuration

Make sure port 80 (HTTP) is open in your security group:

1. Go to EC2 Console → Security Groups
2. Select your instance's security group
3. Edit Inbound Rules
4. Add rule:
   - Type: HTTP
   - Protocol: TCP
   - Port: 80
   - Source: 0.0.0.0/0 (or your IP for security)

## Troubleshooting

### Nginx won't start

Check the error log:
```bash
sudo tail -f /var/log/nginx/error.log
```

Common issues:
- Port 80 already in use: `sudo lsof -i :80`
- Configuration syntax error: `sudo nginx -t`
- Permission issues: Make sure nginx config files are readable

### 502 Bad Gateway

This means nginx can't connect to your Flask app. Check:

1. **Is Flask app running?**
   ```bash
   ps aux | grep web_demo.py
   ```

2. **Is Flask listening on port 5000?**
   ```bash
   netstat -tlnp | grep 5000
   ```

3. **Check Flask app logs** for errors

### 403 Forbidden

Check file permissions:
```bash
sudo chmod 644 /etc/nginx/conf.d/lossy-vae.conf
```

### Connection Refused

Make sure Flask app is binding to `0.0.0.0` (not just `127.0.0.1`). The `web_demo.py` already does this correctly.

## Useful Commands

```bash
# Restart nginx
sudo systemctl restart nginx

# Reload configuration (without downtime)
sudo nginx -s reload

# Stop nginx
sudo systemctl stop nginx

# View nginx access logs
sudo tail -f /var/log/nginx/access.log

# View nginx error logs
sudo tail -f /var/log/nginx/error.log

# Check nginx status
sudo systemctl status nginx

# Test configuration
sudo nginx -t
```

## Running Flask App as a Service (Optional)

For production, you might want to run Flask as a systemd service so it starts automatically:

### Create service file:

```bash
sudo nano /etc/systemd/system/lossy-vae.service
```

Add this content:

```ini
[Unit]
Description=Lossy-VAE Web Demo
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/DataCompression/lossy-vae
Environment="PATH=/home/ec2-user/.local/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/bin/python3 /home/ec2-user/DataCompression/lossy-vae/web_demo.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable lossy-vae
sudo systemctl start lossy-vae
sudo systemctl status lossy-vae
```

Now both nginx and Flask will start automatically on boot!

## Security Considerations

For production use, consider:

1. **Add SSL/TLS** (Let's Encrypt with certbot)
2. **Restrict access** by IP in security group
3. **Use firewall** (firewalld or ufw)
4. **Rate limiting** in nginx config
5. **Disable server tokens** in nginx

## Testing

After setup, test your setup:

```bash
# Test locally
curl http://localhost

# Test from another machine
curl http://YOUR_EC2_PUBLIC_IP
```

You should see the HTML of your web interface!

## Summary

✅ Nginx installed and configured  
✅ Port 80 → Port 5000 proxy set up  
✅ Flask app accessible via HTTP  
✅ Ready for your faculty presentation!

Your web demo is now accessible at `http://YOUR_EC2_PUBLIC_IP` (no port number needed!)

