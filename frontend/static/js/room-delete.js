const roomDeleteForm = document.getElementById("room-delete-form");
const roomNameInput = document.getElementById("room-name");
const capacityInput = document.getElementById("capacity");
const errorMessage = document.getElementById("error-message");
const logoutButton = document.getElementById("logout-button");

// 削除対象の会議室idを取得
const roomId = Number(roomDeleteForm.dataset.roomId);

// エラーメッセージを表示
function showError(message) {
  errorMessage.textContent = message;
}

// JWTを削除してログイン画面に移動
function redirectToLogin() {
  sessionStorage.removeItem("access_token");
  window.location.href = "/login";
}

// 削除対象の会議室情報を取得して表示
async function loadRoom() {
  errorMessage.textContent = "";

  const accessToken = sessionStorage.getItem("access_token");

  if (!accessToken) {
    redirectToLogin();
    return;
  }

  if (!Number.isInteger(roomId) || roomId <= 0) {
    showError("会議室IDを取得できませんでした。");
    roomDeleteForm.hidden = true;
    return;
  }

  // JWTをつけて会議室情報の取得
  try {
    const response = await fetch(`/rooms/${roomId}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (response.status === 401) {
      redirectToLogin();
      return;
    }

    if (response.status === 403) {
      showError("この会議室を削除する権限がありません。");
      roomDeleteForm.hidden = true;
      return;
    }

    if (response.status === 404) {
      showError("会議室が見つかりませんでした。");
      roomDeleteForm.hidden = true;
      return;
    }

    if (!response.ok) {
      showError("会議室情報の取得に失敗しました。");
      return;
    }

    const room = await response.json();

    roomNameInput.value = room.room_name;
    capacityInput.value = room.capacity;
  } catch (error) {
    showError("通信エラーが発生しました");
  }
}
// 削除フォームの送信時の処理
roomDeleteForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorMessage.textContent = "";

  const accessToken = sessionStorage.getItem("access_token");

  if (!accessToken) {
    redirectToLogin();
    return;
  }

  
  try {
// JWTをつけて会議室を削除
    const response = await fetch(`/rooms/${roomId}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (response.status === 401) {
      redirectToLogin();
      return;
    }

    if (response.status === 403) {
      showError("この会議室を削除する権限がありません");
      roomDeleteForm.hidden = true;
      return;
    }

    if (response.status === 404) {
      showError("会議室が見つかりませんでした");
      return;
    }

    if (!response.ok) {
      const errorData = await response.json();
      showError(errorData.detail || "会議室情報の削除に失敗しました");
      return;
    }

// 削除成功後、会議室一覧画面に移動
    window.location.href = "/room";
  } catch (error) {
    console.error("会議室情報の削除中にエラーが発生しました:", error);
    showError("通信エラーが発生しました");
  }
});

// ログアウト処理
if (logoutButton) {
  logoutButton.addEventListener("click", () => {
    sessionStorage.removeItem("access_token");
    window.location.href = "/login";
  });
}

loadRoom();