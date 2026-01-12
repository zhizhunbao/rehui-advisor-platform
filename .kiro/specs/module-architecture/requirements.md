# Requirements Document

## Introduction

本文档定义北美生活决策顾问系统的前后端模块化架构规范。系统采用分层+分模块的混合架构，确保代码的可维护性、可扩展性和团队协作效率。

## Glossary

- **Module（模块）**: 按业务领域划分的独立功能单元，包含该领域的所有分层代码
- **Layer（层）**: 按技术职责划分的代码组织方式，如 Controller、Service、Repository
- **Domain（领域）**: 业务领域，如 Flight、Hotel、Job 等
- **Core Module（核心模块）**: 提供基础设施和通用功能的模块
- **Feature Module（功能模块）**: 实现具体业务功能的模块

## Requirements

### Requirement 1: Backend Module Structure

**User Story:** As a backend developer, I want a clear module structure, so that I can easily locate and maintain code for specific business domains.

#### Acceptance Criteria

1. THE backend SHALL organize code into the following core modules: auth, common, search, recommendation, data-pipeline
2. THE backend SHALL organize code into the following domain modules: flight, hotel, job, car, house, education, investment
3. WHEN a new domain is added THEN THE backend SHALL follow the same module structure pattern
4. THE backend SHALL implement each module with consistent internal layers: controller, service, repository, dto, types

### Requirement 2: Backend Layer Standards

**User Story:** As a backend developer, I want consistent layer responsibilities, so that I can understand where to place different types of code.

#### Acceptance Criteria

1. THE Controller layer SHALL handle HTTP request/response, input validation, and route definitions only
2. THE Service layer SHALL contain all business logic and orchestrate repository calls
3. THE Repository layer SHALL handle all database operations using Prisma
4. THE DTO layer SHALL define data transfer objects for API input/output
5. THE Types layer SHALL define TypeScript interfaces and type definitions
6. WHEN a layer needs to communicate with another layer THEN THE communication SHALL flow: Controller → Service → Repository

### Requirement 3: Frontend Module Structure

**User Story:** As a frontend developer, I want a clear module structure, so that I can easily locate and maintain UI components for specific features.

#### Acceptance Criteria

1. THE frontend SHALL organize code into the following core modules: auth, common, layout
2. THE frontend SHALL organize code into the following feature modules: flight, hotel, job, car, house, education, investment, search, recommendation
3. WHEN a new feature is added THEN THE frontend SHALL follow the same module structure pattern
4. THE frontend SHALL implement each module with consistent internal structure: components, hooks, services, types, utils

### Requirement 4: Frontend Layer Standards

**User Story:** As a frontend developer, I want consistent layer responsibilities, so that I can understand where to place different types of code.

#### Acceptance Criteria

1. THE Components folder SHALL contain React components specific to the module
2. THE Hooks folder SHALL contain custom React hooks for state and side effects
3. THE Services folder SHALL contain API call functions using Axios
4. THE Types folder SHALL define TypeScript interfaces for the module
5. THE Utils folder SHALL contain helper functions specific to the module
6. WHEN a component is shared across modules THEN THE component SHALL be placed in the common module

### Requirement 5: Module Documentation

**User Story:** As a developer, I want documentation for each module and layer, so that I can understand the conventions and standards to follow.

#### Acceptance Criteria

1. THE backend SHALL have a README.md in each module directory explaining the module's purpose and structure
2. THE frontend SHALL have a README.md in each module directory explaining the module's purpose and structure
3. THE documentation SHALL include code examples for common patterns
4. THE documentation SHALL specify naming conventions for files and exports
5. WHEN a new module is created THEN THE module SHALL include a README.md following the standard template

### Requirement 6: Cross-Module Communication

**User Story:** As a developer, I want clear rules for cross-module communication, so that I can avoid circular dependencies and maintain clean architecture.

#### Acceptance Criteria

1. THE modules SHALL communicate through well-defined interfaces exported from module index files
2. THE domain modules SHALL NOT directly import from other domain modules
3. WHEN a domain module needs functionality from another domain THEN THE functionality SHALL be accessed through the common module or service layer
4. THE core modules SHALL be importable by any module
5. THE circular dependencies SHALL be prevented by following the dependency direction: domain modules → core modules → shared utilities
