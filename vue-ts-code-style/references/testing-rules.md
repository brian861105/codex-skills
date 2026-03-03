# Testing Rules (`/html`)

Primary stack: Vitest + Vue Test Utils.

## Rule TEST-001 (must): Test naming pattern

- Intent: make failures self-explanatory.
- ESLint mapping:
  - if using eslint-plugin-vitest: `vitest/consistent-test-it`
- Applies to: all test files.

Bad:

```ts
it('works', () => {});
```

Good:

```ts
it('test_save_case_returns_error_when_payload_invalid', () => {});
```

## Rule TEST-002 (must): Follow Arrange-Act-Assert

- Intent: keep tests readable and maintainable.
- ESLint mapping:
  - no direct lint rule; enforce by review.
- Applies to: unit and component tests.

Bad:

```ts
it('test_switch_tab_updates_page', async () => {
  expect(wrapper.text()).toContain('Case A');
  await wrapper.find('[data-test=tab-b]').trigger('click');
});
```

Good:

```ts
it('test_switch_tab_updates_page', async () => {
  // Arrange
  const wrapper = mount(CaseTabs);

  // Act
  await wrapper.find('[data-test=tab-b]').trigger('click');

  // Assert
  expect(wrapper.text()).toContain('Case B');
});
```

## Rule TEST-003 (must): Cover async failure branch

- Intent: prevent happy-path-only tests.
- ESLint mapping:
  - no direct lint rule; required by checklist.
- Applies to: API/store/composable tests.

Bad:

```ts
it('test_load_cases_success', async () => {
  vi.spyOn(api, 'loadCases').mockResolvedValue([]);
  await expect(loadCases()).resolves.toEqual([]);
});
```

Good:

```ts
it('test_load_cases_fails_when_api_rejects', async () => {
  vi.spyOn(api, 'loadCases').mockRejectedValue(new Error('timeout'));
  await expect(loadCases()).rejects.toThrow('timeout');
});
```

## Rule TEST-004 (should): Prefer behavior assertions over implementation details

- Intent: reduce brittle tests.
- ESLint mapping:
  - no direct lint rule; review-driven.
- Applies to: component tests.

Bad:

```ts
expect((wrapper.vm as any).internalCount).toBe(2);
```

Good:

```ts
expect(wrapper.find('[data-test=count]').text()).toBe('2');
```

## Rule TEST-005 (prefer): Keep test fixtures minimal

- Intent: speed up debugging and reduce setup noise.
- ESLint mapping:
  - no direct lint rule.
- Applies to: test data and mocks.

Bad:

```ts
const casePayload = {
  id: 1,
  title: 'A',
  description: '...',
  // 40 more fields not used by the assertion
};
```

Good:

```ts
const casePayload = { id: 1, title: 'A' };
```
