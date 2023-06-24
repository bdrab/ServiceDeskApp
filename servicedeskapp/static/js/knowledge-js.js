const tagsDiv = document.querySelector(".tags-div")
const categoriesDiv = document.querySelector(".categories-div")
const incDiv = document.querySelector(".incs-div")
const filesDiv = document.querySelector(".files-div")
const selectInput = document.querySelector("#id_search_type")
const btnControlDiv = document.querySelector(".btn-control-div")
const searchDiv = document.querySelector(".search-div")
const articlesDiv = document.querySelector(".knowledge-articles-div")
const articlesNameDiv = document.querySelector(".articles-name-div")



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
        document.querySelector(".knowledge-div").classList.remove("hide")
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
        document.querySelector(".knowledge-div").classList.remove("hide")
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

btnControlDiv.addEventListener("click", async event => {
    if(event.target.type == "button"){
        for(let item of btnControlDiv.children){
            item.classList.remove("selected");
        }
        if(event.target.value == "knowledge-btn"){
            event.target.classList.add("selected");
            searchDiv.classList.add("hide")
            articlesDiv.classList.remove("hide")
        }else if(event.target.value == "btn-search-tag-category"){
            event.target.classList.add("selected");
            searchDiv.classList.remove("hide")
            articlesDiv.classList.add("hide")
        }else{}
    }
})

articlesNameDiv.addEventListener("click", async event => {
    if([...event.target.classList].includes("article")){
        document.querySelector(".article-details").classList.remove("hide")
        let articleID = event.target.dataset["pk"]
        let response = await fetch('http://192.168.0.136/inc-api/knowledge_article/' + articleID, {
                    headers: {'X-CSRFToken': csrftoken},
                    });
        data = await response.json()
        let files = data.files;
        responseStatus = response.status

        if(responseStatus == 200){
            document.querySelector(".article-name").innerText = data.name;
            document.querySelector(".article-description").innerText = data.description;
            document.querySelector(".article-files").innerHTML = "";
            let counter = 1;
            files.forEach(file => {
                let newDIV = document.createElement("div");
                newDIV.setAttribute("class", "file-div")

                let aElement = document.createElement("a");
                aElement.setAttribute("href", file)
                aElement.innerText = "File " + counter
                counter ++;

                newDIV.appendChild(aElement);
                document.querySelector(".article-files").appendChild(newDIV);
            })
        }
    }
})
