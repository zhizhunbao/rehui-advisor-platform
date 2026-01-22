---
inclusion: always
---

# Skills Manager

When user queries match keywords below, proactively load the corresponding SKILL.md from `backend/scripts/data/skills/{skill-name}/SKILL.md` to provide specialized guidance.

## Keyword Matching Rules

- Match keywords in both **English** and **Chinese (中文)**
- Support **partial matches** and related terms
- When multiple skills match, **prioritize the most specific one**
- If uncertain, **ask user to clarify** which skill domain they need

---

## 🛠️ Development

| Keywords                                                                                                                                                                                                                                           | Skill                    |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| discover, 发现, resource discovery, 资源发现, evaluation, 评测, benchmark, selection, 选型                                                                                                                                                         | `dev-resource_discovery` |
| code standards, 代码规范, naming conventions, 命名规范, directory structure, 目录结构, refactor, 重构, code organization, 代码组织, project structure, 项目结构                                                                                    | `dev-code_standards`     |
| code style, 代码风格, formatting, 格式化, linter, lint, prettier, eslint, ruff, black, type check, 类型检查, pre-commit                                                                                                                            | `dev-code_style`         |
| web scraping, 网页抓取, 爬虫, crawler, playwright, selenium, beautifulsoup, data extraction, 数据提取, anti-bot, 反爬虫, browser automation, 浏览器自动化                                                                                          | `dev-web_scraping`       |
| pdf, PDF, extract, 提取, convert, 转换, markdown, bilingual, 双语, 中英文, translation, 翻译, academic, 学术, paper, 论文, slides, 课件                                                                                                            | `dev-pdf_processing`     |
| translation, 翻译, technical translation, 技术翻译, bilingual documentation, 双语文档, terminology, 术语, localization, 本地化, i18n                                                                                                               | `dev-translation`        |
| document review, 文档审查, documentation quality, 文档质量, consistency check, 一致性检查, accuracy, 准确性, readability, 可读性, technical writing, 技术写作, content organization, 内容组织, error detection, 错误检测, check document, 检查文档 | `dev-document_review`    |

---

## 🤖 AI Technology

| Keywords                                               | Skill           |
| ------------------------------------------------------ | --------------- |
| agent, 智能体, AI agent, framework selection, 框架选型 | `ai-agents`     |
| prompt, 提示词, prompt engineering                     | `ai-prompts`    |
| skill, claude skill                                    | `ai-skills`     |
| llm, 大模型, 语言模型, language model                  | `ai-llm_models` |

---

## 🎓 AI Learning

| Keywords                                          | Skill                                |
| ------------------------------------------------- | ------------------------------------ |
| machine learning, ML, 机器学习                    | `ai_learning-ml`                     |
| deep learning, DL, 深度学习                       | `ai_learning-dl`                     |
| LLM learning, 大模型学习                          | `ai_learning-llm`                    |
| NLP, natural language processing, 自然语言处理    | `ai_learning-nlp`                    |
| machine vision, MV, computer vision, CV, 机器视觉 | `ai_learning-mv` or `ai_learning-cv` |
| RAG, retrieval augmented generation, 检索增强     | `ai_learning-rag`                    |
| reinforcement learning, RL, 强化学习              | `ai_learning-rl`                     |

---

## 💼 Career Development

| Keywords               | Skill                     |
| ---------------------- | ------------------------- |
| resume, CV, 简历       | `career-resume`           |
| interview, 面试        | `career-interview`        |
| job search, 求职       | `career-job_search`       |
| certification, 认证    | `career-certification`    |
| entrepreneurship, 创业 | `career-entrepreneurship` |

---

## 🛂 Immigration & Identity

| Keywords                                         | Skill                                                  |
| ------------------------------------------------ | ------------------------------------------------------ |
| visa, 签证                                       | `identity-visa` or `immigration-visa_renewal`          |
| PR, permanent residence, 永居, immigration, 移民 | `immigration-pr_application`                           |
| work permit, 工签                                | `immigration-work_permit`                              |
| citizenship, 入籍                                | `immigration-citizenship`                              |
| family sponsorship, 家庭团聚, 担保               | `immigration-family_sponsorship`                       |
| SSN, social security number, 社保号              | `identity-ssn`                                         |
| driver's license, 驾照                           | `identity-driving` or `transportation-driving_license` |

---

## 💰 Finance

| Keywords            | Skill                 |
| ------------------- | --------------------- |
| banking, 银行       | `finance-banking`     |
| credit card, 信用卡 | `finance-credit_card` |
| insurance, 保险     | `finance-insurance`   |
| investment, 投资    | `finance-investment`  |
| remittance, 汇款    | `finance-remittance`  |
| tax, 报税           | `finance-tax`         |

---

## 🏠 Housing

| Keywords          | Skill                 |
| ----------------- | --------------------- |
| rental, 租房      | `housing-rental`      |
| home buying, 买房 | `housing-home_buying` |
| moving, 搬家      | `housing-moving`      |
| furniture, 家具   | `housing-furniture`   |
| utilities, 水电煤 | `housing-utilities`   |

---

## 🚗 Transportation

| Keywords             | Skill                           |
| -------------------- | ------------------------------- |
| car buying, 买车     | `transportation-car_buying`     |
| car insurance, 车险  | `transportation-car_insurance`  |
| public transit, 公交 | `transportation-public_transit` |
| flight, 机票         | `transportation-flight`         |

---

## 🏥 Healthcare

| Keywords                   | Skill                         |
| -------------------------- | ----------------------------- |
| family doctor, 家庭医生    | `healthcare-family_doctor`    |
| clinic visit, 看病         | `healthcare-clinic_visit`     |
| pharmacy, 药房             | `healthcare-pharmacy`         |
| health insurance, 医疗保险 | `healthcare-health_insurance` |
| mental health, 心理健康    | `healthcare-mental_health`    |
| childcare, 托儿            | `healthcare-childcare`        |

---

## 📚 Education

| Keywords                        | Skill                             |
| ------------------------------- | --------------------------------- |
| school selection, 选校          | `education-school_selection`      |
| credential evaluation, 学历认证 | `education-credential_evaluation` |
| language learning, 语言学习     | `education-language_learning`     |
| skill training, 培训            | `education-skill_training`        |
| tutoring, 补习                  | `education-tutoring`              |
| child education, 子女教育       | `education-child_education`       |

---

## 📝 Learning & Study

| Keywords                                                                                                                                                                                               | Skill                          |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------ |
| notes, 笔记, note-taking, 记笔记, study notes, 学习笔记, lecture notes, 课堂笔记, organize notes, 整理笔记, course materials, 课程资料, study guide, 学习指南                                          | `learning-note_taking`         |
| code generation, 生成代码, generate code, 写代码, lab code, assignment code, jupyter, python script, 作业代码, homework code                                                                           | `learning-code_generation`     |
| assignment document, 作业文档, Lab.docx, submission document, 提交文档, word document, screenshots, 截图, discussion, 讨论, analysis, 分析                                                             | `learning-assignment_document` |
| consistency, 一致性, check consistency, 检查一致, verify files, 验证文件, .py .ipynb .md, compare files, 对比文件, validate code, 验证代码                                                             | `learning-code_consistency`    |
| markdown to word, md转docx, convert to docx, 转换docx, pandoc, word document, 生成word, format document, 格式化文档                                                                                    | `learning-md_to_docx`          |
| notebook conversion, ipynb转py, py转ipynb, convert notebook, 转换notebook, jupyter convert, nbconvert, jupytext, script to notebook, notebook to script, 笔记本转换                                    | `learning-notebook_conversion` |
| submit lab, 提交lab, lab submission, 作业提交, prepare submission, 准备提交, zip file, 打包, upload assignment, 上传作业, brightspace                                                                  | `learning-lab_submission`      |
| brightspace scraper, brightspace抓取, scrape brightspace, 抓取课程, download course, 下载课程, course materials, 课程资料, scrape slides, 抓取slides, scrape labs, 抓取labs, LMS scraper, 学习平台抓取 | `learning-brightspace_scraper` |

---

## 🔄 Usage Workflow

1. **Detect keywords** in user query (English or Chinese)
2. **Identify matching skill(s)** from the mappings above
3. **Read the SKILL.md file**: `backend/scripts/data/skills/{skill-name}/SKILL.md`
4. **Validate skill structure** before applying:
   - Verify SKILL.md has complete structure and format
   - Check for required sections (objectives, use cases, instructions)
   - Ensure content is clear and actionable
   - If non-compliant, fix the skill file first before using
5. **Load additional references** if available: `backend/scripts/data/skills/{skill-name}/references/`
6. **Apply skill guidance** to assist the user
