const loginMessage = document.getElementById("login-message");
const logoutButton = document.getElementById("logout-button");

async function checkAuthentication() {
    const accessToken =
        sessionStorage.getItem("access_token");

    if (!accessToken) {
        window.location.href = "/login";
        return;
    }

    try {
        const response = await fetch("/rooms/", {
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        });

        if (response.status === 401) {
            sessionStorage.removeItem("access_token");
            window.location.href = "/login";
            return;
        }

        if (!response.ok) {
            loginMessage.textContent =
                "会議室情報の取得に失敗しました。";
            return;
        }

        loginMessage.textContent =
            "ログインしています。";
    } catch (error) {
        loginMessage.textContent =
            "通信エラーが発生しました。";
    }
}

logoutButton.addEventListener("click", () => {
    sessionStorage.removeItem("access_token");
    window.location.href = "/login";
});

checkAuthentication();