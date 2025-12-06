import './CSS/Login.css';
import Cookie from 'js-cookie';
import { useState, useEffect } from 'react';
import { public_post } from './Utilities/Request';

export function SignUp(){

    const [incorrect , setIncorrect] = useState(null);

    //_______________Authentication____________________

    async function Register(e){
        e.preventDefault();
        let Data = Object.fromEntries(new FormData(e.target).entries()); // get all field from registeration form

        if (Data.password !== Data.repassword){
            setIncorrect("Password does not match the confirmation.")
        }
        else{
            delete Data.repassword; // remove repassword from JSON data
            let response = await public_post("SignUp" , Data); // send registeration data to server
            if(response.token !== null && response.token !== undefined){
                let val = JSON.stringify(response); // Stringify the token
                Cookie.set("tl-token" , val , {expires : response.exp}); // set expiration date
                window.location.href = "/Panel"; //redirect to Admin Panel
            }
            else{
                setIncorrect(response.status_code + ":" + response.detail);
            }
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
                    <h2 style={{paddingBlock : "10px"}}>Register New Account</h2>
                    <form onSubmit={Register}>

                        <label for="name">Name (FullName)</label>
                        <input type="text" name="name" placeholder="Enter FullName" required />
                        
                        <label for="username">Username</label>
                        <input type="text" name="username" placeholder="Enter username" required />

                        <label for="email">Email Address</label>
                        <input type="email" name="email" placeholder="Enter Email Address" required />

                        <label for="password">Password</label>
                        <input type="password" name="password" placeholder="Enter password" required/>

                        <label for="password">Re-Password</label>
                        <input type="password" name="repassword" placeholder="Confirm Password" required/>

                        <input type="submit" value= "Register and Enter" />

                        <div class="register">
                            Back to <a href="./">Login</a>
                        </div>

                        {/*_______________Errors_______________*/}

                        {
                            incorrect !== null &&
                            <div style={{color:"orangered" , fontSize:"18px", marginTop:"10px", paddingTop : "20px"}}>
                                {
                                    incorrect
                                }
                            </div>
                        }

                    </form>
                </div>
            </div>
        </div>
    
    </>)
}