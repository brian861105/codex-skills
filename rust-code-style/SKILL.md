---
name: rust-code-style
description: Code style conventions for the ai-editor Rust codebase. Covers documentation, testing, error handling, struct design, and naming patterns. Use when writing new Rust code or reviewing code quality.
---

# Rust Code Style

Code style patterns derived from `core/src/crdt` module.

## Documentation

### Module-Level Documentation

Use `//!` for module-level docs explaining purpose and data structures:

```rust
//! Metadata storage for AI suggestions in CRDT documents.
//!
//! ## Data Structure
//!
//! The suggestions are stored in a yrs Map with the following structure:
//!
//! ```text
//! suggestions: Map {
//!   "<action_id>": {
//!     ai_id: String,
//!     suggestions: Array [...]
//!   }
//! }
//! ```
```

### Function Documentation

Use `///` for public functions with examples when helpful:

```rust
/// Get diff contexts for all pending deltas and clear the list.
///
/// Returns a list of text segments that were affected by changes, including
/// surrounding context. The ranges are automatically:
/// - Expanded to include `context_chars` characters before and after
/// - Merged if they overlap
/// - Adjusted to word boundaries
///
/// # Example
/// ```ignore
/// let contexts = state.get_diff_contexts(10);
/// for ctx in contexts {
///     println!("Changed: {} at [{}, {})", ctx.text, ctx.start, ctx.end);
/// }
/// ```
pub fn get_diff_contexts(&mut self, context_chars: usize) -> Vec<DiffContext>
```

### Inline Comments

Add inline comments for complex logic:

```rust
// yrs::Doc uses Arc internally, so cloning is cheap
Self {
    id: self.id,
    content: self.content.clone(),
    pending_deltas: Vec::new(), // Don't clone pending deltas
}
```

## Testing

### Test Structure

All tests in `#[cfg(test)] mod tests` at bottom of file:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_default_document_state() {
        let state = DocumentState::default();
        let text = state.get_text();
        assert_eq!(text, "");
    }

    #[tokio::test]
    async fn test_async_operation() {
        // async test content
    }
}
```

### Test Naming

Use descriptive names: `test_<functionality>_<scenario>`

```rust
#[test]
fn test_merge_ranges_empty() { }

#[test]
fn test_merge_ranges_no_overlap() { }

#[test]
fn test_merge_ranges_overlapping() { }

#[test]
fn test_insert_nonexistent_document_fails() { }

#[test]
fn test_concurrent_get_or_load() { }
```

### Test Coverage

Follow Equivalence Class Partitioning (user rule):

- **Empty/zero cases**: `test_merge_ranges_empty`, `test_get_empty_suggestions`
- **Single element**: `test_insert_and_get_single_suggestion`
- **Multiple elements**: `test_insert_multiple_suggestions`, `test_multiple_documents`
- **Edge cases**: `test_large_index_values`, `test_special_characters_in_text`, `test_unicode_text`
- **Boundary conditions**: `test_expand_to_word_boundaries_already_at_boundary`
- **Error cases**: `test_insert_nonexistent_document_fails`
- **Concurrency**: `test_concurrent_get_or_load`

### Database Tests

Use setup/teardown helpers with unique database names:

```rust
#[tokio::test]
async fn test_insert_and_get_document() {
    let pool = setup_test_db("doc_registry_1").await.unwrap();
    
    // Test code here
    
    teardown_test_db("doc_registry_1", pool).await.unwrap();
}
```

## Error Handling

### Return Types

- **Application code**: `anyhow::Result<T>` for flexibility
- **Library crates**: `thiserror` for public error types to allow callers to match on specific errors
- **Internal functions**: Specific error types (`sqlx::Error`, `yrs::encoding::read::Error`)
- **Optional values**: `Option<T>` with safe fallbacks

```rust
// Application code (bin/ai-editor)
pub async fn load_from_store(pool: &PgPool, id: Uuid) -> anyhow::Result<Self> {
    let data = crate::store::crdt::load_document(pool, id).await?;
    // ...
}

// Library code (core crate) - use thiserror for public APIs
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DocumentError {
    #[error("Document not found: {0}")]
    NotFound(Uuid),
    
    #[error("Invalid update format")]
    InvalidUpdate(#[from] yrs::encoding::read::Error),
    
    #[error("Database error")]
    Database(#[from] sqlx::Error),
}

pub async fn load_document(pool: &PgPool, id: Uuid) -> Result<Doc, DocumentError> {
    // Callers can now match on specific errors
}

// Optional with safe fallback
pub fn get_text(&self) -> String {
    self.try_get_text().unwrap_or_default()
}

fn try_get_text(&self) -> Option<String> {
    let txn = self.content.transact();
    let f = txn.get_xml_fragment("content")?;
    // ...
}
```

### Why thiserror for Libraries?

Library error types with `thiserror` allow callers to handle specific cases:

```rust
match load_document(&pool, id).await {
    Ok(doc) => process(doc),
    Err(DocumentError::NotFound(_)) => create_new_document(),
    Err(DocumentError::InvalidUpdate(_)) => retry_with_reset(),
    Err(e) => return Err(e.into()),
}
```

## Struct Design

### Public Interface with Private Fields

```rust
pub struct DocumentState {
    id: Uuid,
    pub content: Doc,
    pending_deltas: Vec<DeltaChange>,
}
```

### Standard Trait Implementations

Implement `Clone`, `Default` when appropriate:

```rust
impl Clone for DocumentState {
    fn clone(&self) -> Self {
        // Custom implementation with explanation
        Self {
            id: self.id,
            content: self.content.clone(),
            pending_deltas: Vec::new(),
        }
    }
}

impl Default for DocumentState {
    fn default() -> Self {
        Self {
            id: Uuid::new_v4(),
            content: Doc::new(),
            pending_deltas: vec![],
        }
    }
}
```

### Concurrent Data Structures

Use `Arc` for shared ownership, `DashMap` for concurrent access:

```rust
#[derive(Default, Clone)]
pub struct DocumentRegistry {
    documents: DashMap<Uuid, Arc<DocumentState>>,
}

impl DocumentRegistry {
    pub fn get(&self, id: Uuid) -> Option<Arc<DocumentState>> {
        self.documents.get(&id).map(|doc| doc.clone())
    }
}
```

## Code Organization

### File Structure Order

1. Imports
2. Public types and enums
3. Struct definition
4. Trait implementations (`Clone`, `Default`)
5. Public methods
6. Private helper methods
7. Tests module

```rust
use super::change_tracker::{DeltaChange, DiffContext};
use atb_types::Uuid;

pub struct DocumentState { /* ... */ }

impl Clone for DocumentState { /* ... */ }
impl Default for DocumentState { /* ... */ }

impl DocumentState {
    pub fn new(id: Uuid) -> Self { /* ... */ }
    pub fn get_text(&self) -> String { /* ... */ }
    
    fn try_get_text(&self) -> Option<String> { /* ... */ }
    fn ensure_text_node(&self) -> XmlTextRef { /* ... */ }
}

#[cfg(test)]
mod tests { /* ... */ }
```

## Naming Conventions

### Functions

All functions use `snake_case`. Follow Rust API naming conventions:

**Constructors**
- `new()` - default constructor
- `default()` - via `Default` trait
- `with_*()` - constructor with configuration: `with_capacity`, `with_timeout`
- `from_*()` - conversion constructor: `from_bytes`, `from_str`

**Conversions**
- `as_*()` - cheap reference-to-reference: `as_ref`, `as_mut`, `as_bytes`
- `to_*()` - expensive conversion creating new data: `to_string`, `to_vec`, `to_owned`
- `into_*()` - consuming conversion: `into_iter`, `into_inner`, `into_bytes`

**Getters**
- Use field name directly: `len()`, `capacity()`, `id()` (no `get_` prefix)
- Only use `get_*` when returning computed values: `get_text()`, `get_or_load()`

**Boolean Predicates**
- `is_*()` - state check: `is_empty`, `is_valid`, `is_word_boundary`
- `has_*()` - possession: `has_permission`, `has_feature`
- `can_*()` - capability: `can_read`, `can_write`
- `should_*()` - recommendation: `should_retry`, `should_update`

**Mutators**
- Action verbs: `insert()`, `remove()`, `push()`, `clear()`
- `set_*()` only when needed for clarity: `set_timeout()`

**Fallible Operations**
- `try_*()` - fallible version returning `Option` or `Result`: `try_get_text()`, `try_lock()`

**Private Helpers**
- Start with verb: `ensure_text_node()`, `expand_to_word_boundaries()`
- Use `try_*` prefix for fallible helpers: `try_parse()`, `try_extract()`

**Examples from codebase:**
```rust
// Constructor
pub fn new(id: Uuid) -> Self { }

// Getter (no get_ prefix)
pub fn len(&self) -> usize { }

// Boolean predicate
pub fn is_empty(&self) -> bool { }

// Computed getter (with get_ prefix)
pub fn get_text(&self) -> String { }

// Fallible helper
fn try_get_text(&self) -> Option<String> { }

// Mutator
pub fn insert(&self, id: Uuid, pool: &PgPool) { }
pub fn remove(&self, id: Uuid) { }
pub fn clear_deltas(&mut self) { }

// Combined operation
pub async fn get_or_load(&self, id: Uuid, pool: &PgPool) -> Result<T> { }

// Private helper
fn ensure_text_node(&self) -> XmlTextRef { }
```

### Types

- `PascalCase` for structs and enums
- Descriptive: `DocumentState`, `DiffContext`, `MetadataStore`

### Variables

- `snake_case`: `pending_deltas`, `doc_state`, `action_id`
- Descriptive: `adjusted_start`, `last_idx`, `text_len`

## Async Patterns

### Async Functions

Use `async fn` for I/O operations:

```rust
pub async fn load_from_store(pool: &PgPool, id: Uuid) -> anyhow::Result<Self> {
    let data = crate::store::crdt::load_document(pool, id).await?;
    // ...
}
```

### Transaction Management

Scope transactions tightly:

```rust
pub fn insert_text(&self, index: u32, text: &str) {
    let t = self.ensure_text_node();
    let mut txn = self.content.transact_mut();
    t.insert(&mut txn, index, text);
}

pub fn apply_update(&self, update_data: &[u8]) -> Result<(), Error> {
    let update = Update::decode_v1(update_data)?;
    let mut txn = self.content.transact_mut();
    let _ = txn.apply_update(update);
    Ok(())
}
```

### Concurrent Operations

```rust
pub async fn get_or_load(&self, id: Uuid, pool: &PgPool) -> anyhow::Result<Arc<DocumentState>> {
    if let Some(doc) = self.get(id) {
        return Ok(doc);
    }

    match self.documents.entry(id) {
        dashmap::mapref::entry::Entry::Occupied(entry) => Ok(entry.get().clone()),
        dashmap::mapref::entry::Entry::Vacant(entry) => {
            let doc_state = DocumentState::load_from_store(pool, id).await?;
            let doc = Arc::new(doc_state);
            entry.insert(doc.clone());
            Ok(doc)
        }
    }
}
```

## Performance & Iterators

### Avoid Unnecessary collect()

Only call `collect()` when you need to own the collection. Prefer iterator chains when possible:

```rust
// ❌ Unnecessary collect
let numbers: Vec<i32> = vec![1, 2, 3, 4, 5];
let doubled: Vec<i32> = numbers.iter().map(|x| x * 2).collect();
let sum: i32 = doubled.iter().sum();

// ✅ Direct iterator chain
let numbers: Vec<i32> = vec![1, 2, 3, 4, 5];
let sum: i32 = numbers.iter().map(|x| x * 2).sum();

// ❌ Unnecessary intermediate collection
fn process_items(items: &[Item]) -> Vec<String> {
    let filtered: Vec<&Item> = items.iter().filter(|i| i.is_valid()).collect();
    filtered.iter().map(|i| i.name.clone()).collect()
}

// ✅ Single iterator chain
fn process_items(items: &[Item]) -> Vec<String> {
    items.iter()
        .filter(|i| i.is_valid())
        .map(|i| i.name.clone())
        .collect()
}

// ❌ Unnecessary collect for iteration
let ids: Vec<Uuid> = documents.keys().collect();
for id in ids {
    process(id);
}

// ✅ Direct iteration
for id in documents.keys() {
    process(id);
}
```

### When collect() Is Needed

Use `collect()` when you actually need the collection:

```rust
// ✅ Need to reuse the collection
let valid_items: Vec<_> = items.iter()
    .filter(|i| i.is_valid())
    .collect();

process_batch(&valid_items);
store_backup(&valid_items);

// ✅ Need to mutate or sort
let mut sorted: Vec<_> = items.iter().collect();
sorted.sort_by_key(|i| i.priority);

// ✅ Converting to specific collection type
let unique_ids: HashSet<Uuid> = documents.keys()
    .cloned()
    .collect();

// ✅ From codebase: collecting chars for indexing
pub fn expand_to_word_boundaries(text: &str, start: usize, end: usize) -> (usize, usize) {
    let chars: Vec<char> = text.chars().collect(); // Needed for indexed access
    let text_len = chars.len();
    // ...
}
```

## Helper Functions

### Utility Functions

Keep pure functions separate and well-tested:

```rust
/// Expand range to word boundaries to avoid cutting words in half
pub fn expand_to_word_boundaries(text: &str, start: usize, end: usize) -> (usize, usize) {
    let chars: Vec<char> = text.chars().collect();
    let text_len = chars.len();
    
    if start >= text_len {
        return (start, end);
    }
    
    // Implementation...
}

/// Merge overlapping ranges into consolidated ranges
pub fn merge_ranges(mut ranges: Vec<(usize, usize)>) -> Vec<(usize, usize)> {
    if ranges.is_empty() {
        return vec![];
    }
    
    ranges.sort_by_key(|r| r.0);
    // Implementation...
}
```
