async function render_preview(){
    //запрос
    let host = document.location.origin
    let lnk = document.location.pathname
	let response = await fetch(host + "/api/get_post/" + lnk.split("/")[2], {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		}
	});
	let result = await response.json();
    console.log(result)
    let img = await fetch(host + "/api/get_img/" + result["img_name"], {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		}
	});
    result["img"] = await img.json();
    let post = result;
    document.getElementById('pr_pic').setAttribute('src', post["img"]);
    let text = post["post_text"];
    let ret_text = "";
    for(let i = 0; i < text.length; i++){
        if(text[i] === "\n"){
            ret_text += "<br>"
        }
        else{
            ret_text += text[i];
        }
    }
    document.getElementById('pr_txt').innerHTML = ret_text;
    el = document.getElementById('pr_btns');
    let content = '';
    let buttons_array = post["buttons"];
    for(let i = 0; i < buttons_array.length; i++){
        content += "<div class='buttons_str_pr'>";
        for(let j = 0; j < buttons_array[i].length; j++){
            content += "<a class='pr_link' href='" + buttons_array[i][j]["link"] + "' target='_blank'>";
            content += "<div class='button_pr'><p class='btn_pr_txt'>" + buttons_array[i][j]["text"] + "</p></div></a>";
        }
        content += "</div>";
    }
    el.innerHTML = content;
}

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

ch_array = ["title1", "title2", "title3", "title4"];    //del
for(let i = 0; i < ch_array.length; i++)                //del
    chbx_array.push(false);                             //del

async function get_list_of_chanels(){
    //ебани тут запрос пж и запиши каналы в массив ch_array, удали строчки, после которых идут слэши, и раскомменть строчку в функции renders()
    for(let i = 0; i < ch_array.length; i++)
        chbx_array.push(false);
}

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

async function send_data(){
    let host = document.location.origin;
    let _id = document.location.pathname.split("/")[2];
    let chanel_ids = new Array;
    for(let i = 0; i < ch_array.length; i++)
        if(chbx_array[i])
            chanel_ids.push(ch_array[i]);
    let data_to_send = {
        "chanel_ids":  chanel_ids,
        "post_id": _id,
        "dts": dt_array
    };
    let response = await fetch(host + "/api/send_post/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data_to_send)
    });
    alert("Пост отправлен")
}