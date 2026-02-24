---
name: rust-sqlx-patterns
description: Guide for writing SQLx database queries in Rust. Covers simple queries, transactions, reusable PgExecutor patterns, and SeaQuery for dynamic filters. Use when writing database code, queries, or migrations.
---

# Rust SQLx Patterns

## Database Queries

### Simple Reads/Writes

Wrap queries in helper functions that accept a `PgPool` and map results into domain structs:

```rust
#[derive(sqlx::FromRow)]
pub struct Company { id: Uuid, company_name: Option<String> }

pub async fn get_company(pool: &PgPool, id: Uuid) -> Result<Company, sqlx::Error> {
    sqlx::query_as::<_, Company>(
        "SELECT id, company_name FROM companies WHERE id = $1",
    )
    .bind(id)
    .fetch_one(pool)
    .await
}
```

### Transactional Operations

Use `Transaction<'_, Postgres>` for multiple statements that must succeed or fail together:

```rust
let mut tx = pool.begin().await?;
insert_conversation(tx.as_mut(), &conversation).await?;
insert_ai_interaction(tx.as_mut(), &interaction).await?;
tx.commit().await?;
```

### Reusable Queries with PgExecutor

For queries that should work with either a `PgPool` or a transaction, use a generic `PgExecutor` argument:

```rust
use sqlx::{Executor, Postgres};

/// An alias for `Executor<'_, Database = Postgres>`.
pub trait PgExecutor<'c>: Executor<'c, Database = Postgres> {}
impl<'c, T: Executor<'c, Database = Postgres>> PgExecutor<'c> for T {}

pub async fn update_address_by_id<'c, T: PgExecutor<'c>>(
    conn: T,
    user_id: &i64,
    address: &str,
) -> Result<User, sqlx::Error> {
    sqlx::query(
        r#"
        UPDATE users SET
        address = $1
        WHERE id = $2
        RETURNING *
        "#,
    )
    .bind(address)
    .bind(user_id)
    .try_map(TryInto::try_into)
    .fetch_one(conn)
    .await
}
```

### Complex/Optional Filters with SeaQuery

Use SeaQuery with identity enums in `core::store::identity` to dynamically build SQL:

```rust
let (sql, values) = sea_query::Query::select()
    .columns(ALL_COMPANY_COLUMNS)
    .from(Companies::Table)
    .and_where_option(name_filter.map(|f| Expr::col((CompanyRegistry::Table,
        CompanyRegistry::CompanyName)).ilike(format!("%{}%", f))))
    .build_sqlx(PostgresQueryBuilder);

let companies = sqlx::query_as_with(&sql, values).fetch_all(&pool).await?;
```

## Migrations

- SQL migration files live under `core/migrations`
- Executed using `sqlx::migrate!()` through the helper in `core::sqlx_postgres::migrate`
- Create new migrations by adding a timestamped `.sql` file to that directory
