curl -X POST http://localhost:5000/search -H "Content-Type: application/json" --data-binary "{\"query\": \"Quien es Mobbel?\"}"

curl -X DELETE http://localhost:5000/resources/67d7c1c81853b415f3867d4f

curl -X DELETE http://localhost:5000/resources

curl -X POST http://localhost:5000/resources -H "Content-Type: application/json" -d "{\"pdf_path\": \"C:\\Users\\USUARIO\\Desktop\\Sergio\\Docs-trabajo\\Dossier-Mobbeel 2025.pdf\"}"
curl -X POST http://localhost:5000/resources -H "Content-Type: application/json" -d "{\"pdf_path\": \"C:\\Users\\USUARIO\\Desktop\\Sergio\\Docs-trabajo\\Dossier MobbSign 2025.pdf\"}"
curl -X POST http://localhost:5000/resources -H "Content-Type: application/json" -d "{\"pdf_path\": \"C:\\Users\\USUARIO\\Desktop\\Sergio\\Docs-trabajo\\Dossier MobbID 2025.pdf\"}"
curl -X POST http://localhost:5000/resources -H "Content-Type: application/json" -d "{\"pdf_path\": \"C:\\Users\\USUARIO\\Desktop\\Sergio\\Docs-trabajo\\Dossier MobbScan 2025.pdf\"}"

