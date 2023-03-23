function render_posts(q){
    let posts = document.getElementById('posts');
    for(let i = 0; i < q.length; i++){
        console.log(q[i]);

        posts.innerHTML += "<a href='calendar/"+ q[i][Object.keys(q[i])[0]] + "'><div class='post_in_list'><p>" + q[i][Object.keys(q[i])[1]] + "</p></div></a>";
        ///posts.innerHTML += "<p>" + q[i][Object.keys(q[i])[0]]  + "</p>";
    }
}

let loC = new Array;
loC = [{"_id": 0, "name": "title0", "tg_id": 1000000000, "ref": "ref0", "cond": "const"},
       {"_id": 1, "name": "title1", "tg_id": 1000000001, "ref": "ref1", "cond": "const"},
       {"_id": 2, "name": "title2", "tg_id": 1000000002, "ref": "ref2", "cond": "const"},
       {"_id": 3, "name": "title3", "tg_id": 1000000003, "ref": "ref3", "cond": "const"}
      ]; //эту хуйню надо удалить, это я для себя делал

function render_chanels_ws(){
    let el = document.getElementById("ins_ch");
    let content = "";
    for(let i = 0; i < loC.length; i++){
        content += "<div id='chws" + String(i) + "'>";
        content += "<input type='text' value='" + loC[i]["name"] + "' id='name" + String(i) + "'" + (loC[i]["cond"] == "const" ? "readonly" : "") + " onchange='change_field(this.id)'>";
        content += "<input type='text' value='" + loC[i]["tg_id"] + "' id='tgid" + String(i) + "'" + (loC[i]["cond"] == "const" ? "readonly" : "") + " onchange='change_field(this.id)'>";
        content += "<input type='text' value='" + loC[i]["ref"] + "' id='refc" + String(i) + "'" + (loC[i]["cond"] == "const" ? "readonly" : "") + " onchange='change_field(this.id)'>";
        content += "<input type='button' id='chng" + String(i) + "' value='Изм.' onclick='modify_chanel(this.id)'>";
        content += "<input type='button' id='delt" + String(i) + "' value='X' onclick='delete_chanel(this.id)'></div>";
    }
    el.innerHTML = content;
    for(let i = 0; i < loC.length; i++){
        if(loC[i]["cond"] == "const")
            document.getElementById("chws" + String(i)).setAttribute("class", "chanel_ws_const");
        else if(loC[i]["cond"] == "delete")
            document.getElementById("chws" + String(i)).setAttribute("class", "chanel_ws_delete");
        else if(loC[i]["cond"] == "modify")
            document.getElementById("chws" + String(i)).setAttribute("class", "chanel_ws_modify");
        else if(loC[i]["cond"] == "add")
            document.getElementById("chws" + String(i)).setAttribute("class", "chanel_ws_add");
    }
}

function modify_chanel(id_str){
    let id_s = "";
    for(let i = 4; i < id_str.length; i++)
        id_s += id_str[i];
    let id_n = Number(id_s);
    console.log(id_s);
    if(loC[id_n]["cond"] == "const" || loC[id_n]["cond"] == "delete")
        loC[id_n]["cond"] = "modify";
    render_chanels_ws();
}

function delete_chanel(id_str){
    let id_s = "";
    for(let i = 4; i < id_str.length; i++)
        id_s += id_str[i];
    let id_n = Number(id_s);
    if(loC[id_n]["cond"] != "add")
        loC[id_n]["cond"] = "delete";
    else
        loC.splice(id_n, 1);
    render_chanels_ws();
}

function comp(a, b){
    return(a - b);
}

function add_chanel(){
    let all_ids = new Array;
    for(let i = 0; i < loC.length; i++)
        all_ids.push(loC[i]["_id"]);
    all_ids.sort(comp);
    let new_id = 0;
    let it = 0;
    while(true){
        if(new_id < all_ids[it])
            break;
        else if(new_id == all_ids[it]){
            new_id++;
            it++;
        }
        else
            it++;
        if(it == all_ids.length)
            break;
    }
    loC.push({"_id": new_id, "name": "", "tg_id": -1, "ref": "", "cond": "add"});
    render_chanels_ws();
}

function change_field(id_str){
    let id_s = "";
    for(let i = 4; i < id_str.length; i++)
        id_s += id_str[i];
    let id_n = Number(id_s);
    let type = "";
    for(let i = 0; i < 4; i++)
        type += id_str[i];
    if(type == "name")
        loC[id_n]["name"] = document.getElementById(id_str).value;
    else if(type == "tgid")
        loC[id_n]["tg_id"] = document.getElementById(id_str).value;
    else if(type == "refc")
        loC[id_n]["ref"] = document.getElementById(id_str).value;
}

function renders(){
    render_chanels_ws();
    get_p();
}

function save_changes(){
    let delete_array = new Array;
    let modify_array = new Array;
    let add_array = new Array;
    for(let i = 0; i < loC.length; i++){
        if(loC[i]["cond"] == "delete")
            delete_array.push(loC[i]["_id"]);
        else if(loC[i]["cond"] == "modify")
            modify_array.push({"_id": loC[i]["_id"], "name": loC[i]["name"], "tg_id": loC[i]["tg_id"], "ref": loC[i]["ref"]});
        else if(loC[i]["cond"] == "add")
            add_array.push({"_id": loC[i]["_id"], "name": loC[i]["name"], "tg_id": loC[i]["tg_id"], "ref": loC[i]["ref"]});
    }
    let data_to_send = {
        "delete": delete_array,
        "modify": modify_array,
        "add": add_array
    };
    send_save_changes(data_to_send);
}