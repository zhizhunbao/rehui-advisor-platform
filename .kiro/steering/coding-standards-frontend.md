---
inclusion: fileMatch
fileMatchPattern:
  [
    "**/frontend/**/*.ts",
    "**/frontend/**/*.tsx",
    "**/frontend/**/*.js",
    "**/frontend/**/*.jsx",
  ]
---

# Frontend Coding Standards

## Architecture Overview

This frontend follows a strict layered architecture with clear dependency rules. Each layer has specific responsibilities and import restrictions to maintain separation of concerns.

## Import Dependency Rules

Follow these import rules strictly. Each layer can only import from allowed layers:

- `common/` - Foundation layer with no dependencies. Can be imported by any layer.
- `libs/` - Third-party library wrappers. Only imports from `common/`.
- `modules/*/types/` - Type definitions. Only imports from `common/`.
- `modules/*/services/` - API calls and data fetching. Imports: `common/`, `libs/`, same module `types/`.
- `modules/*/hooks/` - State management and business logic. Imports: `common/`, same module `services/`, `types/`.
- `modules/*/components/` - Presentational UI components. Imports: `common/`, `libs/`, same module `types/`. NEVER import `hooks/` or `services/`.
- `modules/*/views/` - Page-level components. Imports: same module `hooks/`, `components/`, plus `common/`, `libs/`.
- `App.tsx` - Application entry. Only imports: `common/`, same module `hooks/`, `views/`.

**Critical**: Components must receive data via props only. Never import hooks or services directly into components.

## File Organization

Place code in the correct location:

- `common/enum.ts` - All enums and constants (use const objects, not TypeScript enum keyword)
- `common/helper.ts` - Utility functions
- `common/types.ts` - Shared type definitions and interfaces
- `common/stores.ts` - Global state management
- Import directly from specific files. Do NOT use `index.ts` barrel exports.

## TypeScript Standards

- Use strict typing. Never use `any` type.
- Prefer `interface` for object shapes, `type` for unions/intersections.
- Define all function return types explicitly.
- Use const objects instead of TypeScript `enum` keyword.

## Naming Conventions

- Functions and variables: `camelCase`
- React components: `PascalCase`
- Constants: `UPPER_SNAKE_CASE` (in enum.ts)
- Files: Match the primary export (component files use PascalCase, others use camelCase)

## API Integration

- Convert API responses from snake_case to camelCase using `keysToCamel()` helper.
- All API calls must be in `services/` layer.
- Handle errors consistently using common error handling utilities.

## UI Components

- Prefer using components from `libs/shadcn/ui/` for consistency.
- Keep components pure and presentational.
- Pass data and callbacks via props, never fetch data inside components.

## Code Quality Rules

**Prohibited**:

- Defining constants inside components (move to `common/enum.ts`)
- Defining utility functions inside modules (move to `common/helper.ts`)
- Defining interfaces inside modules (move to `common/types.ts`)
- Using TypeScript `enum` keyword (use const objects instead)
- Cross-module imports except through `common/`
- Leaving `console.log` statements in committed code
- Leaving commented-out code in commits
- Functions longer than 50 lines (refactor into smaller functions)
- Files longer than 300 lines (split into multiple files)

## Layer Responsibilities

- **services**: Handle API communication. Return typed data. No UI logic.
- **hooks**: Manage state and business logic. Call services. Return data and actions.
- **components**: Render UI based on props. No data fetching or business logic.
- **views**: Compose components and hooks. Handle page-level layout and data flow.

When creating or modifying code, always verify the import dependencies match these rules.
