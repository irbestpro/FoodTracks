import './CSS/Boards.css'; 
import './CSS/Footer.css'; 
import { useEffect, useState } from "react";
import { post_Requests } from './Utilities/Request';
import { MessageBox } from './messageBox';
import { History } from './History';

export function Tasks(props){

    const [tasks, settasks] = useState([]);
    const [filteretasks, setFilteredtasks] = useState([]); // for filtere tasks
    const [focused, setFocused] = useState(null); // changed task
    const [controlfields , setControlFields] = useState(null);
    const [finishTask, setFinishTask] = useState(null); // set the task to be finished
    const [history, setHistory] = useState(null); // show Task's history
    const [modifyTask, setModifyTask] = useState(null); // set the task to be modified

    //_____________Handle all Websoket's Operations________________________

    useEffect(() => {
        const websocket = new WebSocket(`ws://localhost:8000/ws/boards/${props.id}`);

        //____________Send Connection Message_________________

        websocket.onopen = () => {
            websocket.send("Get me all the tesks"); // send a new request to server to see all tasks in a board
        };

        //_________Connect and Load All the tasks_____________

        websocket.onmessage = (event) => {
            const data = JSON.parse(event.data); // create object from strigified message from server

            if(Object.keys(data).includes('data')){ // added/modified tasks
                setFocused({id : data['data']['id'] , action : data['action']}); 
                settasks(prev => {
                    const newList = [data.data, ...prev.filter(t => t.id !== data.data.id)];
                    return newList;
                });
                setFilteredtasks(prev => {
                    const newList = [data.data, ...prev.filter(t => t.id !== data.data.id)];
                    return newList;
                });
            }
            else{
                setControlFields(data.filter(x=> x.status.toLowerCase() === 'control')); // controller field
                settasks(prev => [...prev, ...data]); // load all the tasks
                setFilteredtasks(prev => [...prev, ...data]);
            }
        };

        //_________On Connection Close_____________

        websocket.onclose = () => {

        };

        return () => websocket.close(); // cleaner function

    }, []);


    //______________filter tasks___________________

    const filter = (e)=>{
        const filtered = tasks.filter(task =>
            task.status !== 'control' &&
            task.description.toLowerCase().includes(e.target.value.toLowerCase())
        );

        setFilteredtasks(filtered);
    }

    //__________Add new Task To Board_______________

    const Add_Modify_Tasks = async(e)=>{
        e.preventDefault();
        let data = Object.fromEntries(new FormData(e.target).entries()); // General Object
        let new_data = {'data' : {}}; // Object with Flexible Fields
        
        Object.keys(data).forEach(key=>{
            if(Object.keys(controlfields[0]['data']).includes(key)){
                new_data['data'] = {...new_data['data'], [key] : data[key]};
            }
            else{
                new_data[key] = data[key];
            }
        });

        if (modifyTask === null){
            await post_Requests("api/Boards/Tasks/Add" , new_data, props.token); // add new task to specific board
        }
        else{
            await post_Requests("api/Boards/Tasks/Update" , new_data, props.token); // update exist tasks
            setModifyTask(null);
        }

        //_______________Clear all boxes_________________

        let elements = document.getElementsByClassName('boards_input');
        for(let elm of elements){
            elm.value = '';
        }
    }   

    //____________Handle Message Box_______________

    const close_MessgaeBox = ()=>{
        setFinishTask(null); // close the box
        setHistory(null);
    }

    const Finish_Task = async()=>{
        let obj = finishTask;
        obj['status'] = 'finished';
        await post_Requests("api/Boards/Tasks/Update" , finishTask, props.token); // add new task to specific board
        setFinishTask(null); // close the box
    }

    return(<>

        <div className='container-fluid' id='Tasks'>
            <div className='row'>
                <div className='col-xs-12 col-sm-12 col-md-6 col-lg-9'>
                    
                    {/*_________________Filter Section__________________*/}

                    <h4 style={{paddingLeft:"20px", paddingTop:"10px"}}>
                        All Tasks of:  
                        <span style={{paddingLeft:"10px", color:"carbonblue"}}>
                            {
                                props.title
                            }
                        </span>
                        <div style={{marginTop:"10px"}}>
                            <input style={{width:"98%"}} placeholder = "Filter By Task,s Description" type="text" id="description" className='boards_input' onChange={filter}/>
                        </div>
                    </h4>

                    <div style={{color:"navy", fontSize:"20px", paddingLeft:"22px", borderBottom:"solid thin silver", paddingBottom: "20px"}}>
                        Please click on the task you want to update!
                    </div>
                    
                    {/*_________________Board's Tasks___________________*/}

                    <div class="boards_container">
                        {
                            filteretasks !== null &&
                            filteretasks.filter(x => x.status !== 'control').map((x,index)=> //).map((xx , index) => 
                                <div key={index} class="boards_card" onClick={()=>{ x.status !== 'finished' && setModifyTask(x)}} style={{border: focused !== null && focused.id === x.id ? "solid 2px #A8DCAB" : "solid 2px silver"}}>
                                    <div style={{paddingBottom:"10px"}}>
                                        <h5 style={{paddingTop:"10px", paddingBottom:"10px", borderBottom:"solid thin silver", marginBottom:"10px"}}> 
                                            <span style={{color: x.status === 'in progress' ?  "#8B5CF6" : "green" , marginTop:"-20px"}}>{x.status}</span>
                                            {
                                                x.status === 'in progress' &&
                                                <span style={{marginTop:"-20px"}} className='finished' onClick={()=>{setFinishTask(x)}}>
                                                    Mark as Finished
                                                    ✓
                                                </span>
                                            }
                                            <span style={{marginTop:"0px"}} className='finished' onClick={()=>{setHistory(x)}}>
                                                Show History
                                                ✓
                                            </span>
                                        </h5>
                                        <div class="boards_count"> <strong>Created at: </strong>{x.created_at.replace('T' ,' ')}</div>
                                        <div class="boards_creator"><strong>Created by:</strong> {x.cretaed_by_userName}</div>
                                        <div class="boards_count"> <strong>Updated at: </strong>{x.created_at.replace('T' ,' ')}</div>
                                        <div class="boards_creator"><strong>Updated by: </strong> {x.updated_by_userName}</div>
                                        
                                        {
                                            Object.keys(x['data']).length > 0 &&
                                            Object.keys(x['data']).map((key,index)=>
                                            <div class="boards_creator" key={index}>
                                                <strong> {key} : </strong>
                                                {
                                                    x['data'][key]
                                                }
                                            </div>)
                                        }
                                        
                                    </div>
                                    <div style={{paddingTop:"10px", padding:"5px", backgroundColor:"#d7d7d8", borderRadius:"5px", color:"navy"}}>
                                        {
                                            x.description
                                        }
                                    </div>
                                </div>
                            )
                        }

                    </div>
                </div>
                
                {/*_______________Add new Task_________________*/}

                <div className='col-xs-12 col-sm-12 col-md-6 col-lg-3' style={{paddingTop:"20px"}}>
                    <div className='bards_form' >
                        <h2>Add New Task</h2>
                        <form onSubmit={Add_Modify_Tasks}>

                            <input type='hidden' name='board_id' value={ modifyTask !== null ? modifyTask['board_id'] : props.id} />
                            <input type='hidden' name='created_by' value={ modifyTask !== null ? modifyTask['created_by'] : props.u_id} />
                            <input type='hidden' name='cretaed_by_userName' value={ modifyTask !== null ? modifyTask['cretaed_by_userName'] : props.username} />
                            <input type='hidden' name='updated_by_userName' value={props.username} />
                            <input type='hidden' name='status' value="in progress" />
                            {
                                modifyTask !== null &&
                                <input type='hidden' name='id' value = {modifyTask.id} />
                            }
                            
                            <label for="description">Description</label><br />
                            <input type="text" id="description" name="description" className='boards_input' autoComplete='off' required defaultValue={ modifyTask !== null ? modifyTask['description'] : ''}/>

                            {
                                modifyTask === null &&
                                filteretasks.filter(x=> x.status.toLowerCase() === 'control').map(x =>
                                    Object.keys(x['data']).map(xx =>
                                    [
                                        <label for = {xx}>{xx}</label>,<br />,
                                        <input type="text" id={xx} name= {xx} className='boards_input' autoComplete='off' required/>        
                                    ])
                                )
                            }

                            {
                                modifyTask !== null &&
                                Object.keys(modifyTask['data']).map(xx =>
                                [
                                    <label for = {xx}>{xx}</label>,<br />,
                                    <input type="text" id={xx} name= {xx} defaultValue={modifyTask['data'][xx]} className='boards_input' autoComplete='off' required/>        
                                ])
                            }

                            <button type="submit" className='button_style'>
                                {
                                    modifyTask === null &&
                                    `Create`
                                }
                                {
                                    modifyTask !== null &&
                                    `Update`
                                }
                            </button>
                            {
                                modifyTask !== null &&
                                <a href='#' style={{float:"right", textDecoration:"none", color:"#3B82F6", marginTop:"10px"}} onClick={()=>{setModifyTask(null)}}>
                                    Reset and Add new
                                </a>
                            }
                        </form>
                    </div>
                </div>
            </div>

            <div style={{padding:"20px", height:"50px"}}>

            </div>

            <div className='footer'>
                <div class="username">{filteretasks.length - 1} Tasks are Available</div>
                <button class="logout-btn" onClick={props.close_handler}>Close &times;</button>
            </div>

        </div>

        {/*_______________Finish individual Task_________________*/}

        {
            finishTask !== null &&
            <MessageBox closeHandler = {close_MessgaeBox} functionHandler = {Finish_Task} prompt = {"Are you sure you want to mark this task as finished?"} caption = {"Finish this Task?"}/>
        }

        {/*_______________Finish individual Task_________________*/}

        {
            history !== null &&
            <History closeHandler = {close_MessgaeBox} task_id = {history.id} board_id = {props.id} token = {props.token}/>
        }

        
    </>)
}