const registerForm = document.getElementById("register-form");
const errorMessage = document.getElementById("error-message");
// ユーザー登録フォームの送信処理
registerForm.addEventListener("submit", async(event) =>{
    event.preventDefault();

    errorMessage.textContent="";
    // 入力値を取得
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        // ユーザー登録APIへ入力内容を送信
        const response = await fetch("/users/",{
            method:"POST",
            headers:{
                "Content-Type" :"application/json",
            },
            body: JSON.stringify({
                username,
                password
            }),
        });
        if (!response.ok){
            const errorData = await response.json();
            errorMessage.textContent = 
               typeof errorData.detail === "string"
                   ? errorData.detail
                   : "入力内容を確認してください。" ;
            return;

        }
        window.location.href ="/login";

    }catch(error){
        errorMessage.textContent = 
             "通信エラーが発生しました。もう一度お試しください。"

    }
});