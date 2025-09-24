run core:
1. cd core_ai_service
2. docker build --secret id=openai_api_key,src=./core_ai_service/.env -t text-to-sql-core-ai ./core_ai_service
3. docker run -p 8000:8000 -d --name ai_service --env-file ./core_ai_service/.env text-to-sql-core-ai


Kiểm tra API:
Mở một terminal khác và dùng curl để gửi yêu cầu: 
curl -X POST "http://localhost:8000/generate-sql" \
-H "Content-Type: application/json" \

examples:
    How many artists are there?
    Show me top 5 artists by sales