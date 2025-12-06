import './CSS/Boards.css'; 
import Cookie from 'js-cookie';
import { Tasks } from './Tasks';
import { useEffect, useMemo, useRef, useState } from 'react';
import { get_Requests, post_Requests } from './Utilities/Request';

export function Boards(){

    const [boards , setBoards] = useState(null); // read all Boards on server
    const [state , setState] = useState(0); // refresh the component
    const [fields , setFields] = useState(null); // refresh the component
    const [tasks , setTasks] = useState(null); // show all tasks of an individual Board
    const token = useMemo(()=>{return JSON.parse(Cookie.get('tl-token'))} , []); // extract token from cookie and convert to json object

    const title_ref = useRef(null); // handle title text box
    const field_ref = useRef(null);
    
    //___________________Reall all Boards______________________

    const read_all_boards = async()=>{
        let result = await get_Requests("api/Boards/All_Boards" , {"content-type" : "application/json" , "X-token" : token.token});
        setBoards(result);
    }
    useEffect(()=>{read_all_boards()}, [state]); // extract all boards from Database

    //_____________________Add new Board________________________

    const add_new_Board = async (e)=>{
        e.preventDefault(); // prevent loading page
        let data = Object.fromEntries(new FormData(e.target).entries());
        data['created_by'] = token.id; // add user-id as board creator
        title_ref.current.value = ''; // reset boards title text
        setFields({"board" : data , "fields" : [] }); // ready for getting fields from users
    }

    //___________Add Board's fields (Choesen Fields)_____________

    const add_new_field = (e)=>{
        e.preventDefault(); // prevent loading page
        let data = Object.fromEntries(new FormData(e.target).entries());
        let field_name = data['fieldName']; // field name
        field_ref.current.value = ''; // empty field ref

        setFields(prevState => ({
            ...prevState,
            fields: [...prevState.fields, { "field" : field_name}]  // append newItem
        }));
    }

    const remove_field = (e)=>{
        setFields(prev => ({
            ...prev,
            fields: prev.fields.filter(item => item.field !== e.target.getAttribute('value'))
        }));
    }

    //__________Save the Boards on the server_____________

    const save_Board = async()=>{
        let result = await post_Requests("api/Boards/Add_Board" , {"title" : fields['board']['title'], "created_by" : fields['board']['created_by'] , "fields_list" : fields['fields']} , token.token); // add new Board
        
        //_________Send Controller Task__________
      
        if(result !== null){
            
            let initial_data = {}; // initial Object Data

            fields['fields'].forEach(x => {
                initial_data[Object.values(x)[0]] = 'initial'; // list of desired fields
            });
    
            let obj = { // inital contrlo field
                description: "Controller",
                board_id: result,
                created_by: -1,
                status: "control",
                data : initial_data
            }   

            alert(JSON.stringify(obj))

            await post_Requests("api/Boards/Tasks/Add" , obj , token.token); // add new task to specific board
        }

        setFields(null); // re-set fields
        setState(x => x+1); // re-render the component
    }

    //________________Close Tasks Box_____________________

    const Close_Tasks = ()=>{
        setTasks(null);
    }

    return(<>

        <div className='container-fluid'>
            <div className='row'>
                <div className='col-xs-12 col-sm-12 col-md-6 col-lg-9'>
                    <h4 style={{paddingLeft:"20px", paddingTop:"10px"}}>Available Boards:</h4>
                    <div class="boards_container">
                        {
                            boards !== null &&
                            boards.map((x,index)=>
                                <div key={index} class="boards_card" onClick={()=>{setTasks({id : x.id, title : x.title})}}>
                                    <h2>{x.title}</h2>
                                    <div class="boards_count"> Created at: {x.creation_date.split('T')[0]}</div>
                                    <div class="boards_creator">Created by: {x.created_by}</div>
                                </div>
                            )
                        }

                    </div>
                </div>
                <div className='col-xs-12 col-sm-12 col-md-6 col-lg-3' style={{paddingTop:"20px"}}>
                    <div className='bards_form'>
                        <h2>Create New Board</h2>
                        <form onSubmit={add_new_Board}>
                            <label for="title">Board Title</label><br />
                            <input ref={title_ref} type="text" id="title" name="title" className='boards_input' autoComplete='off' required/>
                            <button type="submit" className='button_style'>Create</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        
        {/*_________Showing All Tasks of individual Board______________*/}
        {
            tasks !== null &&
            <Tasks close_handler = {Close_Tasks} id={tasks.id} title={tasks.title} u_id = {token.id} username = {token.username} token = {token.token}/>
        }
        {
            /*_____________Add new Fields_______________*/

            fields !== null &&
            <div className='container-fluid' id='Tasks'>
                
                <div id='Header'>
                    Manage "{fields.board.title}"" Fields!
                </div>

                {/*__________________Clear Box__________________*/}

                <div style={{padding:"20px", height:"50px"}}>
                </div>

                {/*_______________Desired Fields__________________*/}

                <div className='row' style={{height:"100%", overflowX:"hidden", padding:"20px"}}>
                    <div className='col-xs-12 col-sm-12 col-md-12 col-lg-6' style={{overflowY:"hidden", height:"auto"}}>
                        <div style={{padding:"20px", height:"50px"}}>
                            <div className='bards_form' >
                                <h2>Add desired fields here</h2>
                                <div>
                                    <form onSubmit={add_new_field}>
                                        <label for="fieldName">field Name</label><br />
                                        <input ref={field_ref} style={{width:"80%"}} type="text" id="fieldName" name="fieldName" className='boards_input' autoComplete='off' required/>
                                        <button type='submit' style={{padding:"10px", textDecoration:"none", marginLeft:"10px"}} className='button_style'>+</button>
                                    </form>
                                </div>
                                
                                <button onClick={save_Board} type="submit" className='button_style'>Create</button>
                            </div>
                        </div>
                    </div>
                
                {/*________________Add new Board__________________*/}
               
                    <div className='col-xs-12 col-sm-12 col-md-12 col-lg-5' id='Custom_Fields'>
                        {
                            fields['fields'].length === 0 &&
                            <div>
                                <span>No Custom Fields Have Been Added!</span>
                            </div>
                        }
                        {
                            fields['fields'].length > 0 &&
                            fields['fields'].map((x,index)=>
                                <div key={index} style={{marginTop:"10px"}}>
                                    <span style={{width:"50%", fontWeight:"600"}}>
                                        {
                                            Object.values(x)
                                        }
                                    </span>
                                    <span value={Object.values(x)} onClick={remove_field} style={{ width:"50%" ,cursor:"pointer", float:"right", textAlign:"right"}}>
                                        ❌
                                    </span>
                                </div>
                            )
                        }
                    </div>
                
                </div>

                <div className='footer'>
                    <div class="username"></div>
                </div>

            </div>
        }

    </>)
}