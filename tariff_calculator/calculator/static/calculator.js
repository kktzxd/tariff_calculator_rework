function check_square(square){
    try{
        square = Number(square)
        if (square == NaN)
            return false;
        return true;
    }
    catch{
        return false;
    }
}
function get_date_from_str(_date){
    _date = _date.split(".");
    let day = _date[0];
    let month = _date[1];
    let year = _date[2];
    let new_date = new Date(year,month,day);
    return new_date
}
function check_dates(start, end){
    if (end < start){
        return false;
    }
    return true
}
function get_inputs(){
    let start = document.getElementById("start_date")
    let end = document.getElementById("end_date")
    let square = document.getElementById("square");
    let params = {
        "start_date":start.value,
        "end_date":end.value,
        "square":square.value
    }
    return params
}
// function calculate(){
//     let params = get_inputs()
//     // let url = "http://10.10.5.24:8008/get_payment_cost/";
//     let url = "/get_payment_cost/"; // для локалки
//     let request = new XMLHttpRequest();
//     request.open("POST", url, false);
//     request.setRequestHeader("Content-Type", "application/json");
//     request.send(JSON.stringify(params));
//     let response = JSON.parse(request.responseText);
//     let payment = response["payment"]

//     let result = document.getElementById('result')
//     result.textContent = payment + " руб."
// }

async function calculate() {
    let params = get_inputs();
    let url = "/get_payment_cost/";

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(params)
        });

        if (!response.ok) {
            throw new Error("Ошибка при получении данных: " + response.status);
        }

        const data = await response.json();
        const payment = data.payment;

        let result = document.getElementById("result");
        result.textContent = payment + " руб.";
    } catch (error) {
        console.error("Ошибка:", error);
        let result = document.getElementById("result");
        result.textContent = "Ошибка при расчёте";
    }
}
