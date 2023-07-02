const sendBtn = document.querySelector("#send-note-btn")
const knowledgeBtn = document.querySelector("#knowledge-btn")
const modalsDIV = document.querySelector(".modals")
const knowledgeDiv = document.querySelector(".knowledge-div")
const resolveINCBtn = document.querySelector("#resolve-inc-btn")
const incNumber = document.querySelector("#inc-number").value
const dropDIV = document.querySelector("#drop_zone")
const fileField = document.querySelector("#file")
const chosenFilesList = document.querySelector(".chosen-files-list")
const submitBTN = document.querySelector(".btn-submit-own")
const FILE_SIZE = 4194304


if(sendBtn){
    sendBtn.addEventListener("click", async (event) => {
        let data = new FormData()
        let contentInput = document.querySelector("#note")
        data.append('inc-number', incNumber)
        data.append('content', contentInput.value)
        contentInput.value = "";
        let response = await fetch('http://127.0.0.1:8000/inc-api/create-note', {
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
}


if(resolveINCBtn){
    resolveINCBtn.addEventListener("click", async (event) => {
        let response = await fetch('http://127.0.0.1:8000/inc-api/resolve-inc/' + incNumber, {
                        method: "GET",
                        headers: {'X-CSRFToken': csrftoken}
                        });


        data = await response.json()
        responseStatus = response.status
        console.log(responseStatus)

        if(data.status == "ok"){
            location.reload();
        }
        if(data.status == "failed"){
            document.querySelector("#knowledge-btn").style.backgroundColor = "red";
            console.log(data.details)
        }
    })
}

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
            let response = await fetch('http://127.0.0.1:8000/inc-api/add-attachment', {
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


if(knowledgeBtn){
    knowledgeBtn.addEventListener("click", e => {
        knowledgeDiv.classList.remove("hide");
        document.querySelector(".task-div").style.filter = "blur(8px)";
    })
}


if(modalsDIV){
    modalsDIV.addEventListener("click", event =>{
        if([...event.target.classList].includes("close-modal-div-btn")){
            let list = modalsDIV.children
            for (let item of list) {
                item.classList.add("hide")
            }
        document.querySelector(".task-div").style.filter = "";
        }
    })
}
