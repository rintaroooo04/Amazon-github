# 🍼 Amazon 出産準備お試しBOX 在庫通知ツール

Amazonの「出産準備お試しBOX」が在庫ありになったとき、自動でメール通知するツールです。  
**GitHub Actions を使うため、PCを常時起動する必要はありません（完全無料）。**

---

## 📁 ファイル構成

```
your-repo/
├── check_stock.py                       # 在庫チェック本体
└── .github/
    └── workflows/
        └── check_stock.yml              # GitHub Actions 設定（30分ごとに自動実行）
```

---

## 🚀 セットアップ手順

### 1. GitHubリポジトリを作成

1. [GitHub](https://github.com) にログイン（アカウントがなければ無料作成）
2. 右上の「＋」→「New repository」
3. リポジトリ名（例: `amazon-stock-checker`）を入力して「Create repository」

### 2. ファイルをアップロード

作成したリポジトリに以下の2ファイルをアップロードします：

- `check_stock.py` → リポジトリのルート
- `check_stock.yml` → `.github/workflows/` フォルダ内

> `.github/workflows/` フォルダはGitHub上で「Add file」→「Create new file」で  
> ファイル名に `.github/workflows/check_stock.yml` と入力すると自動作成されます。

### 3. Gmailのアプリパスワードを取得

通常のGmailパスワードではなく「アプリパスワード」が必要です。

1. Googleアカウントにログイン → [セキュリティ設定](https://myaccount.google.com/security)
2. **2段階認証を有効化**（必須）
3. 検索バーで「アプリパスワード」と検索 → 新しいアプリパスワードを生成
4. 生成された **16文字のパスワード** をメモ（スペースなしで保存）

### 4. GitHubにシークレットを登録

リポジトリの `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

| シークレット名 | 値 |
|---|---|
| `GMAIL_USER` | 送信元のGmailアドレス（例: yourname@gmail.com） |
| `GMAIL_APP_PASS` | 手順3で取得した16文字のアプリパスワード |
| `NOTIFY_EMAIL` | 通知を受け取りたいメールアドレス |

### 5. 動作確認

1. GitHubリポジトリの「Actions」タブを開く
2. 「Amazon 出産準備BOX 在庫チェック」ワークフローを選択
3. 「Run workflow」→「Run workflow」で手動実行
4. 緑のチェックマークが出れば成功！

---

## ⚙️ カスタマイズ

### チェック頻度を変える

`check_stock.yml` の `cron` を編集：

```yaml
# 毎時0分・30分（デフォルト：30分おき）
- cron: "0,30 * * * *"

# 毎時0分（1時間おき）
- cron: "0 * * * *"

# 毎時0分・15分・30分・45分（15分おき）
- cron: "0,15,30,45 * * * *"
```

> ⚠️ GitHub Actionsの無料枠は月2,000分まで。15分おきにすると月約3,000分かかるため  
> 30分おきが安全です。

---

## ❓ よくある質問

**Q: 通知メールが来ない**  
→ Actionsタブでエラーログを確認。シークレットの設定ミスが多い原因です。

**Q: 在庫ありなのに通知が来ない**  
→ Amazonのページ構造が変わった可能性があります。`check_stock.py` の  
　`out_of_stock_keywords` を調整してみてください。

**Q: Gmailが使えない**  
→ Yahoo!メールやOutlookでも同様の手順でアプリパスワードを取得できます。  
　`check_stock.py` の SMTP設定を変更してください。
