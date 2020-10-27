# Protocal Buffers

## Message

```
syntax = "proto3"; 

message SearchRequest {
  string query = 1;
  int32 page_number = 2;
  int32 result_per_page = 3;
}
```

必须以syntax为第一行。
每个field要有一个唯一的数字，最小是1，1到15用1byte编码，16到2047用2byte。