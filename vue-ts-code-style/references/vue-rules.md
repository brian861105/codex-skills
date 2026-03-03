# Vue Rules (`/html`)

Apply these rules to `.vue` files with `<script setup lang="ts">`.

## Rule VUE-001 (must): Keep setup block ordering stable

- Intent: reduce cognitive load in large SFCs.
- ESLint mapping:
  - `vue/order-in-components` (for options sections where relevant)
  - `sort-imports` / `import/order` for import section
- Applies to: SFC script block structure.

Recommended order:

1. imports
2. store/composables wiring
3. refs/reactive state
4. computed
5. methods/handlers
6. watchers
7. lifecycle hooks

Bad:

```vue
<script setup lang="ts">
onMounted(() => load());
const state = ref(0);
import { ref, onMounted } from 'vue';
</script>
```

Good:

```vue
<script setup lang="ts">
import { onMounted, ref } from 'vue';

const state = ref(0);

onMounted(() => {
  load();
});
</script>
```

## Rule VUE-002 (must): Typed props and emits

- Intent: enforce component contracts at compile time.
- ESLint mapping:
  - `vue/require-prop-types` (if using runtime props)
  - `vue/require-explicit-emits`
- Applies to: reusable components and shared UI modules.

Bad:

```vue
<script setup lang="ts">
const props = defineProps(['title']);
const emit = defineEmits(['save']);
</script>
```

Good:

```vue
<script setup lang="ts">
const props = defineProps<{ title: string }>();
const emit = defineEmits<{
  (e: 'save', id: number): void;
}>();
</script>
```

## Rule VUE-003 (must): Respect reactivity boundaries

- Intent: avoid accidental reactive loss in Pinia and local state.
- ESLint mapping:
  - `vue/no-ref-as-operand`
  - `vue/no-setup-props-destructure` (legacy rule names may vary by version)
- Applies to: state reads/writes and store usage.

Bad:

```ts
const { caseList } = useReportStore();
```

Good:

```ts
const reportStore = useReportStore();
const { caseList } = storeToRefs(reportStore);
```

## Rule VUE-004 (should): Keep computed pure

- Intent: prevent side effects in derived state.
- ESLint mapping:
  - `vue/no-side-effects-in-computed-properties`
- Applies to: computed getters.

Bad:

```ts
const doubled = computed(() => {
  count.value += 1;
  return count.value * 2;
});
```

Good:

```ts
const doubled = computed(() => count.value * 2);
```

## Rule VUE-005 (prefer): Avoid broad `watchEffect` when `watch` is enough

- Intent: reduce hidden dependency tracking.
- ESLint mapping:
  - no direct lint rule; enforce via review checklist.
- Applies to: side effects tied to specific sources.

Bad:

```ts
watchEffect(() => {
  saveDraft(form.value);
});
```

Good:

```ts
watch(
  () => form.value.title,
  () => {
    saveDraft(form.value);
  }
);
```
