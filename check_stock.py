#!/usr/bin/env python3
"""
Amazon 出産準備お試しBOX 在庫チェックスクリプト
在庫あり → メール通知を送信
"""

import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# ===== 設定 =====
TARGET_URL = "https://www.amazon.co.jp/dp/B07FJVRLZ7"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ja-JP,ja;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def check_stock() -> tuple[bool, str]:
    """
    在庫状況を確認する
    Returns: (在庫あり?, ステータスメッセージ)
    """
    try:
        response = requests.get(TARGET_URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        return False, f"ページ取得エラー: {e}"

    soup = BeautifulSoup(response.text, "html.parser")

    # 「在庫なし」を示すテキストを探す
    out_of_stock_keywords = [
        "現在在庫切れ",
        "在庫切れ",
        "この商品は現在お取り扱いできません",
        "Currently unavailable",
        "Out of Stock",
    ]

    page_text = soup.get_text()
    for keyword in out_of_stock_keywords:
        if keyword in page_text:
            return False, f"在庫なし（キーワード検出: {keyword}）"

    # カートに追加ボタンの存在確認
    add_to_cart = soup.find("input", {"id": "add-to-cart-button"})
    buy_now = soup.find("input", {"id": "buy-now-button"})

    if add_to_cart or buy_now:
        return True, "カートに追加ボタンを検出 → 在庫あり！"

    # 追加のチェック: availability テキスト
    availability_div = soup.find("div", {"id": "availability"})
    if availability_div:
        avail_text = availability_div.get_text(strip=True)
        if "在庫あり" in avail_text or "通常" in avail_text:
            return True, f"在庫あり（availability: {avail_text[:50]}）"
        return False, f"在庫状況不明（availability: {avail_text[:50]}）"

    return False, "在庫確認できず（ボタン・availability要素が見つからない）"


def send_email(subject: str, body: str):
    """Gmail SMTP でメール送信"""
    gmail_user = os.environ["GMAIL_USER"]      # 送信元Gmailアドレス
    gmail_pass = os.environ["GMAIL_APP_PASS"]  # Googleアプリパスワード
    to_email = os.environ["NOTIFY_EMAIL"]      # 通知先メールアドレス

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = to_email

    html_body = f"""
    <html><body>
    <h2 style="color:#e47911;">🍼 Amazon 出産準備お試しBOX 在庫情報</h2>
    <p>{body}</p>
    <p><a href="{TARGET_URL}" style="background:#e47911;color:white;padding:10px 20px;
       text-decoration:none;border-radius:4px;">今すぐAmazonで確認する</a></p>
    <hr>
    <small>通知時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}</small>
    </body></html>
    """

    msg.attach(MIMEText(body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_pass)
        server.sendmail(gmail_user, to_email, msg.as_string())

    print(f"✅ メール送信完了 → {to_email}")


def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 在庫チェック開始...")

    in_stock, status = check_stock()
    print(f"結果: {status}")

    if in_stock:
        subject = "🎉【在庫あり】Amazon 出産準備お試しBOX が購入できます！"
        body = (
            f"Amazon 出産準備お試しBOX の在庫が確認されました！\n\n"
            f"ステータス: {status}\n\n"
            f"今すぐ購入ページを確認してください:\n{TARGET_URL}"
        )
        send_email(subject, body)
        sys.exit(0)
    else:
        print("在庫なし → 通知スキップ")
        sys.exit(0)


if __name__ == "__main__":
    main()
