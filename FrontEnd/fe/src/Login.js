import './CSS/Login.css';
import Cookie from 'js-cookie';
import { useState, useEffect } from 'react';
import { public_post } from './Utilities/Request';

export function Login(){

    const [cookieState , Set_Cookie_State] = useState(Cookie.get('tl-token')); // set to initial value 
    const [incorrect , setIncorrect] = useState(null);

    //___________Check the Cookie at first_____________

     useEffect(()=>{ 
        if (cookieState !== undefined){ //check whether the token is empty or null?
            window.location.href = "/Panel"; //redirect to Admin Panel
        }
    } ,[cookieState]);

    //_______________Authentication____________________

    async function Authenticate(e){
        e.preventDefault();
        let Data = Object.fromEntries(new FormData(e.target).entries()); // get all field from Login form
        let response = await public_post("Authenticate" , Data); // send login data to server

        if(response === null || response.status_code === 401){
            setIncorrect(true); // username and/or password is incorrect
        }
        else{
            let val = JSON.stringify(response); // Stringify the token
            Set_Cookie_State(Cookie.set("tl-token" , val , {expires : response.exp})); // set expiration date and redirect to Admin Panel
        }
    }


    return(<>

        <div class="login_register_container">

            {/*_______________Left Section__________________*/}

            <div class="left">
                RealTime To Do List
            </div>

            {/*_______________Right Section__________________*/}

            <div class="right">
                <div class="login-box">
                    <h2>Login</h2>
                    <form onSubmit={Authenticate}>
                        <label for="username">Username</label>
                        <input type="text" name="username" placeholder="Enter username" required />

                        <label for="password">Password</label>
                        <input type="password" name="password" placeholder="Enter password" required/>

                        <input type="submit" value= "Login" />

                        <div class="register">
                            Havn't Registered yet? <a href="./Register">Register Now</a>
                        </div>
                        
                        {/*____________Password is Incorrect_______________*/}

                        {
                            incorrect !== null &&
                            <div style={{color:"orangered" , fontSize:"18px", marginTop:"10px", paddingTop : "20px"}}>
                                UserName and/or Password is incorrect!
                            </div>
                        }
                    </form>
                </div>
            </div>
        </div>
    
    </>)
}