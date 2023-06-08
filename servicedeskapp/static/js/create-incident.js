const dropDIV = document.querySelector("#drop_zone")
const fileField = document.querySelector("#file")
const chosenFilesList = document.querySelector(".chosen-files-list")
const submitBTN = document.querySelector(".btn-submit")
const categoryINC = document.querySelector("#id_category")
const descriptionINC = document.querySelector("#id_description")
const FILE_SIZE = 4194304



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


submitBTN.addEventListener("click", async event => {
    let filesCounter = Array.from(fileField.files).length

    let data = new FormData()
    Array.from(fileField.files).forEach(element => {
        data.append('file', element)
    })
    data.append('category', categoryINC.value)
    data.append('description', descriptionINC.value)

    let response = await fetch('http://192.168.0.136/create', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrftoken},
                    body: data
                    });
    data = await response.json()
    responseStatus = response.status



    if(responseStatus === 200){
        chosenFilesList.textContent = "Uploaded successfully!";
        fileField.files = (new DataTransfer()).files;

    }else{
        chosenFilesList.textContent = "Uploaded failed!";
        fileField.files = (new DataTransfer()).files;
    }

    setTimeout(function(){
    window.location.replace("/INC" + data.number);;
    },1000);

})
