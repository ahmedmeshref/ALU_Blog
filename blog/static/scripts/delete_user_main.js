

document.getElementById("delete_user_btn").onclick =

//
//
//     function (){
//     let result = confirm("Are you sure to delete?");
//     if(result){
//         delete_user()
//     }
// }


function delete_user() {
    let data = document.getElementById("delete_user_btn").value;
    [user_id, admin_type] = data.match(/[0-9]+/g);
    if (admin_type != 2) {
        alert("Method is not allowed");
        reutrn;
    }
    let article = document.getElementById(`${user_id}`);
    article.remove();
}