const bookingRegistrationForm = document.getElementById(
      "booking-registration-form"
);
const roomIdSelect = document.getElementById("room-id");
const startAtInput = document.getElementById("start-at");
const endAtInput = document.getElementById("end-at");
const reservedNumInput = document.getElementById("reserved-num");
const errorMessage = document.getElementById("error-message");
const logoutButton = document.getElementById("logout-button");

// 会議室一覧の選択肢を追加する
async function fetchRooms(){
    const accessToken=
          sessionStorage.getItem("access_token");

          if (!accessToken){
            window.location.href = "/login";
            return;
          }
          try {
            const response = await fetch("/rooms/", {
                headers:{
                    Authorization: `Bearer ${accessToken}`,
                },
            });
            if(response.status == 401){
                sessionStorage.removeItem("access_token");
                window.location.href="/login";
                return;
            }
            if(!response.ok){
                errorMessage.textContent=
                  "会議室情報の取得に失敗しました"
                  return;
            }
            const rooms = await response.json();
            rooms.forEach((room) =>{
                const option = document.createElement("option");
            option.value = room.id; 
            option.textContent = room.room_name;
            roomIdSelect.appendChild(option);

            });


          }catch(error){
            console.error( 
                "会議室情報の取得中にエラーが発生しました:", 
                error 
            ); 
            errorMessage.textContent = 
            "通信エラーが発生しました";
          }
}

// 予約登録処理
bookingRegistrationForm.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        errorMessage.textContent = "";

        const accessToken =
            sessionStorage.getItem("access_token");

        if (!accessToken) {
            window.location.href = "/login";
            return;
        }

        const roomId = Number(roomIdSelect.value);
        const startAt = startAtInput.value;
        const endAt = endAtInput.value;
        const reservedNum = Number(reservedNumInput.value);

        try {
            const response = await fetch("/bookings/", {
                method: "POST",
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
                sessionStorage.removeItem("access_token");
                window.location.href = "/login";
                return;
            }

            if (!response.ok) {
                const errorData = await response.json();

                errorMessage.textContent =
                    errorData.detail
                    || "予約の登録に失敗しました";

                return;
            }

            window.location.href = "/booking";
        } catch (error) {
            console.error(
                "予約登録中にエラーが発生しました",
                error

            );
            errorMessage.textContent =
                "通信エラーが発生しました";
        }
    }
);


if (logoutButton) {
    logoutButton.addEventListener("click", () => {
        sessionStorage.removeItem("access_token");
        window.location.href = "/login";
    });
}

fetchRooms();

