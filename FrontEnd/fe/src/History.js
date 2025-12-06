import './CSS/popup.css';

import { useEffect, useState } from "react";
import { get_Requests } from './Utilities/Request';

export function History(props){

    const [history, setHistory] = useState(null);

    //___________________Reall all Boards______________________

    const read_Task_history = async()=>{
        let result = await get_Requests(`api/Boards/Tasks/History/?task_id=${props.task_id}&board_id=${props.board_id}` , {"content-type" : "application/json" , "X-token" : props.token});
        setHistory(result);
    }
    useEffect(()=>{read_Task_history()}, []); // extract all boards from Database

    return(<>
        <div id="popup-overlay">
            <div class="popup-box" style={{width:"70%", height:"fit-content", textAlign:"left"}}>
                {
                    history!==null &&
                    history.map((x,index)=>
                        <div style={{padding:"10px", marginTop:"5px", background:"rgba(0,0,0,0.1)", borderRadius:"5px"}}>
                            <div>
                                Event_id : <span>{x.event_id}</span>
                            </div>
                            <div>
                                Action : <span>{x.action}</span>
                            </div>
                            <div>
                                Description : <span>{x.data.description}</span>
                            </div>
                            <div>
                                Time : <span>{x.data.updated_at.split('T')[0]}</span>
                            </div>
                            <div>
                                Applied By : <span>{x.data.updated_by_userName}</span>
                            </div>
                            <div>
                                Status : <span>{x.data.status}</span>
                            </div>
                        </div>
                    )
                }

                <button class="cancel-btn" onClick={()=>{props.closeHandler()}}>Close</button>
            </div>
        </div>
    
    </>)
}