#!/bin/bash

set -e

echo "=== Setting up Nginx Reverse Proxy ==="
echo ""

if ! command -v nginx &> /dev/null; then
    echo "Installing nginx..."
    if command -v yum &> /dev/null; then
        sudo yum update -y
        sudo yum install -y nginx
    elif command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y nginx
    else
        echo "Error: Cannot detect package manager. Please install nginx manually."
        exit 1
    fi
else
    echo "Nginx is already installed."
fi

echo ""
echo "Creating nginx configuration..."

PROJECT_DIR="/home/ec2-user/DataCompression/lossy-vae"
NGINX_CONFIG="/etc/nginx/conf.d/lossy-vae.conf"

sudo cp "$PROJECT_DIR/nginx_config.conf" "$NGINX_CONFIG"

echo "Configuration file created at: $NGINX_CONFIG"
echo ""

echo "Testing nginx configuration..."
sudo nginx -t

if [ $? -eq 0 ]; then
    echo ""
    echo "[OK] Nginx configuration is valid!"
    echo ""
    echo "Starting nginx..."
    sudo systemctl enable nginx
    sudo systemctl restart nginx
    
    echo ""
    echo "=== Setup Complete! ==="
    echo ""
    echo "Nginx is now configured to proxy port 80 to your Flask app on port 5000."
    echo ""
    echo "To check nginx status:"
    echo "  sudo systemctl status nginx"
    echo ""
    echo "To view nginx logs:"
    echo "  sudo tail -f /var/log/nginx/error.log"
    echo ""
    echo "Your web app will be accessible at:"
    echo "  http://YOUR_EC2_PUBLIC_IP"
    echo ""
    echo "Make sure:"
    echo "  1. Port 80 is open in your AWS security group"
    echo "  2. Your Flask app is running: python web_demo.py"
    echo ""
else
    echo ""
    echo "[ERROR] Nginx configuration test failed!"
    echo "Please check the configuration file: $NGINX_CONFIG"
    exit 1
fi

