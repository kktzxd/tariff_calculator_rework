function delete_tariff(tariff){
    let row = tariff.parentElement;
    let values = row.getElementsByTagName("div");
    let id = values[0].textContent;
    let start_date = values[1].textContent;
    let end_date = values[2].textContent;
    let cost = values[3].textContent;
    row.remove();

    let request = new XMLHttpRequest()
    let url = `http://10.10.5.24:8008/delete_tariff/` + id + "/";

    request.open("DELETE", url, false);
    request.setRequestHeader("Content-Type", "application/json");
    request.send()
    console.log(request.status);
}

function change_tariff(tariff){
    let row = tariff.parentElement;

    let cells = row.getElementsByClassName("cell");

    let id = cells[0];
    let start_date = cells[1];
    let end_date = cells[2];
    let cost = cells[3];
    let start_date_old_value = start_date.textContent;
    let end_date_old_value = end_date.textContent;
    let cost_old_value = cost.textContent;

    let buttons = row.getElementsByTagName("button");
    for(let i = buttons.length-1; i > -1; i--){
        buttons[i].remove();
    }

    start_date.remove()
    end_date.remove()
    cost.remove()
    start_date = document.createElement("input");

    start_date.classList.add("cell");
    start_date.classList.add("start_date");

    end_date = document.createElement("input");
    end_date.classList.add("cell");
    end_date.classList.add("end_date");

    cost = document.createElement("input");
    cost.classList.add("cell");
    cost.classList.add("cost");

    row.appendChild(start_date);
    row.appendChild(end_date);
    row.appendChild(cost);

    start_date.value = start_date_old_value;
    end_date.value = end_date_old_value;
    cost.value = cost_old_value;

    let save_button = document.createElement("button");
    save_button.textContent = "Сохранить изменения";
    save_button.classList.add("button");
    save_button.addEventListener("click", () => save_changes(row));

    row.appendChild(save_button);
}
function save_changes(row){
    let inputs = row.getElementsByTagName("input");
    let start_date = inputs[0].value;
    let end_date = inputs[1].value;
    let cost = inputs[2].value;
    
    let url = "http://10.10.5.24:8008/save_tariff/";
    let params = {
        "start_date":start_date,
        "end_date":end_date,
        "cost":cost
    }
    let request = new XMLHttpRequest();
    request.open("POST", url, false);
    request.setRequestHeader("Content-Type", "application/json");
    request.send(JSON.stringify(params));
    console.log(request.status)
    if (request.status == 200){
        location.reload();
    }
    else if (request.status == 404){
        alert("Тариф не был сохранен, он не корректен")
    }

}
function add_tariff(){
    let row = document.createElement("div");
    row.classList.add("row")

    let id;
    let start_date = document.createElement("input");
    start_date.classList.add("cell");
    start_date.classList.add("start_date");
    start_date.placeholder="Начало тарифа ДД.ММ.ГГГГ";

    let end_date = document.createElement("input");
    end_date.classList.add("cell");
    end_date.classList.add("end_date");
    end_date.placeholder="Конец тарифа ДД.ММ.ГГГГ";

    let cost = document.createElement("input");
    cost.classList.add("cell");
    cost.classList.add("cost");
    cost.placeholder="Стоимость тарифа";

    row.appendChild(start_date);
    row.appendChild(end_date);
    row.appendChild(cost);

    let save_button = document.createElement("button");
    save_button.textContent = "Сохранить изменения";
    save_button.classList.add("button");
    save_button.addEventListener("click", () => save_changes(row));

    row.appendChild(save_button);

    let cancel_button = document.createElement("button");
    cancel_button.textContent="Отменить изменения"
    cancel_button.classList.add("button");
    cancel_button.addEventListener("click", () => cancel_tariff(row))

    row.appendChild(cancel_button);

    let tariffs = document.getElementById("tariffs");
    tariffs.append(row);
}
function cancel_tariff(row){
    row.remove()
}