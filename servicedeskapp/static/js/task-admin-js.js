const sendBtn = document.querySelector("#send-note-btn")
const startWorkBtn = document.querySelector("#start-work-btn")
const resolveINCBtn = document.querySelector("#resolve-inc-btn")
const addTagBtn = document.querySelector("#add-tag-btn")
const addTagInput = document.querySelector("#add-tag-input")
const incNumber = document.querySelector("#inc-number").value


sendBtn.addEventListener("click", async (event) => {
    let data = new FormData()
    let contentInput = document.querySelector("#note")
    data.append('inc-number', incNumber)
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






// Attachments below

const dropDIV = document.querySelector("#drop_zone")
const fileField = document.querySelector("#file")
const chosenFilesList = document.querySelector(".chosen-files-list")
const submitBTN = document.querySelector(".btn-submit")
const FILE_SIZE = 4194304


if(fileField){
    fileField.addEventListener("change", event => {
        chosenFilesList.textContent = "";
        [...fileField.files].forEach(item =>{
            if (item.size <= FILE_SIZE){
                const li = document.createElement("li");
                chosenFilesList.append(li);
                li.textContent = item["name"];
            }
        })
    })
}
if(dropDIV){
    dropDIV.addEventListener("drop", event => {
        event.preventDefault();
        let formData = new FormData();
        let dataTransfer = new DataTransfer();
        if (event.dataTransfer.items) {
            [...event.dataTransfer.items].forEach(item => {
                const file = item.getAsFile();
                if (file.size <= FILE_SIZE){
                        dataTransfer.items.add(file);
                }
            })
        fileField.files = dataTransfer.files;
        fileField.dispatchEvent(new Event("change"))
      }
})
    dropDIV.addEventListener("dragover", event => {
      event.preventDefault();
    })
}
if(submitBTN){
    submitBTN.addEventListener("click", async event => {
        let filesCounter = Array.from(fileField.files).length
        if(filesCounter != 0){
            let data = new FormData()
            data.append('incident', incNumber)
            Array.from(fileField.files).forEach(element => {
                data.append('file', element)
            })
            let response = await fetch('http://192.168.0.136/add-attachment', {
                            method: "POST",
                            headers: {'X-CSRFToken': csrftoken},
                            body: data
                            });

            responseStatus = await response.status

            if(responseStatus === 200){
                chosenFilesList.textContent = "Uploaded successfully!";
                fileField.files = (new DataTransfer()).files;

            }else{
                chosenFilesList.textContent = "Uploaded failed!";
                fileField.files = (new DataTransfer()).files;
            }
        }
    })
}

if(addTagBtn){
    addTagBtn.addEventListener("click", async event => {

            let data = new FormData()
            data.append('inc-number', incNumber)
            data.append('tag-name', addTagInput.value)
            if(addTagInput.value === ""){
                return
            }

            let response = await fetch('http://192.168.0.136/inc-api/create-tag', {
                            method: "POST",
                            headers: {'X-CSRFToken': csrftoken},
                            body: data
                            });

            responseStatus = await response.status

            if(responseStatus === 200){
                addTagInput.value = "";

            }else{
                addTagInput.value = "";
            }
}
)

}
