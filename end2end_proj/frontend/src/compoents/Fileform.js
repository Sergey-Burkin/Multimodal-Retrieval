import { useState } from "react";
import API from "../API";


const FileForm = () => {
    const [file, setFile] = useState(null);
    const [help_info, setInfo] = useState(null);
    const [text, setText] = useState(null);
    const [is_not_auth, setAuthState] = useState(false);


    const handleFileInputChange = (event) => {
        setFile(event.target.files[0]);
    }
    const handleTextInputChange = (event) => {
        setText(event.target.value);
    }

    const handleSubmit = async (event) => {
        setAuthState(false);
        event.preventDefault();
        console.log("It is handleSubmit")

        const formData = new FormData();
        formData.append('file', file);

        try {
            // const endpoint = "http://127.0.0.1:8000/send_file";
            // const endpoint = "http://127.0.0.1:8000/send_query";

            // const res = await fetch(endpoint, {
            //     method: "POST",
            //     bode: formData,
            // })
            // const headers = {'Content-Type': file.type}
            let config = {
                headers: {
                    'Access-Control-Allow-Origin': true,
                    'Content-Type': file.type
                },
                params: {
                    "token": localStorage.getItem('accessToken'),
                    'text_query': text,
                }
            }

            // console.log(formData);
            // console.log("----------------------------------------")
            console.log(config)
            // console.log(text)
            // const res = await axios.post(endpoint, formData, config);
            const res = await API.post("/send_query", formData, config);

            console.log("It is try");
            if (res.data.status_code === 200) {
                setInfo(res.data.ans);
                // console.log("Ok")
                // console.log(res);
            } else {
                // console.error(res);
                console.error("Not auth");
                setAuthState(true);
                // console.log("Not ok")
                // console.error(res);
            }
            console.log("set help info")
            // console.log(help_info);
        } catch(error) {
            setAuthState(true);
            // console.log("It is catch")
            console.error(error);
            console.error("Not auth");
        }
    }

    return (
        <div>

            <h2>Upload File</h2>

            <form onSubmit={handleSubmit}>
                {/* <label for="uname">Text Query: </label> */}
                {/* <input type="text" onChange={handleTextInputChange} /> */}
                {/* <p /> */}
                <input type='file' onChange={handleFileInputChange} />
                <button type="submit">Upload</button>
            </form>

            {/* <div><img src="/uploads/23eb1448530add24409ed669467925c2.jpg" alt="oooh" /></div> */}

            {file && <p>{file.name}</p>}

            {help_info && help_info.map((cur_dict) =>
                <div>
                    <h1>System Answer</h1>
                    <img src={"/uploads/" + cur_dict.name} alt={"Doesnt work: /data/uploads/" + cur_dict.name} width="500" height="600"/>
                    <h3>{cur_dict.desc}</h3>
                </div>)}

            {is_not_auth && <h1><font color="red">Not Auth</font></h1>}
        </div>
    )
}

export default FileForm;
