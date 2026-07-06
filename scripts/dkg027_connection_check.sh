#!/bin/bash

echo "🌐 DKG-027: Frontend ↔ Backend API Connection Check"
echo ""

echo "1. Docker services:"
docker compose ps
echo ""

echo "2. Check frontend from host:"
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
echo "Frontend HTTP status: $FRONTEND_STATUS"
echo ""

echo "3. Check backend from host:"
API_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs)
echo "Backend /docs HTTP status: $API_STATUS"
echo "Note: 200 or 401 both mean backend is reachable."
echo ""

echo "4. Check frontend container can reach backend container:"
docker compose exec -T frontend sh -lc 'wget -q --server-response --spider http://api:8000/docs 2>&1 | head -20' || true
echo ""

echo "5. Check frontend env:"
docker compose exec -T frontend sh -lc 'echo NEXT_PUBLIC_DKG_API=$NEXT_PUBLIC_DKG_API' || true
echo ""

echo "6. Result guide:"
echo "✔ Frontend 200 = UI reachable"
echo "✔ Backend 200/401 = API reachable"
echo "✔ frontend → api response 200/401 = Docker network OK"
echo "✔ NEXT_PUBLIC_DKG_API visible = frontend config OK"
echo ""
echo "If backend returns 401, connection is OK but auth is blocking unauthenticated requests."
