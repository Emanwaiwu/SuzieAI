import { useState } from 'react'
import  Title from './title';
import RecordMessage from './RecordMessage';
import axios from 'axios';

function controller () {
 
    const [isLoading, setIsLoading] = useState(false)
    const [messages, setMessages] = useState<any[]>([]);

    const createBlobUrl = (data: any) => {
        const blob = new Blob([data], {type: "audio/mpeg"});
        const url = window.URL.createObjectURL(blob);
        return url;
    };

    const handleStop = async(blobUrl: string) => {
        setIsLoading(true)

        //append recorded messages 

        const myMessage = {sender: "Me", blobUrl}
        const messagesArr = [...messages, myMessage]

        //convert blob url to blob obj
        fetch(blobUrl).then ((res) => res.blob()).then(async(blob) => {
            //construct audio to send file 
            const formData = new FormData();
            formData.append("file", blob, "myFile.wav")

            //send form data to api backend
            await axios.post("http://localhost:8000/post-audio", formData, {headers: {"Content-Type": "audio/mpeg"}, responseType:"arraybuffer",}).then((res:any) => {
                const blob = res.data
                const audio = new Audio();
                audio.src = createBlobUrl(blob)

                //append to audio
                const rachelMessage = {sender:"Suzie", blobUrl: audio.src}
                messagesArr.push(rachelMessage)
                setMessages(messagesArr)

                //play audio
                setIsLoading(false)
                audio.play();

            }).catch((err) => {
                console.error(err.message)
                setIsLoading(false);
            })
        })
    };

    return(
        <div className="h-screen overflow-y-hidden">
            <Title setMessages = {setMessages} />
            <div className="flex flex-col justify-between h-full overflow-y-scroll pb-96">
            
            {/*Conversation*/}
            <div className="mt-5 px-5">
                {messages.map((audio, index) => {
                    return (
                    <div key={index + audio.sender} className={"flex flex-col " + (audio.sender == "Suzie" && "flex items-end")}>

                        {/*sender*/}
                        <div className="mt-4"> 
                            <p className={audio.sender == "Suzie" ? "text-right mr-2 italic text-purple-900" : "ml-2 italic text-blue-500"}>
                                {audio.sender}
                            </p>

                            {/*AudioMessage*/}
                            <audio src={audio.blobUrl}
                            className='appearance-none'
                            controls />
                            
                        </div>
                    </div>
                    );
                })}

                {messages.length == 0 && !isLoading && (
                    <div className="text-center text-white font-light italic mt-10">
                        Talk to me. You can say anything!!
                    </div>
                )}
                {isLoading && (
                    <div className="text-center text-white font-light italic mt-10 animate-pulse">
                        Be patient, I'm responding...
                    </div>
                )}
            </div>

            {/*Recorder*/}
            <div className='fixed bottom-0 w-full py-2 text-center bg-gradient-to-r from-[#1b103084] to-[#0f1c5a8f]'>
                <div className='flex justify-center items-center w-full'>
                    <RecordMessage handleStop = {handleStop}/>
                </div>
            </div>
            </div>
        </div>
    )
}
export default controller