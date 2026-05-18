---
name: rag-pipeline
description: 新增、修改、调试或评估 RAG 摄取、切分、embedding、向量库、检索过滤、reranking、上下文组装、引用来源或答案生成时使用。该 Skill 保持检索行为可观测、受权限控制、可测试且基于来源。
---

# RAG Pipeline Skill

## 适用场景

- 新增文档摄取、解析、清洗、切分或索引流程。
- 修改 embedding 模型、向量库、检索过滤、排序或 reranking。
- 调整上下文拼接、引用来源、答案合成 prompt 或生成策略。
- 排查检索缺失、召回差、幻觉、来源错误或权限越界。
- 为 RAG 行为补充测试、评估或观测指标。

## 必须读取

1. `AGENTS.md`
2. `.harness/rules/coding-rules.md`
3. `.harness/rules/testing-rules.md`
4. `.harness/rules/security-rules.md`
5. `docs/architecture/overview.md`
6. 相关 `docs/domain/` 和 `docs/architecture/`
7. 现有摄取、向量、检索、生成和测试代码

## RAG 边界

- Loading：读取文件、网页、数据库或第三方来源。
- Parsing：结构化解析、清洗、去噪和元数据提取。
- Chunking：切分策略、重叠、标题层级、表格和代码块处理。
- Embedding：模型、维度、批处理、重试和缓存。
- Indexing：向量写入、去重、版本、租户和权限元数据。
- Retrieval：query 生成、过滤、召回数量、排序和 reranking。
- Context assembly：去重、截断、来源保留和 token 预算。
- Generation：prompt、引用、拒答、空结果和错误处理。
- Evaluation：golden set、召回率、引用准确性和失败样本。

## 工作流程

1. 明确变更影响的是摄取、索引、检索、上下文还是生成。
2. 检查访问控制：检索前和检索后都不能越权使用文档。
3. 设计可观测元数据：document id、chunk id、source、tenant、version、score、filter。
4. 实现最小改动，保持 pipeline 阶段边界清晰。
5. 对空结果、低置信度、重复 chunk、无来源和工具失败设计行为。
6. 补测试或评估样例，覆盖成功检索、无结果、权限过滤和来源归因。
7. 运行聚焦验证，并记录影响召回或生成质量的剩余风险。

## 质量门禁

- 不把检索、展示、生成和持久化混在一个大函数中。
- 不在向量元数据或 prompt 中存储密钥、凭据或不必要隐私。
- 来源归因要求存在时，不静默丢弃来源。
- LLM 输出不能直接作为权限、SQL、shell 或文件路径参数。
- 检索过滤必须结构化，不拼接用户可控 DSL。
- 评估要包含失败样本，不只验证 happy path。

## 验证命令

```bash
make test
make check
```

可按项目补充 RAG 专项评估命令，例如：

```bash
uv run pytest tests/test_rag_*.py -q
```

## 输出格式

```text
RAG 阶段：
- ...

核心改动：
- ...

访问控制和来源：
- ...

测试或评估：
- ...

验证命令：
- ...

剩余风险：
- ...
```
