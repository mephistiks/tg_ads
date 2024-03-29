async function send_media(file){
	let host = document.location.origin;
	let response = await fetch(host + "/api/v2/upload", {
		method: 'POST',
		headers: {
			'accept': 'application/json'
			//'Content-Type': 'multipart/form-data'
		},
		body: file
	});
	console.log(response);
	let result = await response.text();
	console.log(result);
	return result;
}

async function send_post_post(post_body){
    let host = document.location.origin;
	let response = await fetch(host + "/api/v2/create", {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(post_body)
	});
	let result = await response.json();

	var mydiv = document.getElementById("new_post");

	mydiv.innerHTML = "<a href = " + host + "/calendar/" + result + "> "+post_body["post_name"]+"</a>";

}