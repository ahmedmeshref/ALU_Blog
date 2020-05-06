// delete existing posts
function delete_post(post_id){
    let result = confirm("Are you sure?");
    if (result) {
        let post_container = document.getElementById(`${post_id}`);
        post_container.remove()
        return send_request(post_id);
    } else {
        return;
    }
}

function send_request(post_id) {
    console.log("Post card is deleted successfully")
    fetch(`${window.origin}/posts/delete_post`, {
        method: "POST",
        body: JSON.stringify({
            "post_id": post_id
        }),
        headers: {
            'Content-type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(resVal => console.log(`id: ${resVal['id']}, title: ${resVal['title']} `))
    .catch(err => console.log(err))

}