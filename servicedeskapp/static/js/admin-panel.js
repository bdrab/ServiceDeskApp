const newTaskTable = document.querySelector(".new-task-table")
const btnControlDiv = document.querySelector(".control-btn-div")

const yourWorkDiv = document.querySelector(".your-work-div")
const yourGroupWorkDiv = document.querySelector(".your-group-work-div")
const allIncDiv = document.querySelector(".all-inc-div")
const closedIncDiv = document.querySelector(".closed-inc-div")
const tablesDiv = document.querySelector(".tables")




if(newTaskTable){
    newTaskTable.addEventListener("click", async event => {
        if([...event.target.classList].includes("start-work-btn")){
            let incNumber = event.target.dataset["id"]
            let response = await fetch('http://127.0.0.1:8000/inc-api/start-work/' + incNumber, {
                           method: "GET",
                           headers: {'X-CSRFToken': csrftoken}
                           });
            responseData = await response;
            responseStatus = await response.status;
            if(responseStatus === 200){
                location.reload();
            }
        }
    })
}



btnControlDiv.addEventListener("click", async event => {
    if(event.target.type == "button"){
        removeClass(btnControlDiv, "selected")

        if(event.target.value == "your-work-btn"){
            event.target.classList.add("selected");
            addClass(tablesDiv, "hide")
            yourWorkDiv.classList.remove("hide")

        }else if(event.target.value == "your-group-work-btn"){
            event.target.classList.add("selected");
            addClass(tablesDiv, "hide")
            yourGroupWorkDiv.classList.remove("hide")

        }else if(event.target.value == "all-inc-btn"){
            event.target.classList.add("selected");
            addClass(tablesDiv, "hide")
            allIncDiv.classList.remove("hide")

        }else if(event.target.value == "closed-inc-btn"){
            event.target.classList.add("selected");
            addClass(tablesDiv, "hide")
            closedIncDiv.classList.remove("hide")
        }
    }
})

