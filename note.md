# Fix List

這份文件記錄了在開發過程中發現的問題和需要改進的功能。請根據以下清單進行修復和改進。

## 已知bug
   - 登入測試黃色條小bug
   - 無痕模式無法使用第三方登入
   - Oauth更改密碼問題

## 疑問
   - api內容是否要更直觀
   - 購物車跟第三方導入衝突測試
   - csrf_token
   - 使用者名稱是否無法更改

## 未解決問題（避開）
   - 上傳圖片問題

## 待優化功能
   - race condition
   - 圖片格式統一
   - 自動化上傳商品
   - 除錯處理
   - api完善
   - email驗證
   - 全部程式碼整理乾淨
   - 多張商品圖
   - 不同規格商品

### 待開發功能
   - 一開始手機號碼可以隨便輸入，但若是跟已認證的衝突要顯示
   - 支付金流
   - 臉書Oauth
   - 定期清理撤下圖片庫
   - 上aws部署
   - session是什麼
   - 客製化後台
   - csrf_token
   - 瀏覽紀錄
   - context-processors
   - 商店方後台使用

### 功能測試
   - 完整訂單
   - 後台CRUD
   - 多人購買

### 已優化
   -

## 已修復問題
   - 0元訂單
   - SOCIALACCOUNT_PROVIDERS settings(後台重複)
   - google github Oauth帳號連結
   - settings sensitive data