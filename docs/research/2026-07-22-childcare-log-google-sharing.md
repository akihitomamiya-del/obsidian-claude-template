---
date: 2026-07-22
type: note
tags: [research, 育児記録, google, obsidian, family-sharing]
status: draft
---

# 育児記録 × Obsidian × 妻との共有 — 方法の徹底調査

**質問**: このテンプレート(Claude管理のObsidian vault)で育児記録をつけ、妻と共有するにはどんな方法がありうるか。Googleのサービス経由を主軸に、**非Google(Obsidian自体の共有機能等)も含めて**調べる。

**調査日**: 2026-07-22。事実の確度は vault 規約に従い **Confirmed / Inferred / Speculative** で明示する。

---

## 0. 結論サマリ(先に要点)

<!-- PLACEHOLDER: 最終推奨 3案 — 調査結果確定後に記入 -->

---

## 1. 前提整理 — いま手元にあるもの

### 1.1 このテンプレートの実能力(Confirmed — 本セッションでスキーマ・実挙動を直接確認)

| 経路 | できること | できないこと |
|---|---|---|
| **Google Drive MCP** | ファイル新規作成(`create_file`)。テキストを渡すと **Googleドキュメント/スプレッドシートに自動変換**可能。`parentId` 指定で**共有済みフォルダ内に直接作成**できる(→ フォルダの共有権限を継承)。既存ファイルの読み取り(`read_file_content` — Docs/Sheets/PDF/画像対応、**コメント込み読み取り可**)。検索・コピー・権限の**閲覧**。 | **既存ファイルの更新(追記・編集)は不可**。共有権限の**付与**も不可(閲覧のみ)。→「毎日同じDocを更新」はできず、「日付き新規ファイルを共有フォルダに置く」が基本形。 |
| **Gmail MCP** | **下書き作成のみ**(宛先・件名・本文・HTML可)。下書き検索・読み取り。 | **自動送信は不可**。妻への自動配信は「下書き作成→ユーザーがワンタップ送信」まで。 |
| **Google Calendar MCP** | イベント作成・更新・削除・検索。**`calendarId` 指定で共有カレンダーに直接書き込み可**。**妻を招待者(attendee)に追加**可。繰り返しルール(RRULE)、リマインダー上書き、終日イベント対応。 | (実質フル機能) |

### 1.2 ユーザーのGoogle環境に既にある資産(Confirmed — 本セッションでMCP経由で確認)

1. **共有カレンダー「Guma&Goro」**(説明:「みのむしケアのための予定調整」、Asia/Tokyo)— 夫婦のケア調整用カレンダーが**既に存在**。Claude はここに直接イベントを作成できる。
2. **Googleドキュメント「Gem作成マニュアル(育児記録アシスタント)」**(2026-07-22 作成)— Gemini Gem を使い、音声/テキスト入力を `• [HH:MM] [絵文字] [内容]` 形式に整形して **Google Keep の日次ノート「育児記録 YYYY/MM/DD」に APPEND する**設計が既に文書化されている。絵文字規約: 🍼授乳 / 💩便 / 💧尿 / 🤮吐き戻し / 😣ぐずり / 🛁沐浴 / 😴睡眠。
3. **Drive 上の Markdown 運用実績**: 「出生後手続きガイド_京都市左京区.md」(2026-07-05)— vault 的な markdown を Drive に置いて使うパターンを既に実践中。

### 1.3 テンプレート側の受け皿(Confirmed — リポジトリ確認)

- vault に `03_Personal/Family/` が既設(git-ignore 対象なので個人内容はコミットされない)。
- 日次ノート(`04_Daily/YYYY-MM-DD.md`)+ `!TASKS/TASKS.md`(ブロックID `^ev-YYMMDD-slug` / `^todo-YYMMDD-slug` + 埋め込み)という既存の同期規約。
- SessionStart hooks(`sync-gcal.sh`, `check-vault-sync-drafts.sh` 等)= 「セッション開始時に外部ソースを取り込む」パターンが確立済み。育児記録用の hook を同型で足せる。
- claude.ai の予約実行エージェント(vault-sync 3回/日)= 定時バッチの前例あり。

### 1.4 設計フレーム — テンプレートの3層構造にそのまま乗る

このテンプレの哲学(Raw sources / Wiki / Schema)は育児記録にきれいに適用できる:

- **入力層(Raw)** = 高頻度・低摩擦の記録面。Keep・Forms/Sheets・共有カレンダー。**夫婦どちらでも書ける**ことが最重要。
- **統合層(Wiki)** = vault。Claude が入力層を取り込み、日次セクション・週次サマリー・成長記録・健診/予防接種ページに**編纂**する。
- **共有層** = 妻が見る面。入力層そのもの(Keep/Sheets/カレンダー)か、Claude が書き出す成果物(共有フォルダのDoc、メールダイジェスト)。

新生児期の授乳・おむつは 1日10回超の記録になるため、**入力層に Obsidian mobile を使わない**(起動・同期が遅い)のが現実的、という前提で各案を評価する。

---

## 2. 方法カタログ(Google経由)

<!-- PLACEHOLDER: A〜K 各方式 — 外部調査結果と統合して記入 -->

---

## 2b. 方法カタログ(非Google — Obsidian自体の共有ほか)

<!-- PLACEHOLDER: Obsidian Sync共有vault / Self-hosted LiveSync / Relay等の共同編集プラグイン / iCloud・Dropbox共有フォルダ / Syncthing / Publish / iOSショートカット入力 / Apple Notes・Notion比較 -->

---

## 3. 比較表

<!-- PLACEHOLDER -->

---

## 4. 推奨アーキテクチャ(妻の関与スタイル別 3案)

<!-- PLACEHOLDER -->

---

## 5. このテンプレートへの実装ロードマップ

<!-- PLACEHOLDER: CLAUDE.md 追記案 / hook 案 / 予約エージェント案 / vault 構造案 -->

---

## 6. リスクと注意点

<!-- PLACEHOLDER: 同期競合 / iOS制約 / Photos API変更 / プライバシー / MCP制約 -->

---

## 7. 出典

<!-- PLACEHOLDER -->
