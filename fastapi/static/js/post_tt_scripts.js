let dt_array = new Array;

function render_dt(){
    let dt_row = document.getElementById('dt_row');
    let content = "";
    for(let i = 0; i < dt_array.length; i++){
        content += "<div class='dt'>";
        content += "<input type='date' id='date" + String(i) + "' value='" + dt_array[i]['date'] + "' onchange='dt_change(this.id)'>";
        content += "<input type='time' id='time" + String(i) + "' value='" + dt_array[i]['time'] + "' onchange='dt_change(this.id)'>";
        content += "<input type='button' value='X' id = '" + String(i) + "' onclick='del_dt(this.id)'></div>";
    }
    dt_row.innerHTML = content;
}

function dt_change(id_str){
    let id_s = "";
    for(let i = 4; i < id_str.length; i++)
        id_s += id_str[i];
    id_n = Number(id_s);
    let date = document.getElementById('date' + id_s).value;
    let time = document.getElementById('time' + id_s).value;
    let dt = {"date": date, "time": time};
    dt_array[id_n] = dt;
}

function add_dt(){
    dt_array.push({"date": "", "time": ""});
    render_dt();
}

function del_dt(id_s){
    let id_n = Number(id_s);
    dt_array.splice(id_n, 1);
    render_dt();
}

let ch_array = new Array;
let chbx_array = new Array;

function render_chbxs(){
    let el = document.getElementById('ch');
    content = "";
    for(let i = 0; i < ch_array.length; i++){
        content += "<div class='ch_chbx'>";
        content += "<input type='checkbox' id='chbx" + String(i) + "' onchange='chbx_change(this.id)'";
        if(chbx_array[i])
            content += " checked";
        content += "><label for='chbx" + String(i) + "'>" + ch_array[i] + "</label></div>";
    }
    el.innerHTML = content;
}

function chbx_change(id_str){
    let id_s = "";
    for(let i = 4; i < id_str.length; i++)
        id_s += id_str[i];
    let id_n = Number(id_s);
    chbx_array[id_n] = Boolean(1 - chbx_array[id_n]);
    render_chbxs();
}

function choose_all(){
    for(let i = 0; i < ch_array.length; i++)
        chbx_array[i] = true;
    render_chbxs();
}

function clear_all(){
    for(let i = 0; i < ch_array.length; i++)
        chbx_array[i] = false;
    render_chbxs();
}

function renders(){
    //get_list_of_chanels();
    render_preview();
    render_chbxs();
}