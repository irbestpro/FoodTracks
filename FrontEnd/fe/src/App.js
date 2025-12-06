import { Login } from "./Login";
import { SignUp } from './Register';
import { Panel } from './Panel';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

export function App(){
    return(<>
        <BrowserRouter>
            <Routes>

                {/*______________Routes_________________*/}

                <Route path = "/" element = {<Login />}></Route>
                <Route path = "/Register" element = { <SignUp /> }></Route>
                <Route path = "/Panel" element = { <Panel /> }></Route>

            </Routes>
        </BrowserRouter>
    </>)
}