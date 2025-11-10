# 🚀 Deployment Guide

Complete guide for deploying the Edge Detection System to Render (and other platforms).

---

## 📋 Prerequisites

- [x] GitHub account
- [x] Render account (free tier available)
- [x] Git installed locally
- [x] Project code ready

---

## 🌐 Deploy to Render (Recommended)

### Method 1: One-Click Deploy (Easiest)

1. **Push to GitHub**
   ```bash
   cd d:\edgedetection
   git init
   git add .
   git commit -m "Initial commit - Edge Detection System"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/edge-detection.git
   git push -u origin main
   ```

2. **Connect to Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml`

3. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy
   - Your app will be live at: `https://edge-detection-api.onrender.com`

### Method 2: Manual Configuration

1. **Create New Web Service on Render**
   - Name: `edge-detection-api`
   - Environment: `Python 3`
   - Branch: `main`

2. **Build Command**
   ```bash
   pip install -r requirements-web.txt
   ```

3. **Start Command**
   ```bash
   gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 app:app
   ```

4. **Environment Variables** (optional)
   - `PYTHON_VERSION`: `3.11.0`
   - `PORT`: Auto-configured by Render

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for initial build

---

## 🐳 Deploy with Docker

### Build Docker Image

```bash
docker build -t edge-detection-api .
```

### Run Locally

```bash
docker run -p 5000:5000 edge-detection-api
```

### Deploy to Docker Hub

```bash
docker tag edge-detection-api YOUR_USERNAME/edge-detection-api
docker push YOUR_USERNAME/edge-detection-api
```

### Deploy to Cloud Platforms

**AWS ECS, Google Cloud Run, Azure Container Instances:**
- Use the Docker image from Docker Hub
- Configure port 5000
- Set health check to `/api/health`

---

## ☁️ Deploy to Other Platforms

### Heroku

1. **Create `Procfile`**
   ```
   web: gunicorn --bind 0.0.0.0:$PORT app:app
   ```

2. **Deploy**
   ```bash
   heroku create edge-detection-api
   heroku buildpacks:set heroku/python
   git push heroku main
   ```

### Railway

1. **Connect GitHub repo**
2. **Railway auto-detects Python**
3. **Set start command**: Same as Render

### Vercel (Serverless)

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   vercel --prod
   ```

### AWS EC2

1. **Launch Ubuntu instance**
2. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv libgl1-mesa-glx
   ```

3. **Clone and setup**
   ```bash
   git clone YOUR_REPO
   cd edge-detection
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements-web.txt
   ```

4. **Run with systemd**
   ```bash
   sudo nano /etc/systemd/system/edge-detection.service
   ```
   ```ini
   [Unit]
   Description=Edge Detection API
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/edge-detection
   Environment="PATH=/home/ubuntu/edge-detection/venv/bin"
   ExecStart=/home/ubuntu/edge-detection/venv/bin/gunicorn --bind 0.0.0.0:5000 app:app

   [Install]
   WantedBy=multi-user.target
   ```

---

## 🔧 Configuration

### Environment Variables

Create `.env` file (for local development):

```env
FLASK_ENV=production
PORT=5000
LOG_LEVEL=INFO
MAX_UPLOAD_SIZE=16777216
```

### config.yaml

Adjust settings in `config.yaml`:

```yaml
web:
  host: "0.0.0.0"
  port: 5000
  debug: false
  max_upload_size: 16777216
```

---

## ✅ Post-Deployment Checklist

- [ ] Access your app URL
- [ ] Test health endpoint: `https://your-app.com/api/health`
- [ ] Upload a test image through the web interface
- [ ] Verify all edge detection algorithms work
- [ ] Check response times (should be < 5 seconds)
- [ ] Monitor logs for errors
- [ ] Set up SSL/HTTPS (auto on Render)
- [ ] Configure custom domain (optional)

---

## 📊 Monitoring

### Check Application Health

```bash
curl https://your-app.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Edge Detection API",
  "version": "1.0.0"
}
```

### View Logs on Render

1. Go to Render Dashboard
2. Select your service
3. Click "Logs" tab
4. Monitor real-time logs

---

## 🔒 Security

### Production Checklist

- [x] Debug mode disabled (`debug: false`)
- [x] File size limits enforced
- [x] File type validation
- [x] CORS configured
- [x] HTTPS enabled
- [ ] Rate limiting (add if needed)
- [ ] API authentication (add if needed)

### Add Rate Limiting (Optional)

Install:
```bash
pip install flask-limiter
```

Add to `app.py`:
```python
from flask_limiter import Limiter
limiter = Limiter(app, default_limits=["100 per hour"])
```

---

## 🎯 Performance Optimization

### For Render Free Tier

- Service sleeps after 15 mins of inactivity
- First request after sleep takes ~30 seconds
- Use Render's paid plan for always-on service

### Optimization Tips

1. **Reduce image size** before processing
2. **Use caching** for common images
3. **Optimize OpenCV operations**
4. **Enable CDN** for static files

---

## 🐛 Troubleshooting

### Build Fails

**Issue**: Missing dependencies
```bash
# Solution: Check requirements-web.txt
pip install -r requirements-web.txt
```

### App Not Starting

**Issue**: Port binding
```bash
# Ensure app binds to 0.0.0.0:$PORT
gunicorn --bind 0.0.0.0:$PORT app:app
```

### 502 Bad Gateway

**Issue**: App crashed or timeout
- Check logs in Render dashboard
- Increase timeout: `--timeout 120`
- Check memory usage

### Image Upload Fails

**Issue**: File size limit
- Increase `MAX_CONTENT_LENGTH`
- Check Render plan limits

---

## 🔄 CI/CD Pipeline

GitHub Actions automatically:
- ✅ Runs tests on push
- ✅ Checks code quality
- ✅ Builds Docker image
- ✅ Reports coverage

### Trigger Deployment

```bash
git add .
git commit -m "Update feature"
git push origin main
# Render auto-deploys on push
```

---

## 📱 Access Your Deployed App

**Your App URLs:**

- **Main Interface**: `https://edge-detection-api.onrender.com`
- **Health Check**: `https://edge-detection-api.onrender.com/api/health`
- **API Docs**: `https://edge-detection-api.onrender.com/api/algorithms`

### Test API with cURL

```bash
curl -X POST \
  https://your-app.onrender.com/api/detect \
  -F "image=@test.jpg" \
  -F "sobel_kernel=3" \
  -F "canny_threshold1=50" \
  -F "canny_threshold2=150"
```

---

## 📈 Scaling

### Render Scaling Options

1. **Free Tier**: 750 hours/month, sleeps after inactivity
2. **Starter ($7/mo)**: Always on, 512MB RAM
3. **Standard ($25/mo)**: 2GB RAM, better performance

### Upgrade Command

Go to Render Dashboard → Select Service → Settings → Change Plan

---

## 🎉 Success!

Your Edge Detection System is now deployed and accessible worldwide!

**Next Steps:**
1. Share your app URL
2. Add to portfolio/resume
3. Monitor usage and performance
4. Add more features
5. Collect user feedback

---

## 📞 Support

**Issues?** Check:
1. [Render Documentation](https://render.com/docs)
2. [GitHub Issues](https://github.com/YOUR_USERNAME/edge-detection/issues)
3. Application logs in Render dashboard

**Need Help?** 
- Review `README.md` for project details
- Check `HOW_TO_USE.md` for usage instructions
- See `PROJECT_INFO.md` for technical details

---

**🚀 Happy Deploying!**
