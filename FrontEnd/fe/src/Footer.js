import Cookie from 'js-cookie';
import './CSS/Footer.css'; 

export function Footer(props){

    const logOut = ()=>{
        Cookie.remove("tl-token"); // user logged out here
        window.location.href = '/';
    }

    return(<>
    
        <footer>
            <div class="username">{props.username}</div>
            <button class="logout-btn" onClick={logOut}>Logout</button>
        </footer>
    
    </>)
}