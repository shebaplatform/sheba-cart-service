docker rm -f cart_service
docker run -itd -p 8000:8000 --name cart_service --network keycloak-production_keycloak-network -v $(pwd):/app -w /app cart_service