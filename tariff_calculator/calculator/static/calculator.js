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
        "start_date":start,
        "end":end,
        "square":square
    }
    return params
}
function calculate(){
    let params = get_inputs()
    let url = "http://10.10.5.24:8008/calculate";
    let request = new XMLHttpRequest();
    request.open("GET", url, false);
    request.setRequestHeader("Content-Type", "application/json");
    request.send(JSON.stringify(params));
    console.log(request.status);
    console.log(request.responseText);
}