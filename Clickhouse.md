# Clickhouse

OLAP

- Tables are “wide,” meaning they contain a large number of columns.
- Datasets are large and queries require high throughput when processing a single query (up to billions of rows per second per server).
- Column values are fairly small: numbers and short strings (for example, 60 bytes per URL).
- Queries extract a large number of rows, but only a small subset of columns.
- For simple queries, latencies around 50ms are allowed.
- There is one large table per query; all tables are small, except for one.
- A query result is significantly smaller than the source data. In other words, data is filtered or aggregated, so the result fits in a single server’s RAM.
- Queries are relatively rare (usually hundreds of queries per server or less per second).
- Inserts happen in fairly large batches (> 1000 rows), not by single rows.
- Transactions are not necessary.


- OLAP
- 列式存储：The values from different columns are stored separately, and data from the same column is stored together.
    
    相同列（字段）的值的在一个文件。列式存储为什么查询快？因为大多数情况下只是使用查询某几个列。

适用：
- 绝大多数读请求
- 
