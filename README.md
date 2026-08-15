# RewardGacha

習慣化のごほうびをガチャとして引けるモバイルアプリ。
毎日の行動をこなすとガチャを回せて、レアリティ付きのアイテムと、それに紐づくブログ記事が当たる。

「ごほうびが確率で当たる」という不確実性を挟むことで、習慣を続けるモチベーションを維持することを狙った個人開発プロジェクト。

## 構成

```
RewardGacha/
├── back/          FastAPI 製 API サーバー
│   └── src/
│       ├── routes/       エンドポイント定義
│       ├── services/     抽選ロジック・アイテム登録
│       ├── models/       SQLModel によるテーブル定義
│       ├── storage/      S3 / MinIO を切り替えるストレージ層
│       ├── cli/          CSV からのアイテム一括登録
│       └── middleware/   API キー認証
└── front/         Expo (React Native) 製アプリ
    └── src/app/   expo-router によるルーティング
```

## 技術スタック

| レイヤー | 使用技術 |
| --- | --- |
| バックエンド | Python 3.10 / FastAPI / SQLModel / Pydantic Settings |
| データベース | PostgreSQL（開発初期は SQLite） |
| ストレージ | AWS S3 + CloudFront（ローカルは MinIO） |
| フロントエンド | TypeScript / React Native 0.76 / Expo SDK 52 / expo-router |
| デプロイ | Render（バックエンド） |

## 設計上の判断

### ストレージを抽象化して S3 と MinIO を差し替え可能にした

アイテム画像は本番では S3 + CloudFront から配信するが、ローカル開発のたびに AWS へ接続するのは避けたかった。
`StorageClient` のインターフェースを切り、環境変数 `STORAGE_TYPE` で S3 / MinIO を差し替える形にしている。
アプリケーションコードはどちらを使っているか知らない。

### 抽選を「レアリティ抽選 → アイテム抽選」の2段階にした

1回の重み付き抽選でアイテムを直接選ぶと、レアリティごとの排出率がアイテム数に引きずられる（SSR のアイテムを増やすと SSR が出やすくなってしまう）。
先にレアリティを引き、そのレアリティの中でアイテムを引く2段階にすることで、排出率とラインナップを独立して調整できるようにした。

- レアリティの重み: `Rarity.weight`（SSR: 3 / SR: 27 / …）
- 同一レアリティ内の重み: `GachaTypeItemLink.weight`（ガチャタイプごとに設定）

### DB を SQLite から PostgreSQL へ移行した

初期は開発速度を優先して SQLite を使っていたが、Render 上ではファイルシステムが永続化されないため PostgreSQL に移行した。
SQLModel を使っていたので、接続 URL の切り替えとマイグレーションのみで済んでいる。

### API キーと User-Agent による認証

このアプリの API は公開ブラウザからではなく自作アプリからのみ叩かれる前提のため、ユーザー認証ではなくアプリ認証を採用した。
`X-API-Key` ヘッダーと User-Agent の組み合わせをミドルウェアで検証している。
ヘルスチェック `/health` のみ認証対象外（Render のコールドスタート確認用）。

なお、User-Agent は容易に詐称できるため、これは「意図しない直接アクセスを減らす」レベルの対策であり、機密性のある処理を守る想定はしていない。

## セットアップ

### バックエンド

```bash
cd back
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # 各値を環境に合わせて設定
python -m src.scripts.init_db   # レアリティ等の初期データ投入
uvicorn main:app --reload --port 9000
```

### フロントエンド

```bash
cd front
npm install
npx expo start
```

## アイテムの一括登録

`back/src/master/` 配下の CSV を順に読み込み、アイテムと画像を洗い替えで登録する。

```bash
python -m src.cli.register_items
```

CSV のパース（`utils/csv_parser.py`）、バリデーション（`validators/item_validator.py`）、
登録処理（`services/gacha_item.py`）を分離しているので、入力形式が変わってもパーサの差し替えで済む。

## API

| メソッド | パス | 説明 |
| --- | --- | --- |
| GET | `/gacha/pull?gacha_type={name}` | 指定ガチャタイプから1回抽選する |
| GET | `/health` | ヘルスチェック（認証不要） |

## 今後の課題

- 自動テストが未整備。抽選ロジックの確率分布はテストで担保したい
- 習慣の記録機能はフロント側で試作中（`feature/habit-home-screen`、`feature/habit-sqlite-storage`）
- 複数回抽選（10連）の API 対応
