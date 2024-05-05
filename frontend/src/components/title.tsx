import {useState} from 'react';
import axios from "axios";


type props ={
    setMessages: any
};

function title ({setMessages}: props){
    const[isResetting, SetIsResetting] = useState(false);

    //reset the convo
    const ResetConversation = async () => {
        SetIsResetting(true);
        await axios.get("http://localhost:8000/reset") .then((res) => {
            if(res.status == 200){
                setMessages([])
            }else{
                console.error("There was an error with API request");
            }
        }).catch((err) => {
            console.error(err.message);
        });
        SetIsResetting(false);
    };

    return(
        <div className='flex justify-between items-center w-full p-4 bg-gradient-to-l from-[#1b10308d] to-[#0f1c5a66] text-white font-bold shadow'>
            <div className='text-white italic flex pl-5'>
                Suzie.AI
            </div>
            <button 
            onClick={ResetConversation}
            className={'transition-all duration-300 text-red-600 hover:text-pink-500' + (isResetting && "animate-pulse")}>
            <svg 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" viewBox="0 0 24 24" 
                strokeWidth={1.5} 
                stroke="currentColor" 
                className="w-6 h-6">
            <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
            </svg>
            </button>
        </div>
    )
}
export default title 