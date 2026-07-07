# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

智慧物业 (Smart Property) -- a property management system graduation project. Spring Boot backend + pure static HTML/JS frontend, no frontend build tools.

## Build & Run

```bash
mvn clean compile          # Compile
mvn spring-boot:run        # Run on localhost:8080
mvn clean package          # Build JAR
java -jar target/property-management-1.0.0.jar
```

Database init: `src/main/resources/db_init.sql` (MySQL 8.0, database `property_management`, user `root`/`123456`).

Default login: `admin` / `123456`

No test suite exists. No Docker config.

## Architecture

### Backend (Java 8, Spring Boot 2.7, MyBatis)

Generic base class hierarchy -- most modules get CRUD for free by extending these:

- `BaseDao<T>` → `BaseService<T>` → `BaseServiceImpl<T>` → `BaseController<T>`
- Standard CRUD endpoints: `GET /findById/{id}`, `POST /findPage`, `POST /add`, `PUT /edit`, `DELETE /delete/{id}`
- Simple modules (Owner, House, Building, etc.) have **empty subclasses** that inherit everything
- Complex modules (User, Payment, Dashboard) add custom endpoints on top

Package: `com.wygl` | Entry: `Application.java` with `@MapperScan("com.wygl.dao")`

Key packages:
- `controller/` — 15 REST controllers
- `service/` + `service/impl/` — service interfaces + implementations
- `service/ai/` — AI remind feature (IAiRemindService, IAiRemindLogService)
- `dao/` — MyBatis mapper interfaces
- `pojo/` — plain Java beans (no Lombok, manual getters/setters)
- `mapper/` (resources) — MyBatis XML files, one per DAO
- `config/` — WebConfig (CORS + interceptor), AiConfig, AiService
- `interceptor/` — AuthInterceptor (JWT Bearer token, skips login + static paths)
- `result/` — `Result` (`{flag, message, data}`) + `PageResult` (`{total, rows}`)

### Frontend (static files, no build step)

Located in `src/main/resources/static/`. Served directly by Spring Boot.

- `js/api.js` — all API endpoint definitions (axios calls)
- `js/axios-config.js` — baseURL, interceptors, token injection
- `js/page-common.js` — reusable CRUD table/search/pagination logic (also has mock data fallback)
- `js/sidebar.js` — navigation menu
- `css/common.css` — CSS variables system, responsive styles
- `pages/*.html` — 19 page files, self-contained (inline scripts + shared JS)

### Auth Flow

JWT stored in `localStorage`. `AuthInterceptor` validates `Authorization: Bearer <token>` on every request except login and static resources.

### AI Feature

Disabled by default (`ai.enabled=false` in application.properties). When enabled, calls DeepSeek API via OkHttp. Controlled by `AiConfig.AI_ENABLED`.

## Conventions

- Database tables use `t_` prefix (e.g., `t_user`, `t_owner`, `t_building`)
- MyBatis XML mappers live in `src/main/resources/mapper/`, one per DAO interface
- Underscore-to-camelCase mapping is enabled globally
- Pagination uses PageHelper (MySQL dialect)
- All API responses wrapped in `Result` class
- Design doc: `设计文档.md` | Progress tracker: `开发进度.md`
