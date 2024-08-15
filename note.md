# Fix List

這份文件記錄了在開發過程中發現的問題和需要改進的功能。請根據以下清單進行修復和改進。

## 已知bug
   ## 商品類
   - upload function 選擇圖片問題
   - 快速點兩次bug
   - 商品分頁
   ## 訂單類

   ## 支付類

   ## 帳號類
   - 亂填已驗證過的email
   - 不能用的功能不要show
   - 登入頁面新增註冊
   - admin管理帳號衝突(merge account)
   - 無痕模式無法使用第三方登入
   - github 無法使用第三方登入
   - ngrok 無法使用第三方登入
   - Oauth更改密碼問題
   - 使用者名稱是否無法更改
   - google登入可以跳過使用者名稱
   - github要填使用者名稱
   - ACCOUNT_LOGIN_REDIRECT_URL
   - 瀏覽器紀錄在哪裡
   ## 運營以及其他
   - 最底部標

## 部署注意
   - debug = off

## 疑問
   - api統一
   - 購物車跟第三方導入next衝突測試

## 未解決問題

### 待優化功能
   ## 商品類
   - 上架下架
   - 圖片格式統一
   - 多張商品圖
   - 不同規格商品
   - 商品排序
   - 加入購物車不要跳轉
   - 購物車歸零跳通知
   - 商品數量眾多翻頁問題
   - 優惠碼折價券
   ## 訂單類
   - 未付款n天後刪除訂單
   - race condition
   - 接上地址功能(google map,7-11,全家)
   ## 支付類

   ## 帳號類
   - email認證後才能使用？
   ## 運營以及其他
   - 除錯處理
   - api完善
   - api頁面 swagger test

### 待開發功能
   ## 商品類
   - 定期清理撤下圖片庫

   ## 訂單類

   ## 支付類
   - 支付金流extra function like email notify
   ## 帳號類
   - 密碼上碼
   - 一開始手機號碼可以隨便輸入，但若是跟已認證的衝突要顯示
   - 臉書Oauth
   - Line Oauth
   - csrf_token
   - csrf_exempt
   - 瀏覽紀錄
   ## 運營以及其他
   - 上aws部署
   - 客製化後台
   - 多語言

### 功能測試
   - 完整訂單
   - 後台CRUD
   - 多人購買
   - 流量測試

### 已優化
   ## 商品類
   - 上傳商品腳本
   ## 訂單類

   ## 支付類

   ## 帳號類

   ## 運營以及其他

## 已修復問題
   - SOCIALACCOUNT_PROVIDERS settings(後台重複刪除即可)
   - settings sensitive data(用env)
   - paypal html問題(改用SDK)

## 特點
   - 權限管理
   - 金流支付
   - 訂單管理
   - 第三方驗證
   - 手機驗證
   - jwt信箱驗證
   - database normalization
   - 批次上架
   - 申請https,ssl
   - api請求次數
   - depoly
   - 圖片進s3
   - 圖片快取cdn