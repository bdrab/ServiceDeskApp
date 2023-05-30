const sendBtn = document.querySelector("#send-note-btn")
const startWorkBtn = document.querySelector("#start-work-btn")
const resolveINCBtn = document.querySelector("#resolve-inc-btn")

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

sendBtn.addEventListener("click", async (event) => {
    let data = new FormData()
    let contentInput = document.querySelector("#note")
    data.append('inc-number', document.querySelector("#inc-number").value)
    data.append('content', contentInput.value)
    contentInput.value = "";
    let response = await fetch('http://192.168.0.136/create-note', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrftoken},
                    body: data
                    });
    responseData = await response;
    responseStatus = await response.status;
    if(responseStatus === 200){
        location.reload();
    }

})

if (startWorkBtn){
    startWorkBtn.addEventListener("click", async (event) => {
        const incNumber = document.querySelector("#inc-number").value;
        let response = await fetch('http://192.168.0.136/start-work/' + incNumber, {
                        method: "GET",
                        headers: {'X-CSRFToken': csrftoken}
                        });
        responseData = await response;
        responseStatus = await response.status;
        if(responseStatus === 200){
            location.reload();
        }
    })
}

if(resolveINCBtn){
    resolveINCBtn.addEventListener("click", async (event) => {
        const incNumber = document.querySelector("#inc-number").value;
        let response = await fetch('http://192.168.0.136/resolve-inc/' + incNumber, {
                        method: "GET",
                        headers: {'X-CSRFToken': csrftoken}
                        });
        responseData = await response;
        responseStatus = await response.status;
        if(responseStatus === 200){
            location.reload();
        }
    })

}