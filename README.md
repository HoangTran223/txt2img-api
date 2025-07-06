# txt2img-api

## Chạy hoàn toàn trong Docker

1. Đảm bảo Docker Desktop đã chạy.
2. Build image:
   ```
   docker build -t txt2img-api .
   ```
3. Chạy container (không mount volume, không dùng `-v`):
   ```
   docker run -p 8000:8000 txt2img-api
   ```
4. Model sẽ được tải và lưu trong container, không chiếm dung lượng trên máy thật.
5. Khi xóa container/image, model cũng sẽ bị xóa theo.
