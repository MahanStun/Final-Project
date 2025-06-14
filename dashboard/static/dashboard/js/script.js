function showPanel(Divid) {
    const buttons = document.querySelectorAll(".menu-btn")
    const panels = document.querySelectorAll(".panel")


    buttons.forEach(everybtn => { everybtn.classList.remove("active-session") })
    panels.forEach(everyDiv => { everyDiv.classList.remove("active-session") })


    

    document.getElementById(Divid).classList.add("active-session")

    // console.log(buttons)
    console.log(panels)
    showTicketPanel(Divid)

}
function showTicketPanel(panelId) {
    document.querySelectorAll(".ticket-panel").forEach(function(panel){
        panel.style.display = "block";
    })
}