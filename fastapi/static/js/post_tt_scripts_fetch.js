//Эта по идее не нужна
async function send_dt(){
    let host = document.location.origin;
    let _id = document.location.pathname.split("/")[2];
    let date = document.getElementById("date").value;
    let time = document.getElementById("time").value;
    let data_to_send = {
        "chanel_id": 1827662376,
        "post_id": _id,
        "date": date,
        "time": time
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

ch_array = ["title1", "title2", "title3", "title4"];    //del
for(let i = 0; i < ch_array.length; i++)                //del
    chbx_array.push(false);                             //del

async function get_list_of_chanels(){
    //ебани тут запрос пж и запиши каналы в массив ch_array, удали строчки, после которых идут слэши, и раскомменть строчку в функции renders()
    for(let i = 0; i < ch_array.length; i++)
        chbx_array.push(false);
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