import Cookie from "js-cookie";
export const server = 'http://localhost:8000/';

//___________________Check results______________________

const result_Checker = (response)=>{ // works like a session
    if (response !== null && response.detail === "Token is Invalid"){ // invalid token
        Cookie.remove("tl-token"); // remove the token from cookie
        window.location.href = "/";
    }
    else
        return response;
}

export async function public_post(url , data){
    try{
        let result = await fetch(server + url , {"method" : "post" , headers : {"content-type" : "application/json"} , body : JSON.stringify(data)});
        let response = await result.json(); // response from server
        return result_Checker(response);    
    }
    catch{
        return null;
    }
}

export async function post_Requests(url , data , token){
    try{
        let result = await fetch(server + url , {"method" : "post" , headers : {"X-Token" : token , "content-type" : "application/json"} , body : JSON.stringify(data)});
        let response = await result.json(); // response from server
        return result_Checker(response);    
    }
    catch{
        return null;
    }
}

export async function get_Requests(url , header){
    try{
        let result = header === null ? await fetch(server + url) : await fetch(server + url , {headers : header});
        let response = await result.json(); // response from server
        return result_Checker(response);
    }
    catch{
        return null;
    }
}