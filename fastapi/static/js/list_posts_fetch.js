async function get_p() {
    let host = document.location.origin
    let r = await fetch(host + '/api/posts', {
        method: "GET",
        headers: {
            'accept': 'application/json'
        }
    });
    let q = await r.json();
    render_posts(q);
}