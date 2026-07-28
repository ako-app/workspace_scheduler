const roomRegistrationForm = document.getElementById("room-registration-form");

const roomNameInput = document.getElementById("room-name");

const capacityInput = document.getElementById("capacity");

const errorMessage = document.getElementById("error-message");

const logoutButton = document.getElementById("logout-button");


roomRegistrationForm.addEventListener(
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

        const roomName = roomNameInput.value.trim();
        const capacity = Number(capacityInput.value);

        try {
            const response = await fetch("/rooms/", {
                method: "POST",
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
                sessionStorage.removeItem("access_token");
                window.location.href = "/login";
                return;
            }

            if (!response.ok) {
                const errorData = await response.json();

                errorMessage.textContent =
                    errorData.detail
                    || "会議室の登録に失敗しました。";

                return;
            }

            window.location.href = "/room";
        } catch (error) {
            errorMessage.textContent =
                "通信エラーが発生しました。";
        }
    }
);


if (logoutButton) {
    logoutButton.addEventListener("click", () => {
        sessionStorage.removeItem("access_token");
        window.location.href = "/login";
    });
}

