import Cookie from 'js-cookie';
import { useState, useEffect } from 'react';
import { Boards } from './Boards';
import { Footer } from './Footer';

export function Panel(){

    const [username, setUserName] = useState(null)

    //______Redirect Users to Authentication page if token is not valid______

    useEffect(()=> {
        let token = Cookie.get("tl-token"); // does token exist?
        token = token === undefined ? window.location.href = "/" : JSON.parse(token); // convert to Json object
        setUserName(token.username);
    }, []);

    return(<>
        <Boards />
        <div style={{padding:"20px", height:"80px"}}></div>
        <Footer username = {username !== null && username}/>
    </>)


}