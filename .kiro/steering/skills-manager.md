---
inclusion: always
---

# Skills Manager

根据用户意图匹配 `backend/scripts/data/skills/` 下的 SKILL.md 文档。

## 开发相关

| 关键词                                          | Skill                    |
| ----------------------------------------------- | ------------------------ |
| discover, 发现, 资源发现, 评测, benchmark, 选型 | `dev-resource_discovery` |

## AI 技术

| 关键词                             | Skill           |
| ---------------------------------- | --------------- |
| agent, 智能体, AI agent, 框架选型  | `ai-agents`     |
| prompt, 提示词, prompt engineering | `ai-prompts`    |
| skill, claude skill                | `ai-skills`     |
| llm, 大模型, 语言模型              | `ai-llm_models` |

## AI 学习

| 关键词                               | Skill                              |
| ------------------------------------ | ---------------------------------- |
| 机器学习, ML, machine learning       | `ai_learning-ml`                   |
| 深度学习, DL, deep learning          | `ai_learning-dl`                   |
| LLM学习, 大模型学习                  | `ai_learning-llm`                  |
| NLP, 自然语言处理                    | `ai_learning-nlp`                  |
| 机器视觉, MV, machine vision, CV     | `ai_learning-mv`, `ai_learning-cv` |
| RAG, 检索增强                        | `ai_learning-rag`                  |
| 强化学习, RL, reinforcement learning | `ai_learning-rl`                   |

## 职业发展

| 关键词                 | Skill                     |
| ---------------------- | ------------------------- |
| 简历, resume, CV       | `career-resume`           |
| 面试, interview        | `career-interview`        |
| 求职, job search       | `career-job_search`       |
| 认证, certification    | `career-certification`    |
| 创业, entrepreneurship | `career-entrepreneurship` |

## 移民身份

| 关键词            | Skill                                                |
| ----------------- | ---------------------------------------------------- |
| 签证, visa        | `identity-visa`, `immigration-visa_renewal`          |
| PR, 永居, 移民    | `immigration-pr_application`                         |
| 工签, work permit | `immigration-work_permit`                            |
| 入籍, citizenship | `immigration-citizenship`                            |
| 家庭团聚, 担保    | `immigration-family_sponsorship`                     |
| SSN, 社保号       | `identity-ssn`                                       |
| 驾照              | `identity-driving`, `transportation-driving_license` |

## 金融财务

| 关键词              | Skill                 |
| ------------------- | --------------------- |
| 银行, banking       | `finance-banking`     |
| 信用卡, credit card | `finance-credit_card` |
| 保险                | `finance-insurance`   |
| 投资, investment    | `finance-investment`  |
| 汇款, remittance    | `finance-remittance`  |
| 报税, tax           | `finance-tax`         |

## 住房

| 关键词            | Skill                 |
| ----------------- | --------------------- |
| 租房, rental      | `housing-rental`      |
| 买房, home buying | `housing-home_buying` |
| 搬家, moving      | `housing-moving`      |
| 家具, furniture   | `housing-furniture`   |
| 水电煤, utilities | `housing-utilities`   |

## 交通出行

| 关键词               | Skill                           |
| -------------------- | ------------------------------- |
| 买车, car buying     | `transportation-car_buying`     |
| 车险, car insurance  | `transportation-car_insurance`  |
| 公交, public transit | `transportation-public_transit` |
| 机票, flight         | `transportation-flight`         |

## 医疗健康

| 关键词                     | Skill                         |
| -------------------------- | ----------------------------- |
| 家庭医生, family doctor    | `healthcare-family_doctor`    |
| 看病, clinic               | `healthcare-clinic_visit`     |
| 药房, pharmacy             | `healthcare-pharmacy`         |
| 医疗保险, health insurance | `healthcare-health_insurance` |
| 心理健康, mental health    | `healthcare-mental_health`    |
| 托儿, childcare            | `healthcare-childcare`        |

## 教育

| 关键词                      | Skill                             |
| --------------------------- | --------------------------------- |
| 选校, school selection      | `education-school_selection`      |
| 学历认证, credential        | `education-credential_evaluation` |
| 语言学习, language learning | `education-language_learning`     |
| 培训, skill training        | `education-skill_training`        |
| 补习, tutoring              | `education-tutoring`              |
| 子女教育, child education   | `education-child_education`       |

## 使用方式

匹配到关键词后，读取对应 SKILL.md：

```
backend/scripts/data/skills/{skill-name}/SKILL.md
```

如有 `references/` 子目录，按需读取详细文档。
