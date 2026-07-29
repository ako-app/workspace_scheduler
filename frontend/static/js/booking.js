const bookingList = document.getElementById("booking-list");
const errorMessage = document.getElementById("error-message");
const logoutButton = document.getElementById("logout-button");

// 日時を「2026/07/15 16:00」の形式に変換
function formatDateTime(dateTime) {
  return new Date(dateTime).toLocaleString("ja-JP", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

async function fetchBookings() {
  const accessToken = sessionStorage.getItem("access_token");

  if (!accessToken) {
    window.location.href = "/login";
    return;
  }

  try {
    const response = await fetch("/bookings/", {
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
      errorMessage.textContent =
        "予約情報の取得に失敗しました。";
      return;
    }

    const bookings = await response.json();
    bookingList.textContent = "";

    bookings.forEach((booking) => {
      const bookingRow = document.createElement("tr");

      bookingRow.innerHTML = `
        <td class="booking-id"></td>
        <td class="room-id"></td>
        <td class="booking-date"></td>
        <td class="reserved-num"></td>
        <td>
          <div class="d-flex gap-2">
            <a
              href="/booking/${booking.id}/edit"
              class="btn btn-outline-primary btn-sm"
            >
              編集
            </a>

            <a
              href="/booking/${booking.id}/delete"
              class="btn btn-outline-danger btn-sm"
            >
              削除
            </a>
          </div>
        </td>
      `;

      bookingRow.querySelector(".booking-id").textContent =
        booking.id;

      bookingRow.querySelector(".room-id").textContent =
        booking.room_id;

      bookingRow.querySelector(".booking-date").textContent =
        `${formatDateTime(booking.start_at)} ～ ${formatDateTime(booking.end_at)}`;

      bookingRow.querySelector(".reserved-num").textContent =
        `${booking.reserved_num}人`;

      bookingList.appendChild(bookingRow);
    });
  } catch (error) {
    console.error(
      "予約情報の取得中にエラーが発生しました:",
      error
    );

    errorMessage.textContent =
      "通信エラーが発生しました。";
  }
}

if (logoutButton) {
  logoutButton.addEventListener("click", () => {
    sessionStorage.removeItem("access_token");
    window.location.href = "/login";
  });
}

fetchBookings();