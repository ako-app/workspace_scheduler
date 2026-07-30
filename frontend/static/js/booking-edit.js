const bookingEditForm = document.getElementById("booking-edit-form");
const roomIdSelect = document.getElementById("room-id");
const startAtInput = document.getElementById("start-at");
const endAtInput = document.getElementById("end-at");
const reservedNumInput = document.getElementById("reserved-num");
const errorMessage = document.getElementById("error-message");
const logoutButton = document.getElementById("logout-button");

// 更新対象の予約IDを取得
const bookingId = Number(bookingEditForm.dataset.bookingId);

// エラーメッセージを表示
function showError(message) {
  errorMessage.textContent = message;
}

// JWTを削除してログイン画面へ移動
function redirectToLogin() {
  sessionStorage.removeItem("access_token");
  window.location.href = "/login";
}

// 会議室一覧を取得して選択肢へ追加
async function fetchRooms(accessToken) {
  try {
    const response = await fetch("/rooms/", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (response.status === 401) {
      redirectToLogin();
      return false;
    }

    if (!response.ok) {
      showError("会議室情報の取得に失敗しました。");
      return false;
    }

    const rooms = await response.json();

    rooms.forEach((room) => {
      const option = document.createElement("option");
      option.value = room.id;
      option.textContent = room.room_name;
      roomIdSelect.appendChild(option);
    });

    return true;
  } catch (error) {
    console.error("会議室情報の取得中にエラーが発生しました:", error);
    showError("通信エラーが発生しました。");
    return false;
  }
}

// 更新対象の予約情報を取得して表示
async function loadBooking() {
  errorMessage.textContent = "";

  const accessToken = sessionStorage.getItem("access_token");

  if (!accessToken) {
    redirectToLogin();
    return;
  }

  if (!Number.isInteger(bookingId) || bookingId <= 0) {
    showError("予約IDを取得できませんでした。");
    bookingEditForm.hidden = true;
    return;
  }

  try {
    // 会議室一覧を先に取得
    const roomsLoaded = await fetchRooms(accessToken);

    if (!roomsLoaded) {
      return;
    }

    // 編集対象の予約情報を取得
    const response = await fetch(`/bookings/${bookingId}`, {
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
      showError("この予約を編集する権限がありません。");
      bookingEditForm.hidden = true;
      return;
    }

    if (response.status === 404) {
      showError("お探しの予約が見つかりませんでした。");
      bookingEditForm.hidden = true;
      return;
    }

    if (!response.ok) {
      showError("予約情報の取得に失敗しました。");
      return;
    }

    const booking = await response.json();

    // 既存の予約情報を入力欄へ表示
    roomIdSelect.value = booking.room_id;
    startAtInput.value = booking.start_at.slice(0, 16);
    endAtInput.value = booking.end_at.slice(0, 16);
    reservedNumInput.value = booking.reserved_num;
  } catch (error) {
    console.error("予約情報の取得中にエラーが発生しました:", error);
    showError("通信エラーが発生しました。");
  }
}

// 更新フォーム送信時の処理
bookingEditForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorMessage.textContent = "";

  const accessToken = sessionStorage.getItem("access_token");

  if (!accessToken) {
    redirectToLogin();
    return;
  }

  const roomId = Number(roomIdSelect.value);
  const startAt = startAtInput.value;
  const endAt = endAtInput.value;
  const reservedNum = Number(reservedNumInput.value);

  // 入力値の確認
  if (!Number.isInteger(roomId) || roomId <= 0) {
    showError("会議室を選択してください。");
    return;
  }

  if (!startAt || !endAt) {
    showError("開始日時と終了日時を入力してください。");
    return;
  }

  if (startAt >= endAt) {
    showError("終了日時は開始日時より後にしてください。");
    return;
  }

  if (!Number.isInteger(reservedNum) || reservedNum <= 0) {
    showError("予約人数は1以上の整数で入力してください。");
    return;
  }

  try {
    const response = await fetch(`/bookings/${bookingId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify({
        room_id: roomId,
        start_at: startAt,
        end_at: endAt,
        reserved_num: reservedNum,
      }),
    });

    if (response.status === 401) {
      redirectToLogin();
      return;
    }

    if (response.status === 403) {
      showError("この予約を編集する権限がありません。");
      return;
    }

    if (response.status === 404) {
      showError("予約が見つかりませんでした。");
      return;
    }

    if (!response.ok) {
      const errorData = await response.json();
      showError(errorData.detail || "予約情報の更新に失敗しました。");
      return;
    }

    window.location.href = "/booking";
  } catch (error) {
    console.error("予約情報の更新中にエラーが発生しました:", error);
    showError("通信エラーが発生しました。");
  }
});

// ログアウト処理
if (logoutButton) {
  logoutButton.addEventListener("click", () => {
    sessionStorage.removeItem("access_token");
    window.location.href = "/login";
  });
}

// 画面表示時に予約情報を取得
loadBooking();