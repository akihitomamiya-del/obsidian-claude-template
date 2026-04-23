---
date: "2026-04-24"
type: note
tags:
  - tasks
  - active
---

# タスクリスト / Task List

Persistent task list. Daily notes pull from here via block embeds. Claude syncs from Google Calendar on SessionStart (if the GCal MCP and `sync-gcal.sh` hook are enabled).

**Block ID conventions**
- Calendar events: `^ev-YYMMDD-slug` (event date)
- Daily todos: `^todo-YYMMDD-slug` (date the task was added)
- `slug`: 1-3 word lowercase ASCII with hyphens (romanize non-ASCII)
- IDs never change once assigned — embeds (`![[TASKS#^ev-YYMMDD-slug]]`) stay valid even if the task moves sections or gets checked off

**Horizons**
- **今週 / This Week** — active items
- **今月 / This Month** — upcoming
- **いつか / Someday** — no deadline
- **完了 / Done** — completed items live here (move them, don't delete)

---

## 今週 / This Week

- [ ] **Example task** — short description ^todo-260424-example
- [ ] **Example event** — 4/26 (土) 14:00-15:00 ^ev-260426-example

## 今月 / This Month

- [ ] 

## いつか / Someday

- [ ] 

## 完了 / Done

- [x] **Example completed task** — what was done ^todo-260423-example-done
