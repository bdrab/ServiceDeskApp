const sendBtn = document.querySelector("#send-note-btn")
const knowledgeBtn = document.querySelector("#knowledge-btn")
const closeKnowledgeDivBtn = document.querySelector(".close-knowledge-div-btn")
const modalsDIV = document.querySelector(".modals")
const knowledgeDiv = document.querySelector(".knowledge-div")
const startWorkBtn = document.querySelector("#start-work-btn")
const resolveINCBtn = document.querySelector("#resolve-inc-btn")
const addTagBtn = document.querySelector("#add-tag-btn")
const addTagInput = document.querySelector("#add-tag-input")
const incNumber = document.querySelector("#inc-number").value
const dropDIV = document.querySelector("#drop_zone")
const fileField = document.querySelector("#file")
const knowledgeFiles = document.querySelector("#files")
const chosenFilesList = document.querySelector(".chosen-files-list")
const submitBTN = document.querySelector(".btn-submit-own")
const addKnowledgeBTN = document.querySelector("#add-knowledge-article-btn")
const knowledgeArticleSelect = document.querySelector("#knowledge-article-select")
const knowledgeArticleSelectDiv = document.querySelector(".add-new-knowledge-article")
const sendSMSBtn = document.querySelector("#send-sms-btn")
const sendSMSDiv = document.querySelector(".send-sms-div")
const sendSMSSubmitBtn = document.querySelector("#send-sms-submit-btn")
const FILE_SIZE = 4194304


if(sendBtn){
    sendBtn.addEventListener("click", async (event) => {
        let data = new FormData()
        let contentInput = document.querySelector("#note")
        data.append('inc-number', incNumber)
        data.append('content', contentInput.value)
        contentInput.value = "";
        let response = await fetch('http://192.168.0.136/inc-api/create-note', {
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

if (startWorkBtn){
    startWorkBtn.addEventListener("click", async (event) => {
        let response = await fetch('http://192.168.0.136/inc-api/start-work/' + incNumber, {
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
        let response = await fetch('http://192.168.0.136/inc-api/resolve-inc/' + incNumber, {
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
            let response = await fetch('http://192.168.0.136/inc-api/add-attachment', {
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
                location.reload();
            }else{
                addTagInput.value = "";
                location.reload();
            }
    })
}


if(sendSMSBtn){
    sendSMSBtn.addEventListener("click", event => {
        sendSMSDiv.classList.remove("hide");
        document.querySelector(".task-div").style.filter = "blur(8px)";
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
        if([...event.target.classList].includes("close-knowledge-div-btn")){
            let list = modalsDIV.children
            for (let item of list) {
                item.classList.add("hide")
            }
        document.querySelector(".task-div").style.filter = "";
        }
    })
}


// create new knowledge article

if(knowledgeArticleSelect){
    knowledgeArticleSelect.addEventListener("change", event =>{
        if(event.target.value == "add_new"){
            knowledgeArticleSelectDiv.classList.remove("hide")
        }
        else{
            knowledgeArticleSelectDiv.classList.add("hide")
        }
    })
}

if(addKnowledgeBTN){
    addKnowledgeBTN.addEventListener("click", async e =>{
        let selectValue = knowledgeArticleSelect.value
        if(selectValue == "add_new"){
            let data = new FormData()
            data.append('name', document.querySelector("#knowledge-article-name").value)
            data.append('description', document.querySelector("#knowledge-note-description").value)
            data.append('inc-number', incNumber)


            let filesCounter = Array.from(knowledgeFiles.files).length
            if(filesCounter != 0){
                Array.from(knowledgeFiles.files).forEach(element => {
                    data.append('file', element)
                })}


            let response = await fetch('http://192.168.0.136/inc-api/create-knowledge-article', {
                            method: "POST",
                            headers: {'X-CSRFToken': csrftoken},
                            body: data
                            });
            response = await response
            responseStatus = response.status

            if(responseStatus === 200){
                location.reload();
                document.querySelector("#knowledge-article-name").value = ""
                document.querySelector("#knowledge-note-description").value = ""
            }else{
                location.reload();
                document.querySelector("#knowledge-article-name").value = ""
                document.querySelector("#knowledge-note-description").value = ""
            }
        }else if(selectValue != ""){
            let data = new FormData()
            data.append('inc-number', incNumber)
            data.append('article-number', selectValue)

            let response = await fetch('http://192.168.0.136/inc-api/add-knowledge-article', {
                            method: "POST",
                            headers: {'X-CSRFToken': csrftoken},
                            body: data
                            });
            response = await response
            console.log(response)
            responseStatus = response.status
            if(responseStatus == 200){
                let articlesDiv = document.querySelector("#knowledge-article-selected");
                const h6 = document.createElement("h6");
                const textNode = document.createTextNode(knowledgeArticleSelect.selectedOptions[0].text);
                h6.appendChild(textNode);
                articlesDiv.appendChild(h6);
            }
        }
    })
}

if(sendSMSSubmitBtn){
    sendSMSSubmitBtn.addEventListener("click", async event=>{
        let data = new FormData()
        data.append('text', document.querySelector("#sms-message").value)
        data.append('phones', document.querySelector("#sms-number").value)

        let response = await fetch("http://192.168.0.130/sms", {
                        method: "POST",
                        body: data
                        });
        response = await response
        console.log(response)
        responseStatus = response.status
        if(responseStatus == 200){
            console.log("sms has been sent")
        }else{
            console.log("sms has not been sent")
        }
    })
}