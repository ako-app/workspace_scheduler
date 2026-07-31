const bookingDeleteForm = document.getElementById("booking-delete-form");
const roomNameInput = document.getElementById("room-name");
const startAtInput = document.getElementById("start-at");
const endAtInput = document.getElementById("end-at");
const reservedNumInput = document.getElementById("reserved-num");
const errorMessage = document.getElementById("error-message");
const logoutButton = document.getElementById("logout-button");

// 削除対象のIDを取得
const bookingId = Number(bookingDeleteForm.dataset.bookingId);

// エラーメッセージを表示
function showError(message){
    errorMessage.textContent = message;
}

// JWTを削除してログイン画面へ移動
function redirectToLogin(){
    sessionStorage.removeItem("access_token");
    window.location.href= "/login";
}

// 会議室一覧を取得
async function fetchRooms(accessToken){
    try {
        const response = await fetch("/rooms/",{
            method: "GET",
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        });
        if (response.status === 401){
            redirectToLogin();
            return null;
        }
        if (!response.ok){
            showError("会議室情報の取得に失敗しました");
            return null;
        }

        const rooms = await response.json()
        return rooms;
    } catch(error){
        console.error("会議室情報の取得中にエラーが発生しました", error);
        showError("通信エラーが発生しました")
        return null;
    }
}
// 削除対象の予約情報を取得して表示
 async function  loadBooking() {
    errorMessage.textContent = "";

    const accessToken = sessionStorage.getItem("access_token");

    if (!accessToken) {
    redirectToLogin();
    return;
    }
    if (!Number.isInteger(bookingId) || bookingId <=0) {
        showError("予約IDを取得できませんでした。");
        bookingDeleteForm.hidden = true;
        return;
    }
    try {
         // 会議室一覧を取得
        const rooms = await fetchRooms(accessToken);
        if (rooms === null){
            return;
        }
        // 削除対象の予約情報を取得
        const response = await fetch(`/bookings/${bookingId}`,{
            method: "GET",
            headers: {
                Authorization: `Bearer ${accessToken}`,
                }
            },
        );
        if (response.status === 401) {
            redirectToLogin();
            return;
        }

        if (response.status === 403) {
            showError(
            "この予約を確認する権限がありません。"
        );
        bookingDeleteForm.hidden = true;
        return;
        }

        if (response.status === 404) {
        showError(
        "お探しの予約が見つかりませんでした。"
        );
        bookingDeleteForm.hidden = true;
        return;
        }
        if (!response.ok) {
        showError("予約情報の取得に失敗しました。");
        return;
        }

        const booking = await response.json();
        // 予約のroom_idと一致する会議室を探す
        const room = rooms.find(
            (room) => room.id === booking.room_id
        );
        // 削除対象の予約情報を画面へ表示
        roomNameInput.value = room
        ? room.room_name : `会議室ID: ${booking.room_id}`;

        startAtInput.value = booking.start_at.slice(0, 16);

        endAtInput.value = booking.end_at.slice(0, 16);

        reservedNumInput.value = booking.reserved_num;

    } catch(error) {
    console.error("予約情報の取得中にエラーが発生しました:", error);
    showError("通信エラーが発生しました。");
   }

}

// 削除フォームの送信時の処理
bookingDeleteForm.addEventListener("submit",async(event) =>{
    event.preventDefault();
    errorMessage.textContent="";
     const accessToken = sessionStorage.getItem("access_token");
     if (!accessToken){
        redirectToLogin();
        return;
     }

     try{
        // JWTをつけて予約を削除
        const response = await fetch(`/bookings/${bookingId}`,{
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${accessToken}`
            }
        });
        if (response.status === 401){
            redirectToLogin();
            return;
        }
        if (response.status === 403) {
            showError("この予約を削除する権限がありません");
            bookingDeleteForm.hidden = true;
            return 
        }
        if (response.status === 404) {
            showError("予約が見つかりませんでした");
            bookingDeleteForm.hidden = true;
            return;
        }
        if (!response.ok) {
            showError("予約削除に失敗しました");
            return;
        }
        // 削除成功後、予約一覧画面に移動
         window.location.href = "/booking";
     } catch(error){
        console.error("予約削除中にエラーが発生しました", error);
        showError("通信エラーが発生しました");
     }

});

// ログアウトボタン
if (logoutButton){
    logoutButton.addEventListener("click",() =>{
        sessionStorage.removeItem("access_token");
        window.location.href = "/login";
    });
}

loadBooking();







