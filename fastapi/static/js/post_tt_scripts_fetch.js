async function get_preview(){
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
    render_preview(post);
}


async function get_list_of_chanels(){
    let host = document.location.origin;
    //let response = await fetch(host + "/api/get_channels/", {
    let response = await fetch(host + "/api/get_channels_array/", {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    let q = await response.json();
    ch_array = q;
    //ебани тут запрос пж и запиши каналы в массив ch_array, удали строчки, после которых идут слэши, и раскомменть строчку в функции renders()
    for(let i = 0; i < ch_array.length; i++)
        chbx_array.push(false);
}

async function _send_data(data_to_send){
    let host = document.location.origin;
    console.log(data_to_send)
    let response = await fetch(host + "/api/create_tasks/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data_to_send)
    });
    alert("Пост отправлен")
}