import React, { useState } from "react";
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Board.css';
import {ApiURL} from '../../ApiURL/ApiURL';

function Boardcreate() {
    const navigate = useNavigate();
    const [board, setBoard] = useState({
        title: '',
        createBy: '',
        content: '',
        createDate: '',
    });
    const { title, createBy, content } = board;

    const onChange = (event) => {
        const date = new Date();
        console.log(event.target);
        const { name, value } = event.target;
        setBoard({
            ...board,
            [name]: value,
            createDate: `${date.getFullYear()}-${date.getMonth()}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}`
        });
    };
    const saveBoard = async () => {

        console.log({ board });
        await axios.post(`${ApiURL.Boardcreate_post}`, board).then((res) => {
            alert('등록되었습니다.');
            navigate('/Boardlist');

        });
    };
    const backToList = () => {
        navigate('/Boardlist');
    };

    return (
        <>
            <div className="form-group">
                <input type="text" name="title" value={title} onChange={onChange} placeholder="제목" />
            </div>
            <div className="form-group">
                <input type="text" name="createBy" value={createBy} onChange={onChange} placeholder="작성자" />
            </div>
            <div className="form-group">
                <textarea name="content" cols="30" row="10" value={content} onChange={onChange} placeholder=" 내용"></textarea>
            </div>
            <div className="form-button">
                <button onClick={saveBoard}>저장</button>
                <button onClick={backToList}>나가기</button>
            </div>
        </>

    );

}
export default Boardcreate;