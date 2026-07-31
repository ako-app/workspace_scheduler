const roomEditForm = document.getElementById("room-edit-form");
const roomNameInput = document.getElementById("room-name");
const capacityInput = document.getElementById("capacity");
const errorMessage = document.getElementById("error-message");
const logoutButton = document.getElementById("logout-button");

// 更新対象の会議室idを取得
const roomId = Number(roomEditForm.dataset.roomId);

// エラーメッセージを表示
function showError(message) {
  errorMessage.textContent = message;
}

// JWTを削除してログイン画面に移動
function redirectToLogin() {
  sessionStorage.removeItem("access_token");
  window.location.href = "/login";
}
// 更新対象の会議室情報を取得して表示
async function loadRoom() {
  errorMessage.textContent = "";

  const accessToken = sessionStorage.getItem("access_token");

  if (!accessToken) {
    redirectToLogin();
    return;
  }

  if (!Number.isInteger(roomId) || roomId <= 0) {
    showError("会議室IDを取得できませんでした。");
    roomEditForm.hidden = true;
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
      showError("この会議室を編集する権限がありません。");
      roomEditForm.hidden = true;
      return;
    }

    if (response.status === 404) {
      showError("会議室が見つかりませんでした。");
      roomEditForm.hidden = true;
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
    showError("通信エラーが発生しました。");
  }
}

// 更新フォームの送信時の処理
roomEditForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorMessage.textContent = "";

  const accessToken = sessionStorage.getItem("access_token");

  if (!accessToken) {
    redirectToLogin();
    return;
  }

  const roomName = roomNameInput.value.trim();
  const capacity = Number(capacityInput.value);

  if (!roomName) {
    showError("会議室名を入力してください。");
    return;
  }

  if (!Number.isInteger(capacity) || capacity <= 0) {
    showError("定員は1以上の整数で入力してください。");
    return;
  }

  try {
    const response = await fetch(`/rooms/${roomId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify({
        room_name: roomName,
        capacity: capacity,
      }),
    });

    if (response.status === 401) {
      redirectToLogin();
      return;
    }

    if (response.status === 403) {
      showError("この会議室を編集する権限がありません。");
      roomEditForm.hidden = true;
      return;
    }

    if (response.status === 404) {
      showError("会議室が見つかりませんでした。");
      return;
    }

    if (!response.ok) {
      const errorData = await response.json();
      showError(errorData.detail || "会議室情報の更新に失敗しました。");
      return;
    }

    window.location.href = "/room";
  } catch (error) {
    console.error("会議室情報の更新中にエラーが発生しました:", error);
    showError("通信エラーが発生しました。");
  }
});

// ログアウトボタン
if (logoutButton) {
  logoutButton.addEventListener("click", () => {
    sessionStorage.removeItem("access_token");
    window.location.href = "/login";
  });
}

loadRoom();