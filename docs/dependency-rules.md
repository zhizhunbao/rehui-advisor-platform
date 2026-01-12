---
inclusion: always
---

# 依赖规则

## 模块依赖层级

```
Level 3: Domain Modules (领域模块)
         flight, hotel, job, car, house, insurance, education, investment
                              │
                              ▼
Level 2: Feature Modules (功能模块)
         advisor, search, recommendation, data-pipeline
                              │
                              ▼
Level 1: Core Modules (核心模块)
         auth, common, layout
```

## 依赖规则

### 规则 1: 单向依赖

模块只能依赖同级或更低级别的模块。

```typescript
// ✅ 正确：领域模块依赖功能模块
import { SearchService } from "../../search/service";

// ❌ 错误：核心模块依赖领域模块
import { FlightService } from "../../flight/service"; // 禁止！
```

### 规则 2: 领域模块隔离

领域模块之间不能直接依赖。

```typescript
// ❌ 错误
import { HotelService } from "../../hotel/service"; // 禁止！

// ✅ 正确：通过功能模块间接通信
import { RecommendationService } from "../../recommendation/service";
```

### 规则 3: Common 模块可被任意依赖

```typescript
// ✅ 任何模块都可以依赖 common
import { BaseError } from "../../common/errors";
import { formatDate } from "../../common/utils";
```

### 规则 4: 层内依赖方向

```
Controller → Service → Repository
```

```typescript
// ✅ 正确
// Controller 依赖 Service
import { FlightService } from "../service";

// Service 依赖 Repository
import { FlightRepository } from "../repository";

// ❌ 错误：Controller 直接依赖 Repository
import { FlightRepository } from "../repository"; // 禁止！
```

### 规则 5: 禁止循环依赖

```typescript
// ❌ 错误：循环依赖
// a/service.ts → b/service.ts → a/service.ts

// ✅ 正确：提取共享逻辑到 common
import { SharedService } from "../common/service";
```

## 依赖矩阵

| 依赖方 ↓ / 被依赖方 → | common | auth | advisor | search | flight | hotel |
| --------------------- | :----: | :--: | :-----: | :----: | :----: | :---: |
| common                |   -    |  ❌  |   ❌    |   ❌   |   ❌   |  ❌   |
| auth                  |   ✅   |  -   |   ❌    |   ❌   |   ❌   |  ❌   |
| advisor               |   ✅   |  ✅  |    -    |   ❌   |   ❌   |  ❌   |
| search                |   ✅   |  ✅  |   ❌    |   -    |   ❌   |  ❌   |
| flight                |   ✅   |  ✅  |   ✅    |   ✅   |   -    |  ❌   |
| hotel                 |   ✅   |  ✅  |   ✅    |   ✅   |   ❌   |   -   |

✅ = 允许依赖 | ❌ = 禁止依赖
