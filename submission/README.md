# Day 19 Lab Submission Notes

Mình làm lab này theo **Docker full path** để bám đúng yêu cầu đề:

```bash
bash setup-docker.sh
make benchmark
make api
make lab
```

## Mục tiêu của lab

Lab này kết hợp 2 lớp hệ thống:

1. **Vector store** để làm semantic search và hybrid retrieval.
2. **Feature store** để quản lý feature online/offline bằng Feast.

Mục tiêu cuối cùng là hoàn thành đủ 4 notebook theo rubric:

- `01_embeddings_index`
- `02_hybrid_search_rrf`
- `03_search_api_benchmark`
- `04_feast_feature_store`

## Mình đã làm gì

### 1. Đồng bộ môi trường Docker

Mình giữ Docker stack đúng tinh thần production:

```bash
docker compose up -d
```

Trong repo này:

- Qdrant chạy server mode
- Redis làm online store
- Postgres làm offline store
- Port Postgres được dời sang `15432` để tránh đụng máy local

### 2. Notebook 1: embeddings + index

Notebook 1 tạo index cho 1000 document trong corpus và kiểm tra top-5 result cho query tiếng Việt.

Ý chính:

```python
embedder = make_embedder()
vectors = embedder.embed_documents(texts)
```

Mình dùng adapter `embed_documents()` / `embed_query()` để code chạy ổn ở cả lite lẫn docker.

### 3. Notebook 2: hybrid search bằng RRF

Notebook 2 triển khai hybrid search theo công thức RRF:

```python
score += 1 / (k + rank)
```

Mình kiểm tra cả:

- Precision@10 trung bình
- bảng theo slice `exact` / `paraphrase` / `mixed`

### 4. Notebook 3: FastAPI benchmark

Notebook 3 dựng endpoint `/search` và đo P50 / P95 / P99 cho 3 mode.

Kết quả benchmark cuối:

- Keyword: P99 `1.4ms`
- Semantic: P99 `12.0ms`
- Hybrid: P99 `17.6ms`

### 5. Notebook 4: Feast feature store

Notebook 4 dùng Feast để:

- `feast apply`
- `materialize-incremental`
- `get_online_features()`
- `get_historical_features()` cho PIT join

Mình tạo 3 feature views:

- `user_profile_features`
- `item_popularity_features`
- `query_velocity_features`

## Điểm đáng chú ý

- Mình thêm loader `.env` để notebook và app đọc config cùng một nguồn.
- Mình tách cấu hình Feast thành script render để chuyển giữa lite và docker sạch hơn.
- Mình giữ repo đi theo **Docker full path** nhưng vẫn để lite path tồn tại cho người chấm muốn chạy nhanh.

## Kết quả benchmark

```text
Keyword (BM25)   :  78.2%
Semantic (vector):  76.8%
Hybrid (RRF=60)  :  82.4%
```

Hybrid thắng cả keyword lẫn semantic, nên đạt đúng hướng rubric.

## Screenshot

Ảnh minh chứng nằm trong:

```text
submission/screenshots/
```

## Ghi chú cuối

Nếu muốn chạy lại từ đầu:

```bash
docker compose down
bash setup-docker.sh
make benchmark
```
