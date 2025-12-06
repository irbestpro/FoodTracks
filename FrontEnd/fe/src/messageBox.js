import './CSS/popup.css';

export function MessageBox(props){
    return(<>
        <div id="popup-overlay">
            <div class="popup-box">
                <h3>{props.caption}</h3>
                <p>{props.prompt}</p>

                <button class="cancel-btn" onClick={()=>{props.closeHandler()}}>Cancel</button>
                <button class="finish-btn" onClick={()=>{props.functionHandler()}} >Finish Task</button>
            </div>
        </div>
    
    </>)
}