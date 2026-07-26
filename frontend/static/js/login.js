const registerForm = document.getElementById("login-form");
const errorMessage = document.getElementById("error-message");
// ログインフォームの送信処理
registerForm.addEventListener("submit", async(event) =>{
    event.preventDefault();

    errorMessage.textContent="";
    // 入力値を取得
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // OAuth2PasswordRequestForm用の送信データ
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    try {
        // ログインAPIへ入力内容を送信
        const response = await fetch("/auth/login",{
            method:"POST",
            headers:{
                "Content-Type" :"application/x-www-form-urlencoded",
            },
            body: formData,
        });

        // JSONは一度だけ読み取る
        const data = await response.json();

        if (!response.ok){
            errorMessage.textContent =
                data.detail || "ログインに失敗しました" ;
            return;

        }
         // JWTを一時保存
        sessionStorage.setItem(
            "access_token",
            data.access_token

        );

        window.location.href ="/room";

    }catch(error){
        errorMessage.textContent = 
             "通信エラーが発生しました。もう一度お試しください。"

    }
});