# Reflection — Lab 19

**Tên:** Dang Minh Hai  
**Cohort:** A20  
**Path đã chạy:** docker

---

## Câu hỏi (≤ 200 chữ)

Trên golden set 50 queries, hybrid thắng rõ nhất ở nhóm `mixed` vì nó vừa giữ được tín hiệu lexical từ BM25 vừa bù được ngữ nghĩa từ vector search. Kết quả của mình là hybrid đạt `99.5%` ở `mixed`, cao hơn keyword `98.0%` và semantic `89.0%`. Ở `exact`, BM25 vẫn rất mạnh vì query khớp từ khóa trực tiếp; ở `paraphrase`, vector search thường hữu ích hơn vì query không chứa literal keyword, nhưng hybrid của mình vẫn không luôn thắng nếu lexical signal làm nhiễu nhẹ. Mình sẽ **không dùng hybrid** khi cần latency thấp nhất tuyệt đối, corpus nhỏ và query rất chính xác theo từ khóa, hoặc khi toàn bộ traffic là paraphrase thuần và vector-only đã đủ tốt, vì hybrid thêm chi phí tính toán nhưng không luôn tạo lợi ích tương xứng.

---

## Điều ngạc nhiên nhất khi làm lab này

Phần khó nhất không phải viết logic search, mà là làm cho cả Docker Feast + Postgres + Redis chạy ổn định cùng một bộ dữ liệu reproducible.

---

## Bonus challenge

- [ ] Đã làm bonus (xem `bonus/`)
- [ ] Pair work với: _<tên đồng đội nếu có>_
