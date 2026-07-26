const roomList = document.getElementById("room-list");
const errorMessage = document.getElementById("error-message");
const logoutButton = document.getElementById("logout-button");

async function fetchRooms() {
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
            errorMessage.textContent =
                "会議室情報の取得に失敗しました。";
            return;
        }

        const rooms = await response.json();
        roomList.textContent = "";

        rooms.forEach((room) => {
            const roomCard = document.createElement("div");
            roomCard.className = "col-md-6 col-lg-4";

            roomCard.innerHTML = `
                <div class="card h-100">
                    <div class="card-body">
                        <h2 class="h5 card-title"></h2>
                        <p class="card-text"></p>

                        <div class="d-flex gap-2">
                            <a
                                href="/room/${room.id}/edit"
                                class="btn btn-outline-primary btn-sm"
                            >
                                編集
                            </a>

                            <a
                                href="/room/${room.id}/delete"
                                class="btn btn-outline-danger btn-sm"
                            >
                                削除
                            </a>
                        </div>
                    </div>
                </div>
            `;

            roomCard.querySelector(".card-title").textContent =
                room.room_name;

            roomCard.querySelector(".card-text").textContent =
                `定員：${room.capacity}人`;

            roomList.appendChild(roomCard);
        });
    } catch (error) {
        errorMessage.textContent =
            "通信エラーが発生しました。";
    }
}
if (logoutButton){
     logoutButton.addEventListener("click", () => {
         sessionStorage.removeItem("access_token");
         window.location.href = "/login";
     });

}

fetchRooms();