#!/bin/bash

echo "Testing all images..."
echo "====================="

# Test watches
echo -e "\n📁 WATCHES:"
curl -s -o /dev/null -w "rolex-submariner.jpg: %{http_code}\n" http://localhost:8000/frontend/static/images/products/watches/rolex-submariner.jpg
curl -s -o /dev/null -w "rolex-daytona.jpg: %{http_code}\n" http://localhost:8000/frontend/static/images/products/watches/rolex-daytona.jpg
curl -s -o /dev/null -w "omega-speedmaster.jpg: %{http_code}\n" http://localhost:8000/frontend/static/images/products/watches/omega-speedmaster.jpg
curl -s -o /dev/null -w "omega-seamaster.jpg: %{http_code}\n" http://localhost:8000/frontend/static/images/products/watches/omega-seamaster.jpg
curl -s -o /dev/null -w "tag-carrera.jpg: %{http_code}\n" http://localhost:8000/frontend/static/images/products/watches/tag-carrera.jpg

# Test gold
echo -e "\n📁 GOLD:"
curl -s -o /dev/null -w "gold-necklace.jpg: %{http_code}\n" http://localhost:8000/frontend/static/images/products/gold/gold-necklace.jpg
curl -s -o /dev/null -w "gold-bracelet.jpg: %{http_code}\n" http://localhost:8000/frontend/static/images/products/gold/gold-bracelet.jpg
curl -s -o /dev/null -w "gold-earrings.jpg: %{http_code}\n" http://localhost:8000/frontend/static/images/products/gold/gold-earrings.jpg

# Test diamond
echo -e "\n📁 DIAMOND:"
curl -s -o /dev/null -w "engagement-ring.jpg: %{http_code}\n" http://localhost:8000/frontend/static/images/products/diamond/engagement-ring.jpg
curl -s -o /dev/null -w "diamond-earrings.jpg: %{http_code}\n" http://localhost:8000/frontend/static/images/products/diamond/diamond-earrings.jpg
curl -s -o /dev/null -w "tennis-bracelet.jpg: %{http_code}\n" http://localhost:8000/frontend/static/images/products/diamond/tennis-bracelet.jpg

# Test banners
echo -e "\n📁 BANNERS:"
curl -s -o /dev/null -w "hero-banner.jpg: %{http_code}\n" http://localhost:8000/frontend/static/images/banners/hero-banner.jpg
curl -s -o /dev/null -w "about-hero.jpg: %{http_code}\n" http://localhost:8000/frontend/static/images/banners/about-hero.jpg
