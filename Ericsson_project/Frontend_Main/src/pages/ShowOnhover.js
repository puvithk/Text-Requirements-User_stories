import React, {useState} from "react";
import png from "./close.png"
export default function ShowButtonHover() {
    const [style, setStyle] = useState({display: 'Block'});

    return (
        <div className="App">
            <div className="closeButton" style={{padding: 10, margin: 100}}
                 onMouseEnter={e => {
                     setStyle({display: 'block'});
                 }}
                 onMouseLeave={e => {
                     setStyle({display: 'none'})
                 }}
            >
                <img src={png} alt="img"></img>
                <button style={style}>Close will delete all the file</button>
            </div>
        </div>
    );
}