---
name: frontend-debugging
description: Debug frontend applications using systematic reproduction, browser DevTools, JavaScript/TypeScript debuggers, console traces, network inspection, DOM/CSS inspection, state inspection, performance profiling, source maps, and framework-specific tools.
when_to_use: Use when diagnosing frontend bugs, broken UI behavior, rendering issues, JavaScript errors, failed network requests, state bugs, CSS/layout problems, performance issues, hydration bugs, or browser-specific behavior.
argument-hint: "[page-or-component-or-bug]"
---

# Frontend Debugging

Use this skill when a frontend application behaves incorrectly and needs diagnosis before changing code.

## First Principle

Debugging is observation before explanation.

Do not start by guessing the fix. First reproduce the issue, identify what the browser is actually doing, and use debugging tools to compare expected behavior with runtime behavior.

## When To Use

- A UI interaction does not work.
- A component renders the wrong data or does not render.
- A page has JavaScript or TypeScript runtime errors.
- A network request fails or returns unexpected data.
- State changes are missing, stale, duplicated, or overwritten.
- CSS layout, sizing, z-index, responsive behavior, or visibility is wrong.
- A page is slow, janky, or memory-heavy.
- A bug appears only in one browser, viewport, user role, route, or environment.
- Server-rendered or hydrated apps behave differently between server and client.

## Goal

Find the smallest observable cause of the frontend bug, fix it at the right layer, and verify the behavior in the browser.

## Core Debugging Workflow

1. Reproduce the issue.
   - route/page
   - viewport/device
   - browser
   - user role/auth state
   - feature flags
   - environment
   - exact interaction steps
2. Define expected versus actual behavior.
3. Check the browser console.
   - runtime errors
   - warnings
   - failed source maps
   - hydration mismatch messages
   - security/CORS errors
   - deprecation warnings
4. Inspect the network.
   - request URL and method
   - headers and auth
   - request payload
   - status code
   - response body
   - timing waterfall
   - cache behavior
   - CORS/preflight behavior
5. Inspect DOM and CSS.
   - element exists or not
   - computed styles
   - layout boxes
   - visibility/display/opacity
   - stacking context and z-index
   - event target
   - accessibility attributes
   - responsive breakpoints
6. Inspect runtime state.
   - component props
   - local state
   - context/store values
   - query cache
   - router state
   - form state
   - feature flags
7. Use a debugger when the control flow is unclear.
8. Fix the smallest responsible layer.
9. Verify in the browser and, when appropriate, add or update tests.

## What Debuggers Tell You

A debugger shows what the running system is actually doing at a precise moment.

Use it to inspect:

- call stack: how execution reached this line
- scope variables: current local, closure, module, and global values
- object references: whether data is shared, mutated, or copied
- control flow: which branch runs
- async flow: where promises, timers, events, and callbacks resume
- event handlers: which handler fires and with what event target
- network-triggered code: what happens after a response resolves
- render timing: when state changes cause rerenders
- exceptions: where errors originate before they are caught or wrapped
- source-mapped code: original TypeScript/JSX instead of bundled output

A debugger does not directly tell you what the code should do. It tells you what it did, with the actual runtime data.

## Browser DevTools

### Console

Use for:

- errors and stack traces
- quick value inspection
- logging temporary observations
- checking global state or feature flags
- verifying event handlers fire

Avoid:

- leaving noisy logs in committed code
- using console output as the only verification when browser behavior can be inspected more directly

### Sources / Debugger

Use for:

- breakpoints
- conditional breakpoints
- logpoints
- stepping through code
- pausing on exceptions
- inspecting scope and call stack
- debugging source-mapped TypeScript/JSX

Useful breakpoint types:

- line breakpoint
- conditional breakpoint
- DOM mutation breakpoint
- event listener breakpoint
- XHR/fetch breakpoint
- exception breakpoint

### Network

Use for:

- failed API calls
- unexpected response data
- auth/session issues
- CORS and preflight failures
- caching problems
- slow requests
- duplicate requests
- missing request bodies or headers

### Elements

Use for:

- DOM structure
- computed CSS
- layout and box model
- hidden/offscreen elements
- event listeners
- accessibility tree clues
- responsive styling

### Application / Storage

Use for:

- cookies
- localStorage/sessionStorage
- IndexedDB
- service workers
- cache storage
- auth/session persistence
- stale client-side data

### Performance

Use for:

- slow rendering
- long tasks
- layout thrashing
- expensive scripts
- blocking network or CPU work
- scroll/input jank

### Memory

Use for:

- memory leaks
- detached DOM nodes
- growing object retainers
- accidental global references
- unbounded caches or subscriptions

## Common Frontend Bug Categories

### Runtime Errors

Symptoms:

- blank screen
- error overlay
- console stack trace
- component fails to render

Strategy:

- read the first meaningful stack frame
- inspect the value that is null/undefined/wrong
- trace where that value came from
- add defensive handling only if the missing value is valid domain behavior

### Network/Data Bugs

Symptoms:

- loading forever
- stale data
- wrong data
- authorization failure
- duplicate requests

Strategy:

- inspect request and response
- compare API contract to frontend assumptions
- inspect query cache/store
- verify loading/error/success states
- check environment base URLs and auth headers

### State Bugs

Symptoms:

- UI does not update
- UI reverts
- duplicated items
- stale form values
- race conditions

Strategy:

- inspect state before and after event
- trace ownership of state
- check async updates and closures
- verify controlled vs uncontrolled inputs
- check cache invalidation or optimistic update rollback

### DOM/CSS/Layout Bugs

Symptoms:

- element hidden, clipped, misaligned, unclickable, overflowing, or behind another element

Strategy:

- inspect computed styles and layout boxes
- check parent containers
- check stacking contexts and z-index
- check pointer-events
- check responsive breakpoints
- verify text fits at target viewports

### Event Bugs

Symptoms:

- click does nothing
- wrong item clicked
- event fires twice
- parent handler fires unexpectedly

Strategy:

- inspect event listeners
- set event listener breakpoints
- check propagation and default behavior
- inspect event target/currentTarget
- check disabled overlays or pointer-events

### Performance Bugs

Symptoms:

- slow interactions
- jank
- long load
- high CPU
- memory growth

Strategy:

- record performance profile
- identify long tasks
- inspect rerenders
- reduce work per interaction
- batch/defer expensive work
- virtualize large lists
- memoize only after measuring
- reduce bundle and network cost

### Hydration / SSR Bugs

Symptoms:

- server HTML differs from client
- content flashes or changes after load
- hydration warnings
- event handlers not attached

Strategy:

- compare server-rendered HTML with client state
- avoid non-deterministic rendering during SSR
- guard browser-only APIs
- verify data available on both server and client
- check locale/time/randomness differences

## Framework Tooling

Use framework-native tools when available:

- React DevTools: props, state, hooks, context, component tree, profiler
- Vue Devtools: component state, events, Pinia/Vuex stores
- Angular DevTools: components, dependency injection, change detection
- Svelte Devtools: component state and events where available
- Next.js/Nuxt/SvelteKit tooling: routing, server/client boundaries, hydration behavior
- Redux/Zustand/Apollo/React Query tools: store/query cache and action history

Prefer these tools when the bug is about component state, render flow, cache state, or framework lifecycle.

## Output Standard

Start with:

- reproduction steps
- expected behavior
- actual behavior
- observed evidence
- likely failing layer

When reporting debugger findings, include:

- breakpoint or tool used
- runtime value observed
- call stack or event path if relevant
- why that observation explains the bug

When fixing, include:

- the smallest responsible code change
- browser verification performed
- tests added or updated when appropriate

## Guardrails

- Do not guess without reproducing when reproduction is feasible.
- Do not patch symptoms before identifying the failing layer.
- Do not trust source code alone when runtime values can be inspected.
- Do not leave temporary console logs or debugger statements.
- Do not assume backend failure without inspecting the network request.
- Do not assume CSS failure without inspecting computed styles and layout.
- Do not memoize frontend code for performance without profiling first.
- Prefer browser verification for user-facing UI bugs.
