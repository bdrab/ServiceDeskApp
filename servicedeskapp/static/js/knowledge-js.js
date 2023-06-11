const tagsDiv = document.querySelector(".tags-div")
const categoriesDiv = document.querySelector(".categories-div")
const incDiv = document.querySelector(".incs-div")
const filesDiv = document.querySelector(".files-div")
const selectInput = document.querySelector("#id_search_type")


selectInput.addEventListener("change", event => {
    if(event.target.value == "tags"){
        tagsDiv.classList.remove("hide")
        categoriesDiv.classList.add("hide")

    }else if(event.target.value == "categories"){
        categoriesDiv.classList.remove("hide")
        tagsDiv.classList.add("hide")
    }

})


tagsDiv.addEventListener("click", async event => {
    if([...event.target.classList].includes("tag")){

        let response = await fetch('http://192.168.0.136/inc-api/tags/' + event.target.innerText, {
                    headers: {'X-CSRFToken': csrftoken},
                    });

        data = await response.json()
        const tickets = data.tickets;
        const files = data.files;

        responseStatus = response.status


        if(responseStatus === 200){
        incDiv.innerHTML = ""
        filesDiv.innerHTML = ""

            if(tickets.length != 0){
                let titleDiv = document.createElement("div");
                titleDiv.setAttribute("class", "inc-title-div");
                titleDiv.innerText = "INC numbers:";
                incDiv.appendChild(titleDiv);

                tickets.forEach(element => {
                    let newDIV = document.createElement("div");
                    newDIV.setAttribute("class", "inc-div");
                    let aElement = document.createElement("a");
                    aElement.setAttribute("href", "/INC" + element.number);
                    aElement.innerText = "INC" + element.number;
                    newDIV.appendChild(aElement);
                    incDiv.appendChild(newDIV);
                })
            }

            if(files.length != 0){
                let titleDiv = document.createElement("div");
                titleDiv.setAttribute("class", "files-title-div");
                titleDiv.innerText = "Related files:";
                filesDiv.appendChild(titleDiv);

                files.forEach(element => {
                    let newDIV = document.createElement("div");
                    newDIV.setAttribute("class", "file-div")
                    let aElement = document.createElement("a");
                    aElement.setAttribute("href", element.path)
                    aElement.innerText = element.name + "." + element.extension
                    newDIV.appendChild(aElement);
                    filesDiv.appendChild(newDIV);
                })
            }
        }
    };
})

categoriesDiv.addEventListener("click", async event => {
    if([...event.target.classList].includes("category")){

        let response = await fetch('http://192.168.0.136/inc-api/categories/' + event.target.innerText, {
                    headers: {'X-CSRFToken': csrftoken},
                    });

        data = await response.json()
        const tickets = data.tickets;
        const files = data.files;

        responseStatus = response.status


        if(responseStatus === 200){
        incDiv.innerHTML = ""
        filesDiv.innerHTML = ""

            if(tickets.length != 0){
                let titleDiv = document.createElement("div");
                titleDiv.setAttribute("class", "inc-title-div");
                titleDiv.innerText = "INC numbers:";
                incDiv.appendChild(titleDiv);
                tickets.forEach(element => {
                    let newDIV = document.createElement("div");
                    newDIV.setAttribute("class", "inc-div");
                    let aElement = document.createElement("a");
                    aElement.setAttribute("href", "/INC" + element.number);
                    aElement.innerText = "INC" + element.number;
                    newDIV.appendChild(aElement);
                    incDiv.appendChild(newDIV);
                })
            }

            if(files.length != 0){
                let titleDiv = document.createElement("div");
                titleDiv.setAttribute("class", "files-title-div");
                titleDiv.innerText = "Related files:";
                filesDiv.appendChild(titleDiv);
                files.forEach(element => {
                    let newDIV = document.createElement("div");
                    newDIV.setAttribute("class", "file-div")
                    let aElement = document.createElement("a");
                    aElement.setAttribute("href", element.path)
                    aElement.innerText = element.name + "." + element.extension
                    newDIV.appendChild(aElement);
                    filesDiv.appendChild(newDIV);
                })
            }
        }
    };
})



